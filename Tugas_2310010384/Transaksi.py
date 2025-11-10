# Transaksi.py (KODE LENGKAP - DIPERBAIKI)

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QFile, QDate, Qt # Import Qt
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

        # 1. Hubungkan Tombol & Tabel
        self.formTransaksi.simpanButton.clicked.connect(self.simpan_data_transaksi)
        self.formTransaksi.ubahButton.clicked.connect(self.ubah_data_transaksi)
        self.formTransaksi.hapusButton.clicked.connect(self.hapus_data_transaksi)

        # Hubungkan klik baris tabel ke fungsi pengisi form
        try:
            self.formTransaksi.transaksiTableWidget.itemSelectionChanged.connect(self.ambil_data_dari_tabel)
        except AttributeError:
            pass

        # Panggil load data saat form dibuka
        self.load_data()

    # --- MEMUAT DATA DARI DB KE TABEL (READ) ---
    def load_data(self):
        data = self.aksi.ambil_semua_transaksi()
        table = self.formTransaksi.transaksiTableWidget

        # Kolom Display (sesuai query JOIN di crud.py)
        # DIPERBAIKI: 'Tgl Pemeriksaan' dan 'Biaya'
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
        kode_dokter = self.formTransaksi.kodeDokterLineEdit.text()
        nomor_rm = self.formTransaksi.nomorRekamMedisLineEdit.text()
        kode_pemeriksaan = self.formTransaksi.kodePemeriksaanLineEdit.text()
        # DIPERBAIKI: Mengambil tanggal dari 'tanggalTransaksiDateEdit'
        tanggal_pemeriksaan = self.formTransaksi.tanggalTransaksiDateEdit.date().toString("yyyy-MM-dd")

        if not kode_dokter or not nomor_rm or not kode_pemeriksaan:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Semua field harus diisi.")
            return

        # DIPERBAIKI: Panggil fungsi tambah_transaksi dengan 4 argumen
        sukses, pesan = self.aksi.tambah_transaksi(
            tanggal_pemeriksaan,
            kode_dokter,
            nomor_rm,
            kode_pemeriksaan
        )

        if sukses:
            QMessageBox.information(self.formTransaksi, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formTransaksi, "Gagal", pesan)

    # --- MENGISI FORM DARI TABEL (SELECT) ---
    def ambil_data_dari_tabel(self):
        selected_items = self.formTransaksi.transaksiTableWidget.selectedItems()
        if not selected_items:
            return

        baris = selected_items[0].row()
        data_db = self.aksi.ambil_semua_transaksi()
        if baris >= len(data_db):
            return

        data_row = data_db[baris] # Mendapat 9 kolom dari CRUD

        # Indeks data_row (sesuai urutan di crud.py yang baru):
        # 0: kode_transaksi, 1: tanggal_pemeriksaan (display), 2: nama_pasien (display),
        # 3: nama_dokter (display), 4: jenis_pemeriksaan (display), 5: harga (display),
        # 6: kode_dokter (FK), 7: nomor_rekam_medis (FK), 8: kode_pemeriksaan (FK)

        self.kode_transaksi_terpilih = data_row[0] # Simpan PK
        tanggal_db = data_row[1] # Ambil tanggal

        # Isi form menggunakan Foreign Key (FK)
        self.formTransaksi.kodeDokterLineEdit.setText(str(data_row[6]))
        self.formTransaksi.nomorRekamMedisLineEdit.setText(str(data_row[7]))
        self.formTransaksi.kodePemeriksaanLineEdit.setText(str(data_row[8]))
        self.formTransaksi.kodeTransaksiLineEdit.setText(str(data_row[0]))
        # DIPERBAIKI: Set tanggal di DateEdit
        self.formTransaksi.tanggalTransaksiDateEdit.setDate(QDate.fromString(tanggal_db, "yyyy-MM-dd"))


    # --- MENGUBAH DATA (UPDATE) ---
    def ubah_data_transaksi(self):
        if not self.kode_transaksi_terpilih:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Pilih data Transaksi yang akan diubah dari tabel.")
            return

        kode_transaksi = self.kode_transaksi_terpilih
        kode_dokter = self.formTransaksi.kodeDokterLineEdit.text()
        nomor_rm = self.formTransaksi.nomorRekamMedisLineEdit.text()
        kode_pemeriksaan = self.formTransaksi.kodePemeriksaanLineEdit.text()
        # DIPERBAIKI: Mengambil tanggal dari 'tanggalTransaksiDateEdit'
        tanggal_pemeriksaan = self.formTransaksi.tanggalTransaksiDateEdit.date().toString("yyyy-MM-dd")

        if not kode_dokter or not nomor_rm or not kode_pemeriksaan:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Semua field harus diisi.")
            return

        # DIPERBAIKI: Panggil fungsi ubah_transaksi dengan 5 argumen
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
        else:
            QMessageBox.critical(self.formTransaksi, "Gagal", pesan)

    # --- MENGHAPUS DATA (DELETE) ---
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


    # --- FUNGSI UTILITY: MEMBERSIHKAN FORM ---
    def bersihkan_form(self):
        self.formTransaksi.kodeTransaksiLineEdit.clear()
        self.formTransaksi.kodeDokterLineEdit.clear()
        self.formTransaksi.nomorRekamMedisLineEdit.clear()
        self.formTransaksi.kodePemeriksaanLineEdit.clear()
        self.formTransaksi.tanggalTransaksiDateEdit.setDate(QDate.currentDate())
        self.kode_transaksi_terpilih = None
