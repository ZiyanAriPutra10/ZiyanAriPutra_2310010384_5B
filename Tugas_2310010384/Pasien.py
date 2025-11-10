# Pasien.py (MODIFIED)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QFile, QDate
from PySide6.QtUiTools import QUiLoader
# Modifikasi Import: Sekarang import kelas CRUD dari file crud
from crud import CRUD
# Hapus import QSqlDatabase, QSqlQuery karena kita menggunakan mysql.connector

class Pasien(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        filenya = QFile('pasien.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formPas = muatfile.load(filenya,self)

        # Inisialisasi objek CRUD
        self.aksi = CRUD() # Ganti CRUDRumahSakit() menjadi CRUD()

        # 1. Hubungkan Tombol & Tabel
        self.formPas.simpanButton.clicked.connect(self.simpan_data_pasien)
        self.formPas.ubahButton.clicked.connect(self.ubah_data_pasien)
        self.formPas.hapusButton.clicked.connect(self.hapus_data_pasien)

        # Hubungkan klik baris tabel ke fungsi pengisi form
        try:
            self.formPas.pasienTableWidget.itemSelectionChanged.connect(self.ambil_data_dari_tabel)
        except AttributeError:
            QMessageBox.critical(self.formPas, "Error UI",
                                 "Widget 'pasienTableWidget' tidak ditemukan di pasien.ui.")
            return

        # Panggil load data saat form dibuka
        self.load_data()

    # --- FUNGSI BARU: MENGAMBIL DATA DARI TABEL KE FORM ---
    def ambil_data_dari_tabel(self):
        # ... (Tidak ada perubahan di sini) ...
        try:
            table = self.formPas.pasienTableWidget
            selected_row = table.currentRow()

            if selected_row >= 0:
                # Ambil data dari kolom (index 0 hingga 4)
                nomor_rm = table.item(selected_row, 0).text()
                nama_pasien = table.item(selected_row, 1).text()
                tgl_lahir_str = table.item(selected_row, 2).text()
                jenis_kelamin = table.item(selected_row, 3).text()
                agama = table.item(selected_row, 4).text()

                # Isi LineEdit/DateEdit
                self.formPas.nomoRekamMedisLineEdit.setText(nomor_rm)
                self.formPas.namaPasienLineEdit.setText(nama_pasien)
                self.formPas.jenisKelaminLineEdit.setText(jenis_kelamin)
                self.formPas.agamaLineEdit.setText(agama)

                # Konversi string tanggal (YYYY-MM-DD) ke objek QDate
                tgl_lahir_qdate = QDate.fromString(tgl_lahir_str, "yyyy-MM-dd")
                self.formPas.tanggalLahirDateEdit.setDate(tgl_lahir_qdate)

                # Saat data sudah terisi, Nonaktifkan field Nomor RM (Primary Key)
                self.formPas.nomoRekamMedisLineEdit.setEnabled(False)
                self.formPas.simpanButton.setEnabled(False)
                self.formPas.ubahButton.setEnabled(True)
                self.formPas.hapusButton.setEnabled(True)

        except Exception as e:
            print(f"Error saat ambil data dari tabel: {e}")


    # --- FUNGSI BARU: MENGUBAH DATA (UPDATE) ---
    def ubah_data_pasien(self):
        # 1. Ambil Data dari Form
        nomor_rm = self.formPas.nomoRekamMedisLineEdit.text()
        nama_pasien = self.formPas.namaPasienLineEdit.text()
        tgl_lahir = self.formPas.tanggalLahirDateEdit.date().toString("yyyy-MM-dd")
        jenis_kelamin = self.formPas.jenisKelaminLineEdit.text()
        agama = self.formPas.agamaLineEdit.text()

        # Panggil metode ubah_pasien dari kelas CRUD
        sukses, pesan = self.aksi.ubah_pasien(nomor_rm, nama_pasien, tgl_lahir, jenis_kelamin, agama)

        # 3. Tampilkan Hasil
        if sukses:
            QMessageBox.information(self.formPas, "Sukses", pesan)
            self.load_data()
            self.bersihkan_form()
        else:
            QMessageBox.critical(self.formPas, "Gagal", pesan)


    # --- FUNGSI BARU: MENGHAPUS DATA (DELETE) ---
    def hapus_data_pasien(self):
        nomor_rm = self.formPas.nomoRekamMedisLineEdit.text()

        # Konfirmasi penghapusan
        reply = QMessageBox.question(self.formPas, 'Konfirmasi Hapus',
                                     f"Yakin ingin menghapus data pasien dengan No. RM: {nomor_rm}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return

        # Panggil metode hapus_pasien dari kelas CRUD
        sukses, pesan = self.aksi.hapus_pasien(nomor_rm)

        # Eksekusi Kueri
        if sukses:
            QMessageBox.information(self.formPas, "Sukses", pesan)
            self.load_data()
            self.bersihkan_form()
        else:
            QMessageBox.critical(self.formPas, "Gagal", pesan)

    # --- FUNGSI LOAD ---
    def load_data(self):
        data_pasien = self.aksi.ambil_semua_pasien()

        try:
            table = self.formPas.pasienTableWidget
        except AttributeError:
            return

        table.setRowCount(0)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["No RM", "Nama Pasien", "Tgl Lahir", "JK", "Agama"])

        baris = 0
        for row_data in data_pasien:
            table.insertRow(baris)
            for kolom in range(5):
                # Konversi semua nilai ke string sebelum dimasukkan ke QTableWidgetItem
                table.setItem(baris, kolom, QTableWidgetItem(str(row_data[kolom])))
            baris += 1

        table.resizeColumnsToContents()
        self.bersihkan_form()

    def simpan_data_pasien(self):
        nomor_rm = self.formPas.nomoRekamMedisLineEdit.text()
        nama_pasien = self.formPas.namaPasienLineEdit.text()
        tgl_lahir = self.formPas.tanggalLahirDateEdit.date().toString("yyyy-MM-dd")
        jenis_kelamin = self.formPas.jenisKelaminLineEdit.text()
        agama = self.formPas.agamaLineEdit.text()

        if not nomor_rm:
            QMessageBox.warning(self.formPas, "Peringatan", "Nomor Rekam Medis harus diisi.")
            return

        # Panggil metode tambah_pasien dari kelas CRUD
        sukses, pesan = self.aksi.tambah_pasien(nomor_rm, nama_pasien, tgl_lahir, jenis_kelamin, agama)

        if sukses:
            QMessageBox.information(self.formPas, "Sukses", pesan)
            self.load_data()
            self.bersihkan_form()
        else:
            QMessageBox.critical(self.formPas, "Gagal", pesan)


    # --- FUNGSI UTILITY: MEMBERSIHKAN FORM ---
    def bersihkan_form(self):
        self.formPas.nomoRekamMedisLineEdit.clear()
        self.formPas.namaPasienLineEdit.clear()
        self.formPas.jenisKelaminLineEdit.clear()
        self.formPas.agamaLineEdit.clear()
        self.formPas.tanggalLahirDateEdit.setDate(QDate.currentDate())

        # Aktifkan kembali mode SIMPAN
        self.formPas.nomoRekamMedisLineEdit.setEnabled(True)
        self.formPas.simpanButton.setEnabled(True)
        self.formPas.ubahButton.setEnabled(False)
        self.formPas.hapusButton.setEnabled(False)
