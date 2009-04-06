# -*- coding: utf-8 -*-
#
#   Copyright (C) 2009 Benjamin Kleiner <bizzl@user.sourceforge.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 2,
#   or (at your option) any later version, as published by the Free
#   Software Foundation
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import os
#from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4 import kdecore, kdeui, kio

class Editor(QWidget):
	def __init__(self, entries = None):
		QWidget.__init__(self)
		if entries == None:
			entries = []
		#self.entries = entries

		# Pretty much the stuff you would get from pyuic for editor.ui
		self.verticalLayout_2 = QVBoxLayout(self)
		self.horizontalLayout = QHBoxLayout()
		self.lstMain = QListWidget(self)
		self.horizontalLayout.addWidget(self.lstMain)
		self.widget_2 = QWidget(self)
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
		self.widget_2.setSizePolicy(sizePolicy)
		self.verticalLayout = QVBoxLayout(self.widget_2)
		self.btnDelete = QPushButton(self.widget_2)
		self.btnDelete.setEnabled(False)
		self.verticalLayout.addWidget(self.btnDelete)
		self.btnNew = QPushButton(self.widget_2)
		self.verticalLayout.addWidget(self.btnNew)
		self.btnUp = QPushButton(self.widget_2)
		self.btnUp.setEnabled(False)
		self.verticalLayout.addWidget(self.btnUp)
		self.btnDown = QPushButton(self.widget_2)
		self.btnDown.setEnabled(False)
		self.verticalLayout.addWidget(self.btnDown)
		spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem)
		self.horizontalLayout.addWidget(self.widget_2)
		self.verticalLayout_2.addLayout(self.horizontalLayout)
		self.widget = QWidget(self)
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
		self.widget.setSizePolicy(sizePolicy)
		self.formLayout = QFormLayout(self.widget)
		self.lblRegex = QLabel(self.widget)
		self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblRegex)
		self.edtRegex = QLineEdit(self.widget)
		self.formLayout.setWidget(1, QFormLayout.FieldRole, self.edtRegex)
		self.lblDestiny = QLabel(self.widget)
		self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblDestiny)
		self.edtDestiny = kio.KUrlRequester(self.widget)
		self.edtDestiny.fileDialog().setMode(kio.KFile.Directory)
		self.formLayout.setWidget(2, QFormLayout.FieldRole, self.edtDestiny)
		self.chbIsWildcard = QCheckBox(self.widget)
		self.formLayout.setWidget(3, QFormLayout.FieldRole, self.chbIsWildcard)
		self.chbIsCaseSensitive = QCheckBox(self.widget)
		self.formLayout.setWidget(4, QFormLayout.FieldRole, self.chbIsCaseSensitive)
		self.verticalLayout_2.addWidget(self.widget)
		self.lblRegex.setBuddy(self.edtRegex)
		self.lblDestiny.setBuddy(self.edtDestiny)

		self.retranslateUi()

		for a in entries:
			item = QListWidgetItem( a[0] + ": " + a[1] )
			item.setData(32, QVariant(a[0]) )
			item.setData(33, QVariant(a[1]) )
			item.setData(34, QVariant(a[2]) )
			item.setData(35, QVariant(a[3]) )
			self.lstMain.addItem(item)

		self.connect(self.edtDestiny, SIGNAL("textChanged(QString)"), self.destinyChanged)
		self.connect(self.edtRegex, SIGNAL("textChanged(QString)"), self.regexChanged)
		self.connect(self.lstMain, SIGNAL("itemSelectionChanged()"), self.selectionChanged)
		self.connect(self.chbIsWildcard, SIGNAL("stateChanged(int)"), self.checkboxStateChanged)
		self.connect(self.chbIsCaseSensitive, SIGNAL("stateChanged(int)"), self.checkboxStateChanged)
		self.connect(self.btnDelete, SIGNAL("clicked(bool)"), self.deleteClicked)
		self.connect(self.btnUp, SIGNAL("clicked(bool)"), self.upClicked)
		self.connect(self.btnDown, SIGNAL("clicked(bool)"), self.downClicked)
		self.connect(self.btnNew, SIGNAL("clicked(bool)"), self.newClicked)
		
		self.changingFlag = False

	@pyqtSignature("bool")
	def newClicked(self, b):
		self.lstMain.addItem("*: " + os.path.expanduser("~") )
		item = self.lstMain.item(self.lstMain.count() - 1)
		item.setData(32, QVariant("*") )
		item.setData(33, QVariant( os.path.expanduser("~") ) )
		item.setData(34, QVariant(True) )
		item.setData(35, QVariant(False) )
		self.lstMain.setCurrentItem(item)

	@pyqtSignature("bool")
	def upClicked(self, b):
		row = self.lstMain.currentRow()
		item = self.lstMain.takeItem(row)
		self.lstMain.insertItem(row - 1, item)
		self.lstMain.setCurrentItem(item)

	@pyqtSignature("bool")
	def downClicked(self, b):
		row = self.lstMain.currentRow()
		item = self.lstMain.takeItem(row)
		self.lstMain.insertItem(row + 1, item)
		self.lstMain.setCurrentItem(item)
		
	@pyqtSignature("bool")
	def deleteClicked(self, b):
		self.lstMain.takeItem( self.lstMain.currentRow() )
		if self.lstMain.count() == 0:
			self.btnDelete.setEnabled(False)
			self.btnDown.setEnabled(False)
			self.btnUp.setEnabled(False)

	def selectionChanged(self):
		if self.lstMain.currentItem() != None:
			self.changingFlag = True
			self.edtDestiny.lineEdit().setText( self.lstMain.currentItem().data(33).toString() )
			self.edtRegex.setText( self.lstMain.currentItem().data(32).toString() )
			self.chbIsWildcard.setChecked( self.lstMain.currentItem().data(34).toBool() )
			self.chbIsCaseSensitive.setChecked( self.lstMain.currentItem().data(35).toBool() )
			self.btnDelete.setEnabled(True)
			self.btnUp.setEnabled(self.lstMain.currentRow() > 0)
			self.btnDown.setEnabled(self.lstMain.currentRow() < self.lstMain.count() - 1)
			self.changingFlag = False

	@pyqtSignature("int")
	def checkboxStateChanged(self, i):
		if not self.changingFlag and not self.lstMain.currentItem() == None:
			self.lstMain.currentItem().setData(34, QVariant(self.chbIsWildcard.checkState() == Qt.Checked) )
			self.lstMain.currentItem().setData(35, QVariant(self.chbIsCaseSensitive.checkState() == Qt.Checked) )

	@pyqtSignature("QString")
	def regexChanged(self, string):
		if not self.changingFlag and not self.lstMain.currentItem() == None:
			self.lstMain.currentItem().setData(32, QVariant(string) )
			self.updateList()

	@pyqtSignature("QString")
	def destinyChanged(self, url):
		if not self.changingFlag and not self.lstMain.currentItem() == None:
			if QFile.exists(url):
				self.lstMain.currentItem().setData(33, QVariant(url) )
				self.updateList()

	def updateList(self):
		a = self.lstMain.currentItem().data(32).toString()
		b = self.lstMain.currentItem().data(33).toString()
		self.lstMain.currentItem().setText(a + ": " + b)

	def retranslateUi(self):
		self.btnDelete.setText( kdecore.ki18n("Delete").toString() )
		self.btnNew.setText( kdecore.ki18n("New").toString() )
		self.btnUp.setText( kdecore.ki18n("Up").toString() )
		self.btnDown.setText( kdecore.ki18n("Down").toString() )
		self.lblRegex.setText( kdecore.ki18n("Regex").toString() )
		self.lblDestiny.setText( kdecore.ki18n("Destiny").toString() )
		self.chbIsWildcard.setText( kdecore.ki18n("Wildcard").toString() )
		self.chbIsCaseSensitive.setText( kdecore.ki18n("Case Sensitive").toString() )

	def exportList(self):
		result = []
		for i in range(0, self.lstMain.count() ):
			item = self.lstMain.item(i)
			regex = item.data(32).toString().__str__()
			destiny = item.data(33).toString().__str__()
			wildcard = item.data(34).toBool()
			case = item.data(35).toBool()
			result.append( [regex, destiny, wildcard, case] )
		return result
		