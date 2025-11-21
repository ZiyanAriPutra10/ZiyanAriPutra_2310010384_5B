# Pemeriksaan.py (KODE LENGKAP - DIPERBAIKI dan Ditambah Fitur Cari)

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QFile, Qt, QTimer # <<< Tambah QTimer
from PySide6.QtUiTools import QUiLoader
from crud import CRUD # <<< PENTING: Import kelas CRUD

class Pemeriksaan(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        filenya = QFile('pemeriksaan.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formPemeriksaan = muatfile.load(filenya,self)

        self.aksi = CRUD() # Inisialisasi objek CRUD
        self.kode_pemeriksaan_terpilih = None

        # List untuk menyimpan data asli, dipakai untuk filter/search
        self.data_pemeriksaan_full = [] # <<< Tambah data full

        # Timer untuk debounce search
        self.search_timer = QTimer() # <<< Tambah timer
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_data)

        # 1. Hubungkan Tombol & Tabel
        self.formPemeriksaan.simpanButton.clicked.connect(self.simpan_data_pemeriksaan)
        self.formPemeriksaan.ubahButton.clicked.connect(self.ubah_data_pemeriksaan)
        self.formPemeriksaan.hapusButton.clicked.connect(self.hapus_data_pemeriksaan)

        # Hubungkan klik baris tabel ke fungsi pengisi form
        try:
            self.formPemeriksaan.pemeriksaanTableWidget.itemSelectionChanged.connect(self.ambil_data_dari_tabel)
        except AttributeError:
            pass

        # Pencarian realtime (debounce)
        try:
            self.formPemeriksaan.cariLineEdit.textChanged.connect(self.schedule_filter) # <<< Hubungkan cariLineEdit
        except:
            pass

        # Panggil load data saat form dibuka
        self.load_data()

    # ======================================================
    # FUNGSI PENCARIAN (BARU)
    # ======================================================
    def schedule_filter(self):
        """Menjadwalkan filter data dengan penundaan (debounce) 200ms."""
        self.search_timer.start(200)

    def filter_data(self):
        """Melakukan pemfilteran data pemeriksaan berdasarkan teks di cariLineEdit."""
        keyword = self.formPemeriksaan.cariLineEdit.text().lower()
        table = self.formPemeriksaan.pemeriksaanTableWidget

        table.setRowCount(0)

        # Iterasi pada data lengkap (data_pemeriksaan_full)
        for row_data in self.data_pemeriksaan_full:
            # Cek di kolom 0 (Kode), 1 (Jenis Pemeriksaan)
            if (keyword in str(row_data[0]).lower() or
                keyword in str(row_data[1]).lower()):

                row_index = table.rowCount()
                table.insertRow(row_index)

                for kolom in range(3):
                    table.setItem(row_index, kolom, QTableWidgetItem(str(row_data[kolom])))

        table.resizeColumnsToContents()

    # --- MEMUAT DATA DARI DB KE TABEL (READ) (DIMODIFIKASI) ---
    def load_data(self):
        data = self.aksi.ambil_semua_pemeriksaan()
        self.data_pemeriksaan_full = data # <<< SIMPAN DATA LENGKAP
        table = self.formPemeriksaan.pemeriksaanTableWidget

        # Atur jumlah baris dan kolom
        table.setRowCount(len(data))
        table.setColumnCount(3)
        # DIPERBAIKI: Menggunakan 'Harga' sesuai DB
        table.setHorizontalHeaderLabels(["Kode Pemeriksaan", "Jenis Pemeriksaan", "Harga"])

        for baris, row_data in enumerate(data):
            for kolom, item in enumerate(row_data):
                new_item = QTableWidgetItem(str(item))
                table.setItem(baris, kolom, new_item)

        table.resizeColumnsToContents()
        self.bersihkan_form()

    # --- MENYIMPAN DATA (CREATE) ---
    def simpan_data_pemeriksaan(self):
        kode = self.formPemeriksaan.kodePemeriksaanLineEdit.text()
        jenis = self.formPemeriksaan.jenisPemeriksaanLineEdit.text()
        # Mengambil harga dari LineEdit, harusnya QSpinBox tapi mengikuti struktur original.
        harga = self.formPemeriksaan.hargaLineEdit.text()

        if not kode or not jenis or not harga:
            QMessageBox.warning(self.formPemeriksaan, "Peringatan", "Semua field harus diisi.")
            return

        try:
            harga_int = int(harga) # Konversi ke integer
        except ValueError:
            QMessageBox.warning(self.formPemeriksaan, "Peringatan", "Harga harus berupa angka.")
            return

        # DIPERBAIKI: Mengirim harga_int ke fungsi 'tambah_pemeriksaan'
        sukses, pesan = self.aksi.tambah_pemeriksaan(kode, jenis, harga_int)

        if sukses:
            QMessageBox.information(self.formPemeriksaan, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formPemeriksaan, "Gagal", pesan)

    # --- MENGISI FORM DARI TABEL (SELECT) ---
    def ambil_data_dari_tabel(self):
        selected_items = self.formPemeriksaan.pemeriksaanTableWidget.selectedItems()
        if not selected_items:
            return

        baris = selected_items[0].row()
        self.kode_pemeriksaan_terpilih = self.formPemeriksaan.pemeriksaanTableWidget.item(baris, 0).text()
        jenis = self.formPemeriksaan.pemeriksaanTableWidget.item(baris, 1).text()
        harga = self.formPemeriksaan.pemeriksaanTableWidget.item(baris, 2).text() # Kolom ke-3 adalah harga

        self.formPemeriksaan.kodePemeriksaanLineEdit.setText(self.kode_pemeriksaan_terpilih)
        self.formPemeriksaan.jenisPemeriksaanLineEdit.setText(jenis)
        self.formPemeriksaan.hargaLineEdit.setText(harga) # Menggunakan hargaLineEdit
        self.formPemeriksaan.kodePemeriksaanLineEdit.setEnabled(False) # Kunci Kode Pemeriksaan

    # --- MENGUBAH DATA (UPDATE) ---
    def ubah_data_pemeriksaan(self):
        if not self.kode_pemeriksaan_terpilih:
            QMessageBox.warning(self.formPemeriksaan, "Peringatan", "Pilih data Pemeriksaan yang akan diubah dari tabel.")
            return

        kode_lama = self.kode_pemeriksaan_terpilih
        kode_baru = self.formPemeriksaan.kodePemeriksaanLineEdit.text() # Seharusnya sama dengan kode_lama
        jenis = self.formPemeriksaan.jenisPemeriksaanLineEdit.text()
        harga = self.formPemeriksaan.hargaLineEdit.text()

        if not kode_baru or not jenis or not harga:
            QMessageBox.warning(self.formPemeriksaan, "Peringatan", "Semua field harus diisi.")
            return

        try:
            harga_int = int(harga)
        except ValueError:
            QMessageBox.warning(self.formPemeriksaan, "Peringatan", "Harga harus berupa angka.")
            return

        # DIPERBAIKI: Mengirim harga_int ke 'ubah_pemeriksaan'
        sukses, pesan = self.aksi.ubah_pemeriksaan(kode_lama, kode_baru, jenis, harga_int)

        if sukses:
            QMessageBox.information(self.formPemeriksaan, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formPemeriksaan, "Gagal", pesan)

    # --- MENGHAPUS DATA (DELETE) ---
    def hapus_data_pemeriksaan(self):
        if not self.kode_pemeriksaan_terpilih:
            QMessageBox.warning(self.formPemeriksaan, "Peringatan", "Pilih data Pemeriksaan yang akan dihapus dari tabel.")
            return

        konfirmasi = QMessageBox.question(self.formPemeriksaan, "Konfirmasi Hapus",
                                        f"Yakin ingin menghapus Pemeriksaan dengan Kode {self.kode_pemeriksaan_terpilih}?",
                                        QMessageBox.Yes | QMessageBox.No)

        if konfirmasi == QMessageBox.Yes:
            sukses, pesan = self.aksi.hapus_pemeriksaan(self.kode_pemeriksaan_terpilih)
            if sukses:
                QMessageBox.information(self.formPemeriksaan, "Sukses", pesan)
                self.load_data()
            else:
                QMessageBox.critical(self.formPemeriksaan, "Gagal", pesan)

        self.bersihkan_form()

    # --- FUNGSI UTILITY: MEMBERSIHKAN FORM ---
    def bersihkan_form(self):
        self.formPemeriksaan.kodePemeriksaanLineEdit.clear()
        self.formPemeriksaan.jenisPemeriksaanLineEdit.clear()
        self.formPemeriksaan.hargaLineEdit.clear()

        self.formPemeriksaan.kodePemeriksaanLineEdit.setEnabled(True) # Aktifkan kembali input kode
        self.kode_pemeriksaan_terpilih = None
