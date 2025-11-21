# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dokter.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(431, 348)
        self.formLayoutWidget = QWidget(Form)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(20, 10, 391, 331))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.kodeDokterLabel = QLabel(self.formLayoutWidget)
        self.kodeDokterLabel.setObjectName(u"kodeDokterLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.kodeDokterLabel)

        self.kodeDokterLineEdit = QLineEdit(self.formLayoutWidget)
        self.kodeDokterLineEdit.setObjectName(u"kodeDokterLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.kodeDokterLineEdit)

        self.namaDokterLabel = QLabel(self.formLayoutWidget)
        self.namaDokterLabel.setObjectName(u"namaDokterLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.namaDokterLabel)

        self.namaDokterLineEdit = QLineEdit(self.formLayoutWidget)
        self.namaDokterLineEdit.setObjectName(u"namaDokterLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.namaDokterLineEdit)

        self.spesialisLabel = QLabel(self.formLayoutWidget)
        self.spesialisLabel.setObjectName(u"spesialisLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.spesialisLabel)

        self.spesialisLineEdit = QLineEdit(self.formLayoutWidget)
        self.spesialisLineEdit.setObjectName(u"spesialisLineEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spesialisLineEdit)

        self.simpanButton = QPushButton(self.formLayoutWidget)
        self.simpanButton.setObjectName(u"simpanButton")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.simpanButton)

        self.hapusButton = QPushButton(self.formLayoutWidget)
        self.hapusButton.setObjectName(u"hapusButton")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.hapusButton)

        self.ubahButton = QPushButton(self.formLayoutWidget)
        self.ubahButton.setObjectName(u"ubahButton")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.ubahButton)

        self.CariLabel = QLabel(self.formLayoutWidget)
        self.CariLabel.setObjectName(u"CariLabel")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.SpanningRole, self.CariLabel)

        self.cariLineEdit = QLineEdit(self.formLayoutWidget)
        self.cariLineEdit.setObjectName(u"cariLineEdit")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.SpanningRole, self.cariLineEdit)

        self.dokterTableWidget = QTableWidget(self.formLayoutWidget)
        self.dokterTableWidget.setObjectName(u"dokterTableWidget")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.SpanningRole, self.dokterTableWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.kodeDokterLabel.setText(QCoreApplication.translate("Form", u"Kode Dokter", None))
        self.namaDokterLabel.setText(QCoreApplication.translate("Form", u"Nama Dokter", None))
        self.spesialisLabel.setText(QCoreApplication.translate("Form", u"Spesialis", None))
        self.simpanButton.setText(QCoreApplication.translate("Form", u"SIMPAN", None))
        self.hapusButton.setText(QCoreApplication.translate("Form", u"HAPUS", None))
        self.ubahButton.setText(QCoreApplication.translate("Form", u"UBAH", None))
        self.CariLabel.setText(QCoreApplication.translate("Form", u"Cari Data :", None))
    # retranslateUi

