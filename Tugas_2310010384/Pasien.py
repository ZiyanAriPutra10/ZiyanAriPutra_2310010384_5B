# Pasien.py (KODE LENGKAP - DENGAN FITUR CARI)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QFile, QDate, QTimer # <<< QTimer di-import
from PySide6.QtUiTools import QUiLoader
from crud import CRUD

class Pasien(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        filenya = QFile('pasien.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formPas = muatfile.load(filenya,self)

        # Inisialisasi objek CRUD
        self.aksi = CRUD()

        # List untuk menyimpan data asli, dipakai untuk filter/search
        self.data_pasien_full = [] # <<< Menyimpan data lengkap

        # Timer untuk debounce search
        self.search_timer = QTimer() # <<< Inisialisasi QTimer
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_data) # Hubungkan ke fungsi filter

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

        # Pencarian realtime (debounce)
        try:
            self.formPas.cariLineEdit.textChanged.connect(self.schedule_filter) # <<< Hubungkan cariLineEdit
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
        """Melakukan pemfilteran data pasien berdasarkan teks di cariLineEdit."""
        keyword = self.formPas.cariLineEdit.text().lower()
        table = self.formPas.pasienTableWidget

        table.setRowCount(0)

        # Iterasi pada data lengkap (data_pasien_full)
        for row_data in self.data_pasien_full:
            # Cari di kolom 0 (No RM), 1 (Nama Pasien), 3 (JK), 4 (Agama)
            if (keyword in str(row_data[0]).lower() or
                keyword in str(row_data[1]).lower() or
                keyword in str(row_data[3]).lower() or
                keyword in str(row_data[4]).lower()):

                row_index = table.rowCount()
                table.insertRow(row_index)

                for kolom in range(5):
                    table.setItem(row_index, kolom, QTableWidgetItem(str(row_data[kolom])))

        table.resizeColumnsToContents()

    # ======================================================
    # MEMUAT DATA DARI DB KE TABEL (READ) (DIMODIFIKASI)
    # ======================================================
    def load_data(self):
        data_pasien = self.aksi.ambil_semua_pasien()
        self.data_pasien_full = data_pasien # <<< SIMPAN DATA LENGKAP

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

    # ======================================================
    # AMBIL DATA DARI TABEL KE FORM
    # ======================================================
    def ambil_data_dari_tabel(self):
        try:
            selected_items = self.formPas.pasienTableWidget.selectedItems()
            if not selected_items:
                return

            baris = selected_items[0].row()
            table = self.formPas.pasienTableWidget

            # Ambil nilai dari kolom yang ditampilkan (0 sampai 4)
            nomor_rm = table.item(baris, 0).text()
            nama_pasien = table.item(baris, 1).text()
            tgl_lahir_str = table.item(baris, 2).text()
            jenis_kelamin = table.item(baris, 3).text()
            agama = table.item(baris, 4).text()

            # Isi form
            self.formPas.nomoRekamMedisLineEdit.setText(nomor_rm)
            self.formPas.namaPasienLineEdit.setText(nama_pasien)

            # Konversi string tanggal ke objek QDate
            tgl_lahir_qdate = QDate.fromString(tgl_lahir_str, "yyyy-MM-dd")
            self.formPas.tanggalLahirDateEdit.setDate(tgl_lahir_qdate)

            self.formPas.jenisKelaminLineEdit.setText(jenis_kelamin)
            self.formPas.agamaLineEdit.setText(agama)

            # Nonaktifkan Nomor Rekam Medis untuk operasi Ubah/Hapus
            self.formPas.nomoRekamMedisLineEdit.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self.formPas, "Error", f"Gagal mengambil data dari tabel: {e}")

    # ======================================================
    # SIMPAN DATA (CREATE)
    # ======================================================
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

    # ======================================================
    # UBAH DATA (UPDATE)
    # ======================================================
    def ubah_data_pasien(self):
        nomor_rm = self.formPas.nomoRekamMedisLineEdit.text()
        nama_pasien = self.formPas.namaPasienLineEdit.text()
        tgl_lahir = self.formPas.tanggalLahirDateEdit.date().toString("yyyy-MM-dd")
        jenis_kelamin = self.formPas.jenisKelaminLineEdit.text()
        agama = self.formPas.agamaLineEdit.text()

        if not nomor_rm or self.formPas.nomoRekamMedisLineEdit.isEnabled():
            QMessageBox.warning(self.formPas, "Peringatan", "Pilih data pasien dari tabel yang akan diubah.")
            return

        sukses, pesan = self.aksi.ubah_pasien(nomor_rm, nama_pasien, tgl_lahir, jenis_kelamin, agama)

        if sukses:
            QMessageBox.information(self.formPas, "Sukses", pesan)
            self.load_data()
            self.bersihkan_form()
        else:
            QMessageBox.critical(self.formPas, "Gagal", pesan)

    # ======================================================
    # HAPUS DATA (DELETE)
    # ======================================================
    def hapus_data_pasien(self):
        nomor_rm = self.formPas.nomoRekamMedisLineEdit.text()

        if not nomor_rm or self.formPas.nomoRekamMedisLineEdit.isEnabled():
            QMessageBox.warning(self.formPas, "Peringatan", "Pilih data pasien dari tabel yang akan dihapus.")
            return

        reply = QMessageBox.question(
            self.formPas,
            'Konfirmasi Hapus',
            f"Yakin ingin menghapus data Pasien dengan No RM: {nomor_rm}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        sukses, pesan = self.aksi.hapus_pasien(nomor_rm)

        if sukses:
            QMessageBox.information(self.formPas, "Sukses", pesan)
            self.load_data()
            self.bersihkan_form()
        else:
            QMessageBox.critical(self.formPas, "Gagal", pesan)


    # ======================================================
    # FUNGSI UTILITY: MEMBERSIHKAN FORM
    # ======================================================
    def bersihkan_form(self):
        self.formPas.nomoRekamMedisLineEdit.clear()
        self.formPas.namaPasienLineEdit.clear()
        self.formPas.jenisKelaminLineEdit.clear()
        self.formPas.agamaLineEdit.clear()
        self.formPas.tanggalLahirDateEdit.setDate(QDate.currentDate()) # Set ke tanggal hari ini

        # Aktifkan kembali Nomor Rekam Medis
        self.formPas.nomoRekamMedisLineEdit.setEnabled(True)
