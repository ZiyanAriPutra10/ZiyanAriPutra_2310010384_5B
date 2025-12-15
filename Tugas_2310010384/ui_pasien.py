# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pasien.ui'
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
        Form.resize(500, 430)
        self.formLayoutWidget = QWidget(Form)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(50, 10, 391, 411))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.nomoRekamMedisLabel = QLabel(self.formLayoutWidget)
        self.nomoRekamMedisLabel.setObjectName(u"nomoRekamMedisLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.nomoRekamMedisLabel)

        self.nomoRekamMedisLineEdit = QLineEdit(self.formLayoutWidget)
        self.nomoRekamMedisLineEdit.setObjectName(u"nomoRekamMedisLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.nomoRekamMedisLineEdit)

        self.namaPasienLabel = QLabel(self.formLayoutWidget)
        self.namaPasienLabel.setObjectName(u"namaPasienLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.namaPasienLabel)

        self.namaPasienLineEdit = QLineEdit(self.formLayoutWidget)
        self.namaPasienLineEdit.setObjectName(u"namaPasienLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.namaPasienLineEdit)

        self.tanggaLahirLabel = QLabel(self.formLayoutWidget)
        self.tanggaLahirLabel.setObjectName(u"tanggaLahirLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.tanggaLahirLabel)

        self.tanggalLahirDateEdit = QDateEdit(self.formLayoutWidget)
        self.tanggalLahirDateEdit.setObjectName(u"tanggalLahirDateEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.tanggalLahirDateEdit)

        self.jenisKelaminLabel = QLabel(self.formLayoutWidget)
        self.jenisKelaminLabel.setObjectName(u"jenisKelaminLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.jenisKelaminLabel)

        self.jenisKelaminLineEdit = QLineEdit(self.formLayoutWidget)
        self.jenisKelaminLineEdit.setObjectName(u"jenisKelaminLineEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.jenisKelaminLineEdit)

        self.agamaLabel = QLabel(self.formLayoutWidget)
        self.agamaLabel.setObjectName(u"agamaLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.agamaLabel)

        self.agamaLineEdit = QLineEdit(self.formLayoutWidget)
        self.agamaLineEdit.setObjectName(u"agamaLineEdit")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.agamaLineEdit)

        self.ubahButton = QPushButton(self.formLayoutWidget)
        self.ubahButton.setObjectName(u"ubahButton")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.ubahButton)

        self.hapusButton = QPushButton(self.formLayoutWidget)
        self.hapusButton.setObjectName(u"hapusButton")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.hapusButton)

        self.pasienTableWidget = QTableWidget(self.formLayoutWidget)
        self.pasienTableWidget.setObjectName(u"pasienTableWidget")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.SpanningRole, self.pasienTableWidget)

        self.cariLineEdit = QLineEdit(self.formLayoutWidget)
        self.cariLineEdit.setObjectName(u"cariLineEdit")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.SpanningRole, self.cariLineEdit)

        self.CariLabel = QLabel(self.formLayoutWidget)
        self.CariLabel.setObjectName(u"CariLabel")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.CariLabel)

        self.simpanButton = QPushButton(self.formLayoutWidget)
        self.simpanButton.setObjectName(u"simpanButton")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.simpanButton)

        self.cetakButton = QPushButton(self.formLayoutWidget)
        self.cetakButton.setObjectName(u"cetakButton")

        self.formLayout.setWidget(12, QFormLayout.ItemRole.LabelRole, self.cetakButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.nomoRekamMedisLabel.setText(QCoreApplication.translate("Form", u"Nomor Rekam Medis", None))
        self.namaPasienLabel.setText(QCoreApplication.translate("Form", u"Nama Pasien ", None))
        self.tanggaLahirLabel.setText(QCoreApplication.translate("Form", u"Tanggal Lahir", None))
        self.jenisKelaminLabel.setText(QCoreApplication.translate("Form", u"Jenis Kelamin", None))
        self.agamaLabel.setText(QCoreApplication.translate("Form", u"Agama", None))
        self.ubahButton.setText(QCoreApplication.translate("Form", u"UBAH", None))
        self.hapusButton.setText(QCoreApplication.translate("Form", u"HAPUS", None))
        self.CariLabel.setText(QCoreApplication.translate("Form", u"Cari Data :", None))
        self.simpanButton.setText(QCoreApplication.translate("Form", u"SIMPAN", None))
        self.cetakButton.setText(QCoreApplication.translate("Form", u"CETAK", None))
    # retranslateUi

