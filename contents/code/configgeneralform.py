# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configgeneralform.ui'
#
# Created: Fri May  1 17:21:02 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(479, 200)
        form.setMinimumSize(QtCore.QSize(400, 200))
        self.formLayout = QtGui.QFormLayout(form)
        self.formLayout.setObjectName("formLayout")
        self.instanceURL = QtGui.QLineEdit(form)
        self.instanceURL.setMaximumSize(QtCore.QSize(230, 16777215))
        self.instanceURL.setObjectName("instanceURL")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.instanceURL)
        self.label = QtGui.QLabel(form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        self.username = QtGui.QLineEdit(form)
        self.username.setMaximumSize(QtCore.QSize(120, 16777215))
        self.username.setObjectName("username")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.username)
        self.label_3 = QtGui.QLabel(form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_3)
        self.activitiesNumber = QtGui.QSpinBox(form)
        self.activitiesNumber.setObjectName("activitiesNumber")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.activitiesNumber)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(QtGui.QApplication.translate("form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("form", "Rubytime instance URL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("form", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("form", "Number of recent activities", None, QtGui.QApplication.UnicodeUTF8))

