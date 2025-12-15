# Pemeriksaan.py (KODE LENGKAP - DIPERBAIKI dan Ditambah Fitur Cari + CETAK)
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QFile, Qt, QTimer
from PySide6.QtUiTools import QUiLoader
from crud import CRUD
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

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
        self.formPemeriksaan.cetakButton.clicked.connect(self.cetak_data_pemeriksaan) # <<< Tambah tombol cetak

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

    # --- CETAK DATA KE PDF (FUNGSI BARU) ---
    def cetak_data_pemeriksaan(self):
        """Mencetak data pemeriksaan ke file PDF"""
        if not self.data_pemeriksaan_full:
            QMessageBox.warning(self.formPemeriksaan, "Peringatan", "Tidak ada data untuk dicetak.")
            return

        # Dialog untuk memilih lokasi penyimpanan
        options = QFileDialog.Options()
        default_filename = f"data_pemeriksaan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filename, _ = QFileDialog.getSaveFileName(
            self.formPemeriksaan,
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
            elements.append(Paragraph("LAPORAN DATA PEMERIKSAAN", title_style))
            elements.append(Spacer(1, 20))

            # Tanggal cetak
            date_style = styles['Normal']
            date_text = f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
            elements.append(Paragraph(date_text, date_style))
            elements.append(Spacer(1, 20))

            # Siapkan data tabel
            headers = ["Kode Pemeriksaan", "Jenis Pemeriksaan", "Harga (Rp)"]
            table_data = [headers]

            for row in self.data_pemeriksaan_full:
                # Format harga dengan pemisah ribuan
                try:
                    harga = f"Rp {int(row[2]):,}".replace(",", ".")
                except:
                    harga = str(row[2])

                table_data.append([
                    str(row[0]),  # Kode
                    str(row[1]),  # Jenis
                    harga         # Harga
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

            # Atur alignment khusus untuk kolom harga
            table_style.add('ALIGN', (2, 1), (2, -1), 'RIGHT')

            table.setStyle(table_style)
            elements.append(table)

            # Tambah footer
            elements.append(Spacer(1, 20))
            footer_text = f"Jumlah Data: {len(self.data_pemeriksaan_full)}"
            elements.append(Paragraph(footer_text, date_style))

            # Build PDF
            doc.build(elements)

            QMessageBox.information(self.formPemeriksaan, "Sukses", f"PDF berhasil disimpan di:\n{filename}")

            # Buka file PDF (Windows)
            try:
                os.startfile(filename)
            except:
                pass

        except Exception as e:
            QMessageBox.critical(self.formPemeriksaan, "Gagal", f"Terjadi kesalahan saat membuat PDF:\n{str(e)}")

    # --- FUNGSI UTILITY: MEMBERSIHKAN FORM ---
    def bersihkan_form(self):
        self.formPemeriksaan.kodePemeriksaanLineEdit.clear()
        self.formPemeriksaan.jenisPemeriksaanLineEdit.clear()
        self.formPemeriksaan.hargaLineEdit.clear()

        self.formPemeriksaan.kodePemeriksaanLineEdit.setEnabled(True) # Aktifkan kembali input kode
        self.kode_pemeriksaan_terpilih = None
