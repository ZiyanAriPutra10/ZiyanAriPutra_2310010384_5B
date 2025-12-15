# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_Main(object):
    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName(u"Main")
        Main.resize(800, 600)
        self.actionDATA_PASIEN = QAction(Main)
        self.actionDATA_PASIEN.setObjectName(u"actionDATA_PASIEN")
        self.actionDATA_DOKTER = QAction(Main)
        self.actionDATA_DOKTER.setObjectName(u"actionDATA_DOKTER")
        self.actionDATA_PEMERIKSAAN = QAction(Main)
        self.actionDATA_PEMERIKSAAN.setObjectName(u"actionDATA_PEMERIKSAAN")
        self.actionDATA_TRANSAKSI = QAction(Main)
        self.actionDATA_TRANSAKSI.setObjectName(u"actionDATA_TRANSAKSI")
        self.centralwidget = QWidget(Main)
        self.centralwidget.setObjectName(u"centralwidget")
        Main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuHALAMAN_UTAMA = QMenu(self.menubar)
        self.menuHALAMAN_UTAMA.setObjectName(u"menuHALAMAN_UTAMA")
        Main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Main)
        self.statusbar.setObjectName(u"statusbar")
        Main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHALAMAN_UTAMA.menuAction())
        self.menuHALAMAN_UTAMA.addAction(self.actionDATA_PASIEN)
        self.menuHALAMAN_UTAMA.addAction(self.actionDATA_DOKTER)
        self.menuHALAMAN_UTAMA.addAction(self.actionDATA_PEMERIKSAAN)
        self.menuHALAMAN_UTAMA.addAction(self.actionDATA_TRANSAKSI)

        self.retranslateUi(Main)

        QMetaObject.connectSlotsByName(Main)
    # setupUi

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", u"Main", None))
        self.actionDATA_PASIEN.setText(QCoreApplication.translate("Main", u"DATA PASIEN", None))
        self.actionDATA_DOKTER.setText(QCoreApplication.translate("Main", u"DATA DOKTER", None))
        self.actionDATA_PEMERIKSAAN.setText(QCoreApplication.translate("Main", u"DATA PEMERIKSAAN", None))
        self.actionDATA_TRANSAKSI.setText(QCoreApplication.translate("Main", u"DATA TRANSAKSI", None))
        self.menuHALAMAN_UTAMA.setTitle(QCoreApplication.translate("Main", u"HALAMAN UTAMA", None))
    # retranslateUi

