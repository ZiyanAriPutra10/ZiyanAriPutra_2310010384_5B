# Dokter.py (MODIFIED to use crud.CRUD)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from crud import CRUD # Ganti QSqlDatabase, QSqlQuery dengan CRUD

class Dokter(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        filenya = QFile('dokter.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formDok = muatfile.load(filenya,self)

        self.aksi = CRUD() # Inisialisasi objek CRUD

        # 1. Hubungkan Tombol & Tabel
        self.formDok.simpanButton.clicked.connect(self.simpan_data_dokter)
        self.formDok.ubahButton.clicked.connect(self.ubah_data_dokter)
        self.formDok.hapusButton.clicked.connect(self.hapus_data_dokter)

        # Hubungkan klik baris tabel ke fungsi pengisi form
        try:
            self.formDok.dokterTableWidget.itemSelectionChanged.connect(self.ambil_data_dari_tabel)
        except AttributeError:
            pass

        # Panggil load data saat form dibuka
        self.load_data()

    # --- MEMUAT DATA DARI DB KE TABEL (READ) ---
    def load_data(self):
        data_dokter = self.aksi.ambil_semua_dokter()

        try:
            table = self.formDok.dokterTableWidget
        except AttributeError:
            return

        table.setRowCount(0)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Kode Dokter", "Nama Dokter", "Spesialis"])

        baris = 0
        for row_data in data_dokter:
            table.insertRow(baris)
            for kolom in range(3):
                table.setItem(baris, kolom, QTableWidgetItem(str(row_data[kolom])))
            baris += 1

        table.resizeColumnsToContents()
        self.bersihkan_form()

    # --- MENGAMBIL DATA DARI TABEL KE FORM ---
    def ambil_data_dari_tabel(self):
        # ... (Logika pengambilan data dari UI tetap sama) ...
        try:
            table = self.formDok.dokterTableWidget
            selected_row = table.currentRow()

            if selected_row >= 0:
                kode = table.item(selected_row, 0).text()
                nama = table.item(selected_row, 1).text()
                spesialis = table.item(selected_row, 2).text()

                self.formDok.kodeDokterLineEdit.setText(kode)
                self.formDok.namaDokterLineEdit.setText(nama)
                self.formDok.spesialisLineEdit.setText(spesialis)

                # Nonaktifkan PK saat mode Ubah/Hapus
                self.formDok.kodeDokterLineEdit.setEnabled(False)
                self.formDok.simpanButton.setEnabled(False)
                self.formDok.ubahButton.setEnabled(True)
                self.formDok.hapusButton.setEnabled(True)

        except Exception as e:
            print(f"Error saat ambil data dari tabel Dokter: {e}")

    # --- MENGUBAH DATA (UPDATE) ---
    def ubah_data_dokter(self):
        kode = self.formDok.kodeDokterLineEdit.text() # Kunci utama
        nama = self.formDok.namaDokterLineEdit.text()
        spesialis = self.formDok.spesialisLineEdit.text()

        sukses, pesan = self.aksi.ubah_dokter(kode, nama, spesialis)

        if sukses:
            QMessageBox.information(self.formDok, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formDok, "Gagal", pesan)

    # --- MENGHAPUS DATA (DELETE) ---
    def hapus_data_dokter(self):
        kode = self.formDok.kodeDokterLineEdit.text()

        reply = QMessageBox.question(self.formDok, 'Konfirmasi Hapus',
                                     f"Yakin ingin menghapus data Dokter dengan Kode: {kode}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No: return

        sukses, pesan = self.aksi.hapus_dokter(kode)

        if sukses:
            QMessageBox.information(self.formDok, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formDok, "Gagal", pesan)

    # --- MENYIMPAN DATA (CREATE) ---
    def simpan_data_dokter(self):
        kode = self.formDok.kodeDokterLineEdit.text()
        nama = self.formDok.namaDokterLineEdit.text()
        spesialis = self.formDok.spesialisLineEdit.text()

        if not kode or not nama:
            QMessageBox.warning(self.formDok, "Peringatan", "Kode dan Nama Dokter harus diisi.")
            return

        sukses, pesan = self.aksi.tambah_dokter(kode, nama, spesialis)

        if sukses:
            QMessageBox.information(self.formDok, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formDok, "Gagal", pesan)

    # --- FUNGSI UTILITY: MEMBERSIHKAN FORM ---
    def bersihkan_form(self):
        self.formDok.kodeDokterLineEdit.clear()
        self.formDok.namaDokterLineEdit.clear()
        self.formDok.spesialisLineEdit.clear()

        self.formDok.kodeDokterLineEdit.setEnabled(True)
        self.formDok.simpanButton.setEnabled(True)
        self.formDok.ubahButton.setEnabled(False)
        self.formDok.hapusButton.setEnabled(False)
