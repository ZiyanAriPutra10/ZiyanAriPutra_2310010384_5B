# Pasien.py (KODE LENGKAP - DENGAN FITUR CARI DAN CETAK)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QFile, QDate, QTimer
from PySide6.QtUiTools import QUiLoader
from crud import CRUD
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

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
        self.formPas.cetakButton.clicked.connect(self.cetak_data_pasien) # <<< Tambah tombol cetak

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
    # FUNGSI PENCARIAN
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
    # MEMUAT DATA DARI DB KE TABEL
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
    # CETAK DATA KE PDF (FUNGSI BARU)
    # ======================================================
    def cetak_data_pasien(self):
        """Mencetak data pasien ke file PDF"""
        if not self.data_pasien_full:
            QMessageBox.warning(self.formPas, "Peringatan", "Tidak ada data untuk dicetak.")
            return

        # Dialog untuk memilih lokasi penyimpanan
        options = QFileDialog.Options()
        default_filename = f"data_pasien_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filename, _ = QFileDialog.getSaveFileName(
            self.formPas,
            "Simpan PDF",
            default_filename,
            "PDF Files (*.pdf);;All Files (*)",
            options=options
        )

        if not filename:
            return

        try:
            # Buat dokumen PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            elements = []

            # Styles
            styles = getSampleStyleSheet()

            # Judul
            title_style = styles['Heading1']
            title_style.alignment = 1  # Center
            elements.append(Paragraph("LAPORAN DATA PASIEN", title_style))
            elements.append(Spacer(1, 20))

            # Tanggal cetak
            date_style = styles['Normal']
            date_text = f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
            elements.append(Paragraph(date_text, date_style))
            elements.append(Spacer(1, 20))

            # Siapkan data tabel
            headers = ["No RM", "Nama Pasien", "Tanggal Lahir", "Jenis Kelamin", "Agama"]
            table_data = [headers]

            for row in self.data_pasien_full:
                table_data.append([
                    str(row[0]),  # No RM
                    str(row[1]),  # Nama
                    str(row[2]),  # Tgl Lahir
                    str(row[3]),  # JK
                    str(row[4])   # Agama
                ])

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

            # Atur lebar kolom
            table_style.add('ALIGN', (1, 0), (1, -1), 'LEFT')  # Nama rata kiri

            table.setStyle(table_style)
            elements.append(table)

            # Tambah footer
            elements.append(Spacer(1, 20))
            footer_text = f"Jumlah Data: {len(self.data_pasien_full)}"
            elements.append(Paragraph(footer_text, date_style))

            # Build PDF
            doc.build(elements)

            QMessageBox.information(self.formPas, "Sukses", f"PDF berhasil disimpan di:\n{filename}")

            # Buka file PDF (Windows)
            try:
                os.startfile(filename)
            except:
                pass

        except Exception as e:
            QMessageBox.critical(self.formPas, "Gagal", f"Terjadi kesalahan saat membuat PDF:\n{str(e)}")

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
