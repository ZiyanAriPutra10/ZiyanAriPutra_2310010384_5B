# Dokter.py (KODE LENGKAP DENGAN CETAK PDF)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QFile, QTimer
from PySide6.QtUiTools import QUiLoader
from crud import CRUD
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

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

        # Tombol CETAK
        self.formDok.cetakButton.clicked.connect(self.cetak_data_dokter)

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
    # CETAK DATA KE PDF (FUNGSI BARU)
    # ======================================================
    def cetak_data_dokter(self):
        """Mencetak data dokter ke file PDF"""
        if not self.data_dokter_full:
            QMessageBox.warning(self.formDok, "Peringatan", "Tidak ada data untuk dicetak.")
            return

        # Dialog untuk memilih lokasi penyimpanan
        options = QFileDialog.Options()
        default_filename = f"data_dokter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filename, _ = QFileDialog.getSaveFileName(
            self.formDok,
            "Simpan PDF",
            default_filename,
            "PDF Files (*.pdf);;All Files (*)",
            options=options
        )

        if not filename:
            return  # Pengguna membatalkan

        try:
            # Buat dokumen PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            elements = []

            # Styles
            styles = getSampleStyleSheet()

            # Judul
            title_style = styles['Heading1']
            title_style.alignment = 1  # Center
            elements.append(Paragraph("LAPORAN DATA DOKTER", title_style))
            elements.append(Spacer(1, 20))

            # Tanggal cetak
            date_style = styles['Normal']
            date_text = f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
            elements.append(Paragraph(date_text, date_style))
            elements.append(Spacer(1, 20))

            # Siapkan data tabel
            headers = ["Kode Dokter", "Nama Dokter", "Spesialis"]
            table_data = [headers]

            for row in self.data_dokter_full:
                table_data.append([str(row[0]), str(row[1]), str(row[2])])

            # Buat tabel
            table = Table(table_data, repeatRows=1)

            # Style tabel
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Alternating row colors
            for i in range(1, len(table_data)):
                if i % 2 == 0:
                    table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)

            table.setStyle(table_style)
            elements.append(table)

            # Tambah footer
            elements.append(Spacer(1, 20))
            footer_text = f"Jumlah Data: {len(self.data_dokter_full)}"
            elements.append(Paragraph(footer_text, date_style))

            # Build PDF
            doc.build(elements)

            QMessageBox.information(self.formDok, "Sukses", f"PDF berhasil disimpan di:\n{filename}")

            # Buka file PDF (Windows)
            try:
                os.startfile(filename)
            except:
                pass

        except Exception as e:
            QMessageBox.critical(self.formDok, "Gagal", f"Terjadi kesalahan saat membuat PDF:\n{str(e)}")

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
