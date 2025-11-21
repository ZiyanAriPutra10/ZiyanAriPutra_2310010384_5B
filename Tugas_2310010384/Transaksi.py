# Transaksi.py (KODE LENGKAP - DIPERBAIKI dan Ditambah Fitur Cari)

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QFile, QDate, Qt, QTimer # <<< Tambah QTimer
from PySide6.QtUiTools import QUiLoader
from crud import CRUD # <<< PENTING: Import kelas CRUD

class Transaksi(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        filenya = QFile('transaksi.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formTransaksi = muatfile.load(filenya,self)

        self.aksi = CRUD() # Inisialisasi objek CRUD
        self.kode_transaksi_terpilih = None

        # List untuk menyimpan data asli (9 kolom), dipakai untuk filter/search
        self.data_transaksi_full = [] # <<< Tambah data full (9 kolom)

        # Timer untuk debounce search
        self.search_timer = QTimer() # <<< Tambah timer
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_data)

        # 1. Hubungkan Tombol & Tabel
        self.formTransaksi.simpanButton.clicked.connect(self.simpan_data_transaksi)
        self.formTransaksi.ubahButton.clicked.connect(self.ubah_data_transaksi)
        self.formTransaksi.hapusButton.clicked.connect(self.hapus_data_transaksi)

        # Hubungkan klik baris tabel ke fungsi pengisi form
        try:
            self.formTransaksi.transaksiTableWidget.itemSelectionChanged.connect(self.ambil_data_dari_tabel)
        except AttributeError:
            pass

        # Pencarian realtime (debounce)
        try:
            self.formTransaksi.cariLineEdit.textChanged.connect(self.schedule_filter) # <<< Hubungkan cariLineEdit
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
        """Melakukan pemfilteran data transaksi berdasarkan teks di cariLineEdit."""
        keyword = self.formTransaksi.cariLineEdit.text().lower()
        table = self.formTransaksi.transaksiTableWidget

        # Kolom yang ditampilkan (6 kolom)
        kolom_display = ["Kode Transaksi", "Tgl Pemeriksaan", "Nama Pasien", "Nama Dokter", "Jenis Pemeriksaan", "Biaya"]

        table.setRowCount(0)

        # Iterasi pada data lengkap (9 kolom)
        for row_data in self.data_transaksi_full:
            # Kolom yang dicari:
            # 0: Kode Transaksi, 2: Nama Pasien, 3: Nama Dokter, 4: Jenis Pemeriksaan
            if (keyword in str(row_data[0]).lower() or # Kode Transaksi
                keyword in str(row_data[2]).lower() or # Nama Pasien
                keyword in str(row_data[3]).lower() or # Nama Dokter
                keyword in str(row_data[4]).lower()): # Jenis Pemeriksaan

                row_index = table.rowCount()
                table.insertRow(row_index)

                # Hanya masukkan 6 kolom display ke tabel
                for kolom, item in enumerate(row_data[:len(kolom_display)]):
                    new_item = QTableWidgetItem(str(item))
                    table.setItem(row_index, kolom, new_item)

        table.resizeColumnsToContents()

    # --- MEMUAT DATA DARI DB KE TABEL (READ) (DIMODIFIKASI) ---
    def load_data(self):
        data = self.aksi.ambil_semua_transaksi()
        self.data_transaksi_full = data # <<< SIMPAN DATA LENGKAP (9 kolom)
        table = self.formTransaksi.transaksiTableWidget

        # Kolom Display (sesuai query JOIN di crud.py)
        kolom_display = ["Kode Transaksi", "Tgl Pemeriksaan", "Nama Pasien", "Nama Dokter", "Jenis Pemeriksaan", "Biaya"]

        # Atur jumlah baris dan kolom
        table.setRowCount(len(data))
        table.setColumnCount(len(kolom_display))
        table.setHorizontalHeaderLabels(kolom_display)

        for baris, row_data in enumerate(data):
            for kolom, item in enumerate(row_data[:len(kolom_display)]):
                new_item = QTableWidgetItem(str(item))
                table.setItem(baris, kolom, new_item)

        table.resizeColumnsToContents()
        self.bersihkan_form()

    # --- MENYIMPAN DATA (CREATE) ---
    def simpan_data_transaksi(self):
        # Data untuk disimpan
        # kode = self.formTransaksi.kodeTransaksiLineEdit.text() # BARIS INI DIHAPUS
        tanggal_pemeriksaan = self.formTransaksi.tanggalTransaksiDateEdit.date().toString("yyyy-MM-dd")
        kode_dokter = self.formTransaksi.kodeDokterLineEdit.text()
        nomor_rm = self.formTransaksi.nomorRekamMedisLineEdit.text()
        kode_pemeriksaan = self.formTransaksi.kodePemeriksaanLineEdit.text()

        # Validasi hanya untuk FKs
        if not kode_dokter or not nomor_rm or not kode_pemeriksaan:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Semua field harus diisi.")
            return

        # Panggil fungsi tambah_transaksi dengan 4 argumen data (PK tidak dikirim)
        sukses, pesan = self.aksi.tambah_transaksi(
            tanggal_pemeriksaan,
            kode_dokter,
            nomor_rm,
            kode_pemeriksaan
        )

        if sukses:
            QMessageBox.information(self.formTransaksi, "Sukses", pesan)
            self.load_data()
            self.bersihkan_form() # Panggil bersihkan form agar siap input data baru
        else:
            QMessageBox.critical(self.formTransaksi, "Gagal", pesan)

    # --- MENGISI FORM DARI TABEL (SELECT) ---
    def ambil_data_dari_tabel(self):
        selected_items = self.formTransaksi.transaksiTableWidget.selectedItems()
        if not selected_items:
            return

        baris_tabel = self.formTransaksi.transaksiTableWidget.currentRow()

        # Ambil data lengkap (9 kolom) dari self.data_transaksi_full
        if baris_tabel >= len(self.data_transaksi_full):
            return

        data_row = self.data_transaksi_full[baris_tabel] # Mendapat 9 kolom dari load_data

        # Indeks data_row (sesuai urutan di crud.py):
        # 0: kode_transaksi, 1: tanggal_pemeriksaan, ...
        # 6: kode_dokter (FK), 7: nomor_rekam_medis (FK), 8: kode_pemeriksaan (FK)

        self.kode_transaksi_terpilih = data_row[0] # Simpan PK
        tanggal_db = str(data_row[1]) # Ambil tanggal

        # Isi form menggunakan Foreign Key (FK) dan PK
        self.formTransaksi.kodeTransaksiLineEdit.setText(str(data_row[0])) # Kode Transaksi

        # PERHATIAN: Di SELECT JOIN, Kode Dokter ada di indeks 6 dan Nomor RM di indeks 7
        # Namun, di kueri SELECT Anda, urutannya: (t.kode_dokter, t.nomor_rekam_medis)
        # 6: kode_dokter (FK), 7: nomor_rekam_medis (FK), 8: kode_pemeriksaan (FK)
        self.formTransaksi.kodeDokterLineEdit.setText(str(data_row[6]))
        self.formTransaksi.nomorRekamMedisLineEdit.setText(str(data_row[7]))
        self.formTransaksi.kodePemeriksaanLineEdit.setText(str(data_row[8])) # Kode Pemeriksaan

        self.formTransaksi.tanggalTransaksiDateEdit.setDate(QDate.fromString(tanggal_db, "yyyy-MM-dd"))
        self.formTransaksi.kodeTransaksiLineEdit.setEnabled(False)


    # --- MENGUBAH DATA (UPDATE) ---
    def ubah_data_transaksi(self):
        if not self.kode_transaksi_terpilih:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Pilih data Transaksi yang akan diubah dari tabel.")
            return

        kode_transaksi = self.kode_transaksi_terpilih
        tanggal_pemeriksaan = self.formTransaksi.tanggalTransaksiDateEdit.date().toString("yyyy-MM-dd")
        kode_dokter = self.formTransaksi.kodeDokterLineEdit.text()
        nomor_rm = self.formTransaksi.nomorRekamMedisLineEdit.text()
        kode_pemeriksaan = self.formTransaksi.kodePemeriksaanLineEdit.text()

        if not kode_dokter or not nomor_rm or not kode_pemeriksaan:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Semua field harus diisi.")
            return

        # Panggil fungsi ubah_transaksi dengan 5 argumen
        sukses, pesan = self.aksi.ubah_transaksi(
            kode_transaksi,
            tanggal_pemeriksaan,
            kode_dokter,
            nomor_rm,
            kode_pemeriksaan
        )

        if sukses:
            QMessageBox.information(self.formTransaksi, "Sukses", pesan)
            self.load_data()
            self.bersihkan_form()
        else:
            QMessageBox.critical(self.formTransaksi, "Gagal", pesan)

    # --- MENGHAPUS DATA (DELETE) ---\r\n
    def hapus_data_transaksi(self):
        if not self.kode_transaksi_terpilih:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Pilih data Transaksi yang akan dihapus dari tabel.")
            return

        konfirmasi = QMessageBox.question(self.formTransaksi, "Konfirmasi Hapus",
                                        f"Yakin ingin menghapus Transaksi dengan Kode {self.kode_transaksi_terpilih}?",
                                        QMessageBox.Yes | QMessageBox.No)

        if konfirmasi == QMessageBox.Yes:
            sukses, pesan = self.aksi.hapus_transaksi(self.kode_transaksi_terpilih)
            if sukses:
                QMessageBox.information(self.formTransaksi, "Sukses", pesan)
                self.load_data()
            else:
                QMessageBox.critical(self.formTransaksi, "Gagal", pesan)

        self.bersihkan_form()


    # --- FUNGSI UTILITY: MEMBERSIHKAN FORM ---\r\n
    def bersihkan_form(self):
        self.formTransaksi.kodeTransaksiLineEdit.clear()
        self.formTransaksi.kodeDokterLineEdit.clear()
        self.formTransaksi.nomorRekamMedisLineEdit.clear()
        self.formTransaksi.kodePemeriksaanLineEdit.clear()
        self.formTransaksi.tanggalTransaksiDateEdit.setDate(QDate.currentDate())
        self.kode_transaksi_terpilih = None
        self.formTransaksi.kodeTransaksiLineEdit.setEnabled(True)
