# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confignotifications.ui'
#
# Created: Fri May  1 14:21:50 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(468, 209)
        self.verticalLayout = QtGui.QVBoxLayout(form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtGui.QLabel(form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox = QtGui.QCheckBox(form)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.timeEdit = QtGui.QTimeEdit(form)
        self.timeEdit.setObjectName("timeEdit")
        self.gridLayout.addWidget(self.timeEdit, 0, 1, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(form)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 1, 0, 1, 1)
        self.timeEdit_2 = QtGui.QTimeEdit(form)
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.gridLayout.addWidget(self.timeEdit_2, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_4 = QtGui.QLabel(form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(QtGui.QApplication.translate("form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("form", "Rubytime plasmoid can notify you about missing activities.\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("form", "Check for yesterday\'s activity at", None, QtGui.QApplication.UnicodeUTF8))
        self.timeEdit.setDisplayFormat(QtGui.QApplication.translate("form", "HH:mm", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("form", "Check for today\'s activity at", None, QtGui.QApplication.UnicodeUTF8))
        self.timeEdit_2.setDisplayFormat(QtGui.QApplication.translate("form", "HH:mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("form", "\n"
"To configure notifications behaviour please go to the KDE \"System Settings\",\n"
"select \"Notifications\", select \"Rubytime Plasmoid\" and then modify as required.", None, QtGui.QApplication.UnicodeUTF8))

