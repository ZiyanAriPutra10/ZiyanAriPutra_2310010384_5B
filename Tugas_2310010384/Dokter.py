from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QFile, QTimer
from PySide6.QtUiTools import QUiLoader
from crud import CRUD


class Dokter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        filenya = QFile('dokter.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formDok = muatfile.load(filenya, self)

        self.aksi = CRUD()

        # List untuk menyimpan data asli, dipakai untuk filter
        self.data_dokter_full = []

        # Timer untuk debounce search
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_data)

        # Tombol CRUD
        self.formDok.simpanButton.clicked.connect(self.simpan_data_dokter)
        self.formDok.ubahButton.clicked.connect(self.ubah_data_dokter)
        self.formDok.hapusButton.clicked.connect(self.hapus_data_dokter)

        # Klik tabel → isi form
        try:
            self.formDok.dokterTableWidget.itemSelectionChanged.connect(self.ambil_data_dari_tabel)
        except:
            pass

        # Pencarian realtime (debounce)
        try:
            self.formDok.cariLineEdit.textChanged.connect(self.schedule_filter)
        except:
            pass

        # Load awal
        self.load_data()

    # ======================================================
    # LOAD DATA
    # ======================================================
    def load_data(self):
        data_dokter = self.aksi.ambil_semua_dokter()
        self.data_dokter_full = data_dokter  # Simpan data untuk search

        table = self.formDok.dokterTableWidget

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

    # ======================================================
    # DEBOUNCE SEARCH
    # ======================================================
    def schedule_filter(self):
        self.search_timer.start(200)  # 200 ms (0.2 detik)

    # ======================================================
    # FILTER SEARCH
    # ======================================================
    def filter_data(self):
        keyword = self.formDok.cariLineEdit.text().lower()
        table = self.formDok.dokterTableWidget

        table.setRowCount(0)

        for row_data in self.data_dokter_full:
            if (keyword in row_data[0].lower() or
                keyword in row_data[1].lower() or
                keyword in row_data[2].lower()):

                row_index = table.rowCount()
                table.insertRow(row_index)

                for kolom in range(3):
                    table.setItem(row_index, kolom, QTableWidgetItem(str(row_data[kolom])))

        table.resizeColumnsToContents()

    # ======================================================
    # AMBIL DATA DARI TABEL
    # ======================================================
    def ambil_data_dari_tabel(self):
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

                # Mode Ubah/Hapus
                self.formDok.kodeDokterLineEdit.setEnabled(False)
                self.formDok.simpanButton.setEnabled(False)
                self.formDok.ubahButton.setEnabled(True)
                self.formDok.hapusButton.setEnabled(True)

        except Exception as e:
            print(f"Error ambil data tabel: {e}")

    # ======================================================
    # SIMPAN DATA
    # ======================================================
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

    # ======================================================
    # UBAH DATA
    # ======================================================
    def ubah_data_dokter(self):
        kode = self.formDok.kodeDokterLineEdit.text()
        nama = self.formDok.namaDokterLineEdit.text()
        spesialis = self.formDok.spesialisLineEdit.text()

        sukses, pesan = self.aksi.ubah_dokter(kode, nama, spesialis)

        if sukses:
            QMessageBox.information(self.formDok, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formDok, "Gagal", pesan)

    # ======================================================
    # HAPUS DATA
    # ======================================================
    def hapus_data_dokter(self):
        kode = self.formDok.kodeDokterLineEdit.text()

        reply = QMessageBox.question(
            self.formDok,
            'Konfirmasi Hapus',
            f"Yakin ingin menghapus data Dokter dengan Kode: {kode}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        sukses, pesan = self.aksi.hapus_dokter(kode)

        if sukses:
            QMessageBox.information(self.formDok, "Sukses", pesan)
            self.load_data()
        else:
            QMessageBox.critical(self.formDok, "Gagal", pesan)

    # ======================================================
    # BERSIHKAN FORM
    # ======================================================
    def bersihkan_form(self):
        self.formDok.kodeDokterLineEdit.clear()
        self.formDok.namaDokterLineEdit.clear()
        self.formDok.spesialisLineEdit.clear()

        self.formDok.kodeDokterLineEdit.setEnabled(True)
        self.formDok.simpanButton.setEnabled(True)
        self.formDok.ubahButton.setEnabled(False)
        self.formDok.hapusButton.setEnabled(False)
