# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transaksi.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QFormLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.formLayoutWidget = QWidget(Form)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(70, 10, 261, 283))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.nomorRekamMedisLabel = QLabel(self.formLayoutWidget)
        self.nomorRekamMedisLabel.setObjectName(u"nomorRekamMedisLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.nomorRekamMedisLabel)

        self.nomorRekamMedisLineEdit = QLineEdit(self.formLayoutWidget)
        self.nomorRekamMedisLineEdit.setObjectName(u"nomorRekamMedisLineEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.nomorRekamMedisLineEdit)

        self.kodePemeriksaanLabel = QLabel(self.formLayoutWidget)
        self.kodePemeriksaanLabel.setObjectName(u"kodePemeriksaanLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.kodePemeriksaanLabel)

        self.simpanButton = QPushButton(self.formLayoutWidget)
        self.simpanButton.setObjectName(u"simpanButton")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.simpanButton)

        self.ubahButton = QPushButton(self.formLayoutWidget)
        self.ubahButton.setObjectName(u"ubahButton")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.ubahButton)

        self.hapusButton = QPushButton(self.formLayoutWidget)
        self.hapusButton.setObjectName(u"hapusButton")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.hapusButton)

        self.kodePemeriksaanLineEdit = QLineEdit(self.formLayoutWidget)
        self.kodePemeriksaanLineEdit.setObjectName(u"kodePemeriksaanLineEdit")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.kodePemeriksaanLineEdit)

        self.kodeDokterLabel = QLabel(self.formLayoutWidget)
        self.kodeDokterLabel.setObjectName(u"kodeDokterLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.kodeDokterLabel)

        self.kodeDokterLineEdit = QLineEdit(self.formLayoutWidget)
        self.kodeDokterLineEdit.setObjectName(u"kodeDokterLineEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.kodeDokterLineEdit)

        self.kodeTransaksiLabel = QLabel(self.formLayoutWidget)
        self.kodeTransaksiLabel.setObjectName(u"kodeTransaksiLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.kodeTransaksiLabel)

        self.kodeTransaksiLineEdit = QLineEdit(self.formLayoutWidget)
        self.kodeTransaksiLineEdit.setObjectName(u"kodeTransaksiLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.kodeTransaksiLineEdit)

        self.transaksiTableWidget = QTableWidget(self.formLayoutWidget)
        self.transaksiTableWidget.setObjectName(u"transaksiTableWidget")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.SpanningRole, self.transaksiTableWidget)

        self.tanggalTransaksiLabel = QLabel(self.formLayoutWidget)
        self.tanggalTransaksiLabel.setObjectName(u"tanggalTransaksiLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.tanggalTransaksiLabel)

        self.tanggalTransaksiDateEdit = QDateEdit(self.formLayoutWidget)
        self.tanggalTransaksiDateEdit.setObjectName(u"tanggalTransaksiDateEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.tanggalTransaksiDateEdit)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.nomorRekamMedisLabel.setText(QCoreApplication.translate("Form", u"Nomor Rekam Medis", None))
        self.kodePemeriksaanLabel.setText(QCoreApplication.translate("Form", u"Kode Pemeriksaan", None))
        self.simpanButton.setText(QCoreApplication.translate("Form", u"SIMPAN", None))
        self.ubahButton.setText(QCoreApplication.translate("Form", u"UBAH", None))
        self.hapusButton.setText(QCoreApplication.translate("Form", u"HAPUS", None))
        self.kodeDokterLabel.setText(QCoreApplication.translate("Form", u"Kode Dokter", None))
        self.kodeTransaksiLabel.setText(QCoreApplication.translate("Form", u"Kode Transaksi", None))
        self.tanggalTransaksiLabel.setText(QCoreApplication.translate("Form", u"Tanggal Transaksi", None))
    # retranslateUi

