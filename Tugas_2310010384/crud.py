# crud.py (KODE LENGKAP - FUNGSI UBAH PASIEN & DOKTER DIPERBAIKI)

import mysql.connector
import sys

# Konfigurasi Koneksi Database
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PORT = '8111'
DB_PASSWORD = ''
DB_NAME = 'tugas_2310010384'

class CRUD:
    def __init__(self):
        try:
            self.koneksi = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                port=DB_PORT,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        except mysql.connector.Error as err:
            print(f"Error Koneksi Database: {err}")
            sys.exit(1) # Keluar jika koneksi gagal

    # =========================================================
    # 🧑 Operasi CRUD untuk Tabel PASIEN
    # =========================================================

    def ambil_semua_pasien(self):
        aksi = self.koneksi.cursor()
        aksi.execute("SELECT nomor_rekam_medis, nama_pasien, tanggal_lahir, jenis_kelamin, agama FROM pasien")
        data = aksi.fetchall()
        aksi.close()
        return data

    def tambah_pasien(self, nomor_rm, nama, tgl_lahir, jk, agama):
        aksi = self.koneksi.cursor()
        sql = "INSERT INTO pasien (nomor_rekam_medis, nama_pasien, tanggal_lahir, jenis_kelamin, agama) VALUES (%s, %s, %s, %s, %s)"
        try:
            aksi.execute(sql, (nomor_rm, nama, tgl_lahir, jk, agama))
            self.koneksi.commit()
            return True, "Data Pasien berhasil disimpan!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menyimpan data Pasien: {err}"
        finally:
            aksi.close()

    # --- FUNGSI INI DIPERBAIKI ---
    def ubah_pasien(self, nomor_rm, nama, tgl_lahir, jk, agama):
        aksi = self.koneksi.cursor()
        # Primary Key (nomor_rekam_medis) tidak diubah, hanya digunakan di WHERE
        sql = "UPDATE pasien SET nama_pasien = %s, tanggal_lahir = %s, jenis_kelamin = %s, agama = %s WHERE nomor_rekam_medis = %s"
        try:
            # Urutan parameter disesuaikan: (nama, tgl_lahir, jk, agama, nomor_rm)
            aksi.execute(sql, (nama, tgl_lahir, jk, agama, nomor_rm))
            self.koneksi.commit()
            return True, "Data Pasien berhasil diubah!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal mengubah data Pasien: {err}"
        finally:
            aksi.close()

    def hapus_pasien(self, nomor_rm):
        aksi = self.koneksi.cursor()
        sql = "DELETE FROM pasien WHERE nomor_rekam_medis = %s"
        try:
            aksi.execute(sql, (nomor_rm,))
            self.koneksi.commit()
            return True, "Data Pasien berhasil dihapus!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menghapus data Pasien: {err} (Pastikan tidak ada relasi di tabel Transaksi)"
        finally:
            aksi.close()

    # =========================================================
    # 👨‍⚕️ Operasi CRUD untuk Tabel DOKTER
    # =========================================================

    def ambil_semua_dokter(self):
        aksi = self.koneksi.cursor()
        aksi.execute("SELECT kode_dokter, nama_dokter, spesialis FROM dokter")
        data = aksi.fetchall()
        aksi.close()
        return data

    def tambah_dokter(self, kode, nama, spesialis):
        aksi = self.koneksi.cursor()
        sql = "INSERT INTO dokter (kode_dokter, nama_dokter, spesialis) VALUES (%s, %s, %s)"
        try:
            aksi.execute(sql, (kode, nama, spesialis))
            self.koneksi.commit()
            return True, "Data Dokter berhasil disimpan!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menyimpan data Dokter: {err}"
        finally:
            aksi.close()

    # --- FUNGSI INI DIPERBAIKI ---
    def ubah_dokter(self, kode, nama, spesialis):
        aksi = self.koneksi.cursor()
        # Primary Key (kode_dokter) tidak diubah, hanya digunakan di WHERE
        sql = "UPDATE dokter SET nama_dokter = %s, spesialis = %s WHERE kode_dokter = %s"
        try:
            # Urutan parameter disesuaikan: (nama, spesialis, kode)
            aksi.execute(sql, (nama, spesialis, kode))
            self.koneksi.commit()
            return True, "Data Dokter berhasil diubah!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal mengubah data Dokter: {err}"
        finally:
            aksi.close()

    def hapus_dokter(self, kode):
        aksi = self.koneksi.cursor()
        sql = "DELETE FROM dokter WHERE kode_dokter = %s"
        try:
            aksi.execute(sql, (kode,))
            self.koneksi.commit()
            return True, "Data Dokter berhasil dihapus!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menghapus data Dokter: {err} (Pastikan tidak ada relasi di tabel Transaksi)"
        finally:
            aksi.close()

    # =========================================================
    # 📋 Operasi CRUD untuk Tabel PEMERIKSAAN
    # =========================================================

    def ambil_semua_pemeriksaan(self):
        aksi = self.koneksi.cursor()
        aksi.execute("SELECT kode_pemeriksaan, jenis_pemeriksaan, harga FROM pemeriksaan")
        data = aksi.fetchall()
        aksi.close()
        return data

    def tambah_pemeriksaan(self, kode, jenis, harga):
        aksi = self.koneksi.cursor()
        sql = "INSERT INTO pemeriksaan (kode_pemeriksaan, jenis_pemeriksaan, harga) VALUES (%s, %s, %s)"
        try:
            aksi.execute(sql, (kode, jenis, harga))
            self.koneksi.commit()
            return True, "Data Pemeriksaan berhasil disimpan!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menyimpan data Pemeriksaan: {err}"
        finally:
            aksi.close()

    def ubah_pemeriksaan(self, kode_lama, kode_baru, jenis, harga):
        aksi = self.koneksi.cursor()
        sql = "UPDATE pemeriksaan SET kode_pemeriksaan = %s, jenis_pemeriksaan = %s, harga = %s WHERE kode_pemeriksaan = %s"
        try:
            # Kode di sini mengizinkan perubahan PK, tapi disarankan untuk tidak melakukannya
            aksi.execute(sql, (kode_baru, jenis, harga, kode_lama))
            self.koneksi.commit()
            return True, "Data Pemeriksaan berhasil diubah!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal mengubah data Pemeriksaan: {err}"
        finally:
            aksi.close()

    def hapus_pemeriksaan(self, kode):
        aksi = self.koneksi.cursor()
        sql = "DELETE FROM pemeriksaan WHERE kode_pemeriksaan = %s"
        try:
            aksi.execute(sql, (kode,))
            self.koneksi.commit()
            return True, "Data Pemeriksaan berhasil dihapus!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menghapus data Pemeriksaan: {err} (Pastikan tidak ada relasi di tabel Transaksi)"
        finally:
            aksi.close()


    # =========================================================
    # 💵 Operasi CRUD untuk Tabel TRANSAKSI (MENGGUNAKAN JOIN)
    # =========================================================

    def ambil_semua_transaksi(self):
        aksi = self.koneksi.cursor()
        sql = """
        SELECT
            t.kode_transaksi,
            t.tanggal_pemeriksaan,
            p.nama_pasien,
            d.nama_dokter,
            pm.jenis_pemeriksaan,
            pm.harga,
            t.kode_dokter,      -- KOLOM 6 (FK)
            t.nomor_rekam_medis, -- KOLOM 7 (FK)
            t.kode_pemeriksaan  -- KOLOM 8 (FK)
        FROM transaksi t
        JOIN pasien p ON t.nomor_rekam_medis = p.nomor_rekam_medis
        JOIN dokter d ON t.kode_dokter = d.kode_dokter
        JOIN pemeriksaan pm ON t.kode_pemeriksaan = pm.kode_pemeriksaan
        ORDER BY t.kode_transaksi DESC
        """
        aksi.execute(sql)
        data = aksi.fetchall()
        aksi.close()
        return data

    def tambah_transaksi(self, tgl, kd_dokter, no_rm, kd_pemeriksaan):
        aksi = self.koneksi.cursor()
        sql = """
        INSERT INTO transaksi
        (tanggal_pemeriksaan, kode_dokter, nomor_rekam_medis, kode_pemeriksaan)
        VALUES (%s, %s, %s, %s)
        """
        try:
            aksi.execute(sql, (tgl, kd_dokter, no_rm, kd_pemeriksaan))
            self.koneksi.commit()
            return True, "Data Transaksi berhasil disimpan!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menyimpan data Transaksi: {err}"
        finally:
            aksi.close()

    def ubah_transaksi(self, kode_transaksi, tgl, kd_dokter, no_rm, kd_pemeriksaan):
        aksi = self.koneksi.cursor()
        sql = "UPDATE transaksi SET tanggal_pemeriksaan = %s, kode_dokter = %s, nomor_rekam_medis = %s, kode_pemeriksaan = %s " \
              "WHERE kode_transaksi = %s"
        try:
            aksi.execute(sql, (tgl, kd_dokter, no_rm, kd_pemeriksaan, kode_transaksi))
            self.koneksi.commit()
            return True, "Data Transaksi berhasil diubah!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal mengubah data Transaksi: {err}"
        finally:
            aksi.close()

    def hapus_transaksi(self, kode_transaksi):
        aksi = self.koneksi.cursor()
        sql = "DELETE FROM transaksi WHERE kode_transaksi = %s"
        try:
            aksi.execute(sql, (kode_transaksi,))
            self.koneksi.commit()
            return True, "Data Transaksi berhasil dihapus!"
        except mysql.connector.Error as err:
            self.koneksi.rollback()
            return False, f"Gagal menghapus data Transaksi: {err}"
        finally:
            aksi.close()
