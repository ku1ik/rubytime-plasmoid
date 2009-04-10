# -*- coding: utf-8 -*-
#
#   Copyright (C) 2009 Marcin Kulik <marcin.kulik@gmail.com>
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
# from editor import Editor
import dbus
import rubytime

class RubytimeApplet(plasmascript.Applet):
  def __init__(self, parent, args = None):
    plasmascript.Applet.__init__(self, parent)

  def init(self):
    self.cfg = self.config()
    self.recentActivities = []

    # create session
    self.api = rubytime.RubytimeSession(self.cfg.readEntry('hostname', 'http://rt.llp.pl'),
                                        self.cfg.readEntry('username', 'test'), self.cfg.readEntry('password', 'test123'))

    # setup notifications proxy
    self.sessionBus = dbus.SessionBus()
    self.notificationsProxy = self.sessionBus.get_object('org.kde.VisualNotifications', '/VisualNotifications')

    # no config
    self.setHasConfigurationInterface(False)
    self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

    # setup ui
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
#    KColorScheme(QPalette.Active, KColorScheme.View, Plasma.Theme.defaultTheme().colorScheme())

    # main vertical layout
    QGraphicsLinearLayout(Qt.Vertical, self.applet)
    self.layout().setSpacing(3)

    # header (logo)
    headerLayout = QGraphicsLinearLayout(Qt.Horizontal)
    headerLayout.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    headerLayout.setPreferredSize(300, 25)
    headerLayout.setMinimumSize(200, 25)
    qicon = QIcon("contents/logo-small.png")
    # qicon.resize(111, 25)
    icon = KIcon(qicon)
    #iconWidget = QGraphicsProxyWidget()
    #iconWidget.setWidget(QGraphicsWidget(icon))
    # icon.resize(111, 25)
    iconWidget = Plasma.IconWidget(icon, "", self.applet)
    iconWidget.setPreferredSize(111, 25)
    iconWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    label1 = Plasma.Label(self.applet)
    label1.setText('<html><b>New activity</b></html>')
    headerLayout.addItem(label1)
    headerLayout.addItem(iconWidget)
    self.layout().addItem(headerLayout)
    
    # new activity form

    newActivityFrame = Plasma.Frame(self.applet)
    newActivityLayout = QGraphicsLinearLayout(Qt.Vertical, newActivityFrame)

    # project name
    projectNameLayout = QGraphicsLinearLayout(Qt.Horizontal, newActivityLayout)
    label = Plasma.Label(self.applet)
    label.setText('<html><b>Project</b></html>')
    label.setPreferredSize(60, 0)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
    projectNameLayout.addItem(label)
    projectNameCombo = Plasma.ComboBox(newActivityFrame)
    projectNameCombo.addItem('Cayox')
    projectNameCombo.addItem('UK Wells')
    projectNameLayout.addItem(projectNameCombo)
    newActivityLayout.addItem(projectNameLayout)

    # activity date
    dateLayout = QGraphicsLinearLayout(Qt.Horizontal, newActivityLayout)
    label = Plasma.Label(self.applet)
    label.setText('<html><b>Date</b></html>')
    label.setPreferredSize(60, 0)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
    dateLayout.addItem(label)
    date = QDateEdit()
    dateWidget = QGraphicsProxyWidget(newActivityFrame)
    dateWidget.setWidget(date)
    dateLayout.addItem(dateWidget)
    newActivityLayout.addItem(dateLayout)

    # hours worked
    hoursLayout = QGraphicsLinearLayout(Qt.Horizontal, newActivityLayout)
    label = Plasma.Label(self.applet)
    label.setText('<html><b>Hours</b></html>')
    label.setPreferredSize(60, 0)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
    hoursLayout.addItem(label)
    hours = Plasma.LineEdit(newActivityFrame)
    hoursLayout.addItem(hours)
    newActivityLayout.addItem(hoursLayout)

    description = Plasma.TextEdit(newActivityFrame)
    newActivityLayout.addItem(description)
    sendButton = Plasma.PushButton(newActivityFrame)
    sendButton.setText('Add!')
    newActivityLayout.addItem(sendButton)
    newActivityFrame.setFrameShadow(Plasma.Frame.Sunken)
    self.layout().addItem(newActivityFrame)


    # recent activities
    label2 = Plasma.Label(self.applet)
    label2.setText('<html><b>Recent activities</b></html>')
    self.layout().addItem(label2)

    for i in xrange(3):
      frame = Plasma.Frame(self.applet)
      frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
      layout = QGraphicsLinearLayout(Qt.Vertical, frame)
      label = Plasma.Label(self.applet)
      label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
      label.setText('<html><b>Abcdef 123</b><br/>Lal la lal</html>')
      layout.addItem(label)
      self.layout().addItem(frame)

#    flashLayout = QGraphicsLinearLayout(Qt.Horizontal, self)
#    self.label = Plasma.FlashingLabel()#self)
#    self.label.setAutohide(True)
#    self.label.setMinimumSize(0, 20)
#    self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    
    
