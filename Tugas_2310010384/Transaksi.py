# Transaksi.py (KODE LENGKAP - DIPERBAIKI dan Ditambah Fitur Cari + CETAK)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QFile, QDate, Qt, QTimer
from PySide6.QtUiTools import QUiLoader
from crud import CRUD
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

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
        self.formTransaksi.cetakButton.clicked.connect(self.cetak_data_transaksi) # <<< Tambah tombol cetak

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

    # --- CETAK DATA KE PDF (FUNGSI BARU) ---
    def cetak_data_transaksi(self):
        """Mencetak data transaksi ke file PDF"""
        if not self.data_transaksi_full:
            QMessageBox.warning(self.formTransaksi, "Peringatan", "Tidak ada data untuk dicetak.")
            return

        # Dialog untuk memilih lokasi penyimpanan
        options = QFileDialog.Options()
        default_filename = f"data_transaksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filename, _ = QFileDialog.getSaveFileName(
            self.formTransaksi,
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
            elements.append(Paragraph("LAPORAN DATA TRANSAKSI", title_style))
            elements.append(Spacer(1, 20))

            # Tanggal cetak
            date_style = styles['Normal']
            date_text = f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
            elements.append(Paragraph(date_text, date_style))
            elements.append(Spacer(1, 20))

            # Siapkan data tabel
            headers = ["Kode Transaksi", "Tgl Pemeriksaan", "Nama Pasien",
                      "Nama Dokter", "Jenis Pemeriksaan", "Biaya (Rp)"]
            table_data = [headers]

            for row in self.data_transaksi_full:
                # Format biaya dengan pemisah ribuan
                try:
                    biaya = f"Rp {int(row[5]):,}".replace(",", ".")
                except:
                    biaya = str(row[5])

                table_data.append([
                    str(row[0]),  # Kode Transaksi
                    str(row[1]),  # Tgl Pemeriksaan
                    str(row[2]),  # Nama Pasien
                    str(row[3]),  # Nama Dokter
                    str(row[4]),  # Jenis Pemeriksaan
                    biaya         # Biaya
                ])

            # Buat tabel
            table = Table(table_data, repeatRows=1)

            # Style tabel
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Alternating row colors
            for i in range(1, len(table_data)):
                if i % 2 == 0:
                    table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)

            # Atur alignment khusus untuk kolom nama
            table_style.add('ALIGN', (2, 1), (2, -1), 'LEFT')  # Nama Pasien rata kiri
            table_style.add('ALIGN', (3, 1), (3, -1), 'LEFT')  # Nama Dokter rata kiri
            table_style.add('ALIGN', (5, 1), (5, -1), 'RIGHT') # Biaya rata kanan

            # Atur lebar kolom
            col_widths = [80, 80, 100, 100, 100, 80]
            table._argW = col_widths

            table.setStyle(table_style)
            elements.append(table)

            # Tambah footer
            elements.append(Spacer(1, 20))
            footer_text = f"Jumlah Data: {len(self.data_transaksi_full)}"
            elements.append(Paragraph(footer_text, date_style))

            # Build PDF
            doc.build(elements)

            QMessageBox.information(self.formTransaksi, "Sukses", f"PDF berhasil disimpan di:\n{filename}")

            # Buka file PDF (Windows)
            try:
                os.startfile(filename)
            except:
                pass

        except Exception as e:
            QMessageBox.critical(self.formTransaksi, "Gagal", f"Terjadi kesalahan saat membuat PDF:\n{str(e)}")

    # --- FUNGSI UTILITY: MEMBERSIHKAN FORM ---
    def bersihkan_form(self):
        self.formTransaksi.kodeTransaksiLineEdit.clear()
        self.formTransaksi.kodeDokterLineEdit.clear()
        self.formTransaksi.nomorRekamMedisLineEdit.clear()
        self.formTransaksi.kodePemeriksaanLineEdit.clear()
        self.formTransaksi.tanggalTransaksiDateEdit.setDate(QDate.currentDate())
        self.kode_transaksi_terpilih = None
        self.formTransaksi.kodeTransaksiLineEdit.setEnabled(True)
