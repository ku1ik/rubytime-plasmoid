# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confignotifications.ui'
#
# Created: Sun Apr 26 23:10:04 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(392, 287)
        self.formLayout = QtGui.QFormLayout(form)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.timeEdit = QtGui.QTimeEdit(form)
        self.timeEdit.setObjectName("timeEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.timeEdit)
        self.timeEdit_2 = QtGui.QTimeEdit(form)
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.timeEdit_2)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(QtGui.QApplication.translate("form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("form", "Morning check at", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("form", "Afternoon check at", None, QtGui.QApplication.UnicodeUTF8))
        self.timeEdit.setDisplayFormat(QtGui.QApplication.translate("form", "HH:mm", None, QtGui.QApplication.UnicodeUTF8))
        self.timeEdit_2.setDisplayFormat(QtGui.QApplication.translate("form", "HH:mm", None, QtGui.QApplication.UnicodeUTF8))