#    self.setContentsMargins(0, 0, 0, 0)
#    self.layout().setContentsMargins(0, 0, 0, 0)
#    self.icon = Plasma.IconWidget(KIcon("folder-red"), "", self.applet)
#    self.layout().addItem(self.icon)
    #self.resize( self.icon.iconSize() )
    #self.setAcceptDrops(True)
#    self.entries = []
    #gc = self.config()
    #(count, bummer) = gc.readEntry("count", QVariant(0) ).toInt()
    #if count > 0:
    #	default = QStringList("*")
    #	default.append( os.path.expanduser("~") )
    #	default.append("True")
    #	default.append("False")
    #	for i in range(0, count):
    #		lst = gc.readXdgListEntry("_" + str(i), default)
    #		lst.append("")
    #		wildcard = True
    #		if lst[2] == "False":
    #			wildcard = False
    #		case = False
    #		if lst[3] == "True":
    #			case = True
    #		self.entries.append( [lst[0], lst[1], wildcard, case] )
#    self.connect(self.icon, SIGNAL("clicked()"), self.notifyMe)
    # self.resize(128, 128)

    # initial activities fetch
    self.initialTimer = QTimer(self)
    self.connect(self.initialTimer, SIGNAL("timeout()"), self.initialActivitiesFetch)
    self.initialTimer.start(2 * 1000)

    # setup activities updates
    self.updateTimer = QTimer(self)
    self.connect(self.updateTimer, SIGNAL("timeout()"), self.updateActivities)
    self.updateTimer.start(10 * 60 * 1000)

    # setup morning notifications
    self.morningTimer = QTimer(self)
    self.connect(self.morningTimer, SIGNAL("timeout()"), self.morningCheck)
    self.morningTimer.start(10 * 1000)

    # setup afternoon notifications
    self.afternoonTimer = QTimer(self)
    self.connect(self.afternoonTimer, SIGNAL("timeout()"), self.afternoonCheck)
    self.afternoonTimer.start(20 * 1000)
    pass

  def contextualActions(self):
    return []

  def paintInterface(self, painter, option, rect):
    pass

  def constraintsEvent(self, constraints):
    pass

  def initialActivitiesFetch(self):
    self.initialTimer.stop()
    print self.api.getActivities()
    pass

  def updateActivities(self):
    print self.api.getActivities()
    pass

  def morningCheck(self):
    self.morningTimer.stop()
    self.sendNotification("<html><b>Morning!</b><br/>Did you fill Rubytime for yesterday?</html>")
    pass

  def afternoonCheck(self):
    self.afternoonTimer.stop()
    self.sendNotification("<html><b>Good afternoon!</b><br/>Don't forget to add today's activities to Rubytime.</html>")
    pass

  #def createConfigurationInterface(self, parent):
  #	self.editor = Editor(self.entries)
  #	p = parent.addPage(self.editor, ki18n("Rules").toString() )
  #	p.setIcon( KIcon("view-filter") )
  #	self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
  #	self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)
  #	pass

  #def showConfigurationInterface(self):
  #	dialog = KPageDialog()
  #	dialog.setFaceType(KPageDialog.List)
  #	dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
  #	self.createConfigurationInterface(dialog)
  #	dialog.exec_()
  
  def notifyMe(self):
    self.sendNotification('Icon clicked, yay!')
    pass

  def sendNotification(self, body):
#    self.notificationsProxy.Notify('rubytime-plasmoid', 0, "someid", 'folder-red', 'Rubytime', body, [], [], 2000, dbus_interface='org.kde.VisualNotifications')
    #self.notifications.Notify('rubytime-plasmoid', 0, str(random.random() * 10), 'folder-red', 'Rubytime', body, [], [], 0, dbus_interface='org.kde.VisualNotifications')
    pass

  def mousePressEvent(self, event):
    pass

  def configAccepted(self):
    self.entries = self.editor.exportList()
    gc = self.config()
    gc.writeEntry("count", QVariant( len(self.entries) ) )
    counter = 0
    for entry in self.entries:
      print entry

      lst = QStringList( entry[0] )
      lst.append( entry[1] )

      if entry[2]:
        a = "True"
      else:
        a = "False"
      lst.append(a)

      if entry[3]:
        a = "True"
      else:
        a = "False"
      lst.append(a)

      gc.writeXdgListEntry("_" + str(counter), lst)
      counter += 1
    self.configDenied()

  def configDenied(self):
    self.editor.deleteLater()

  def shouldConserveResources(self):
    return True

  def dragEnterEvent(self, e):
    e.accept()

  def dropEvent(self, e):
    t = e.mimeData().text().split("\n")
    for src in t:
      if src.isEmpty():
        continue
      dest = ""
      for entry in self.entries:
        format = QRegExp.RegExp2
        if entry[2]:
          format = QRegExp.Wildcard
        regex = QRegExp(entry[0], Qt.CaseSensitive, format)
        if not regex.isValid():
          continue
        if regex.indexIn(src) > -1:
          dest = entry[1]
          break
      if QString(dest).isEmpty():
        continue
      KIO.move( KUrl(src), KUrl(dest) )


def CreateApplet(parent):
  return RubytimeApplet(parent)

