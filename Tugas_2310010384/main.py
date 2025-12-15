# main.py (KODE LENGKAP)
# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

# Pastikan semua file ini ada:
from Pasien import Pasien
from Dokter import Dokter
from Transaksi import Transaksi
from Pemeriksaan import Pemeriksaan

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        filenya = QFile('form.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formutama = muatfile.load(filenya,self)
        self.resize(self.formutama.size())
        self.setMenuBar(self.formutama.menuBar())

        self.formutama.actionDATA_PASIEN.triggered.connect(self.bukapasien)
        self.formutama.actionDATA_DOKTER.triggered.connect(self.bukadokter)
        self.formutama.actionDATA_TRANSAKSI.triggered.connect(self.bukatransaksi)
        self.formutama.actionDATA_PEMERIKSAAN.triggered.connect(self.bukapemeriksaan)

    def bukapasien(self):
        self.formPas = Pasien()
        self.formPas.show()

    def bukadokter(self):
        self.formDok = Dokter()
        self.formDok.show()

    def bukatransaksi(self):
        self.formTransaksi = Transaksi()
        self.formTransaksi.show()

    def bukapemeriksaan(self):
        self.formPemeriksaan = Pemeriksaan()
        self.formPemeriksaan.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jendela = MainWindow()
    jendela.show()
    sys.exit(app.exec())
