# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pemeriksaan.ui'
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
        Form.resize(400, 300)
        self.formLayoutWidget = QWidget(Form)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(80, 10, 281, 281))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.kodePemeriksaanLabel = QLabel(self.formLayoutWidget)
        self.kodePemeriksaanLabel.setObjectName(u"kodePemeriksaanLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.kodePemeriksaanLabel)

        self.kodePemeriksaanLineEdit = QLineEdit(self.formLayoutWidget)
        self.kodePemeriksaanLineEdit.setObjectName(u"kodePemeriksaanLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.kodePemeriksaanLineEdit)

        self.jenisPemeriksaanLabel = QLabel(self.formLayoutWidget)
        self.jenisPemeriksaanLabel.setObjectName(u"jenisPemeriksaanLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.jenisPemeriksaanLabel)

        self.jenisPemeriksaanLineEdit = QLineEdit(self.formLayoutWidget)
        self.jenisPemeriksaanLineEdit.setObjectName(u"jenisPemeriksaanLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.jenisPemeriksaanLineEdit)

        self.hargaLabel = QLabel(self.formLayoutWidget)
        self.hargaLabel.setObjectName(u"hargaLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.hargaLabel)

        self.hargaLineEdit = QLineEdit(self.formLayoutWidget)
        self.hargaLineEdit.setObjectName(u"hargaLineEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.hargaLineEdit)

        self.simpanButton = QPushButton(self.formLayoutWidget)
        self.simpanButton.setObjectName(u"simpanButton")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.simpanButton)

        self.ubahButton = QPushButton(self.formLayoutWidget)
        self.ubahButton.setObjectName(u"ubahButton")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.ubahButton)

        self.hapusButton = QPushButton(self.formLayoutWidget)
        self.hapusButton.setObjectName(u"hapusButton")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.hapusButton)

        self.pemeriksaanTableWidget = QTableWidget(self.formLayoutWidget)
        self.pemeriksaanTableWidget.setObjectName(u"pemeriksaanTableWidget")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.pemeriksaanTableWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.kodePemeriksaanLabel.setText(QCoreApplication.translate("Form", u"Kode Pemeriksaan", None))
        self.jenisPemeriksaanLabel.setText(QCoreApplication.translate("Form", u"Jenis Pemeriksaan", None))
        self.hargaLabel.setText(QCoreApplication.translate("Form", u"Harga", None))
        self.simpanButton.setText(QCoreApplication.translate("Form", u"SIMPAN", None))
        self.ubahButton.setText(QCoreApplication.translate("Form", u"UBAH", None))
        self.hapusButton.setText(QCoreApplication.translate("Form", u"HAPUS", None))
    # retranslateUi

