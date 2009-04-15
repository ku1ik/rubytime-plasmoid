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
import os
import sys
sys.path.append(os.path.dirname(__file__))
import rubytime
#import workers


class RubytimeApplet(plasmascript.Applet):
  def __init__(self, parent, args = None):
    plasmascript.Applet.__init__(self, parent)

  def init(self):
    self.cfg = self.config()
    self.recentActivities = []

    # create session
    self.api = rubytime.RubytimeSession(str(self.cfg.readEntry('hostname', 'http://localhost:4000')),
                                        str(self.cfg.readEntry('username', 'dev1')),
                                        str(self.cfg.readEntry('password', 'password')), self)

    # setup notifications proxy
    self.sessionBus = dbus.SessionBus()
    self.notificationsProxy = self.sessionBus.get_object('org.kde.VisualNotifications', '/VisualNotifications')

    # no config
    self.setHasConfigurationInterface(False)
    self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
    self.theme = Plasma.Svg(self)
    self.theme.setImagePath("widgets/background")
    self.setBackgroundHints(Plasma.Applet.DefaultBackground)

    # build layout
    self.createLayout()

    # setup timers
#    self.setupTimers()
    
    self.initialFetch()


  def createLayout(self):
    # setup ui
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
#    self.setPreferredSize(300, 500)
    self.setMinimumSize(250, 400)
#    KColorScheme(QPalette.Active, KColorScheme.View, Plasma.Theme.defaultTheme().colorScheme())

    # main vertical layout
    self.layout = QGraphicsLinearLayout(Qt.Vertical)
    self.layout.setSpacing(3)

    # header (flash + logo)
    headerLayout = QGraphicsLinearLayout(Qt.Horizontal)
#    headerLayout.setPreferredSize(300, 25)
    headerLayout.setMinimumSize(200, 25)
#    headerLayout.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    qicon = QIcon("contents/logo-small.png")
    # qicon.resize(111, 25)
    icon = KIcon(qicon)
    #iconWidget = QGraphicsProxyWidget()
    #iconWidget.setWidget(QGraphicsWidget(icon))
    # icon.resize(111, 25)
    label = Plasma.Label()
    label.setText("...")
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
    headerLayout.addItem(label)
    iconWidget = Plasma.IconWidget(icon, "")
    iconWidget.setPreferredSize(111, 25)
    iconWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    headerLayout.addItem(iconWidget)
    self.layout.addItem(headerLayout)

    # new activity label

    label = Plasma.Label()
    label.setText('<html><b>New activity</b></html>')
    self.layout.addItem(label)

#    a = QGraphicsWidget()
#    b = QGraphicsLinearLayout(Qt.Vertical, a)
#    b.addItem(Plasma.BusyWidget())
#    layout.addItem(a)
    # new activity form

    newActivityFrame = Plasma.Frame()
    newActivityFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    newActivityLayout = QGraphicsLinearLayout(Qt.Vertical, newActivityFrame)
#    newActivityLayout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    # project name
    projectNameLayout = QGraphicsLinearLayout(Qt.Horizontal)
#    grid = QGraphicsGridLayout()
    label = Plasma.Label()
    label.setText('<html><b>Project</b></html>')
    label.setPreferredSize(60, 0)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
    projectNameLayout.addItem(label)
#    grid.addItem(label, 0, 0)
#    projectNameLayout.setAlignment(label, Qt.AlignRight)
    projectNameCombo = Plasma.ComboBox()
    projectNameCombo.addItem('Cayox')
    projectNameCombo.addItem('UK Wells')
    projectNameLayout.addItem(projectNameCombo)
#    grid.addItem(projectNameCombo, 0, 1)
    newActivityLayout.addItem(projectNameLayout)
#    newActivityLayout.addItem(grid)

    # activity date
    dateLayout = QGraphicsLinearLayout(Qt.Horizontal)
    label = Plasma.Label()
    label.setText('<html><b>Date</b></html>')
    label.setPreferredSize(60, 0)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
    dateLayout.addItem(label)
    date = KDateWidget() #QDateEdit()
    dateWidget = QGraphicsProxyWidget()
    dateWidget.setWidget(date)
    dateLayout.addItem(dateWidget)
    newActivityLayout.addItem(dateLayout)

    # hours worked
    hoursLayout = QGraphicsLinearLayout(Qt.Horizontal)
    label = Plasma.Label()
    label.setText('<html><b>Hours</b></html>')
    label.setPreferredSize(60, 0)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
    hoursLayout.addItem(label)
    hours = Plasma.LineEdit()
    hoursLayout.addItem(hours)
    newActivityLayout.addItem(hoursLayout)

    description = Plasma.TextEdit()
    newActivityLayout.addItem(description)

    # button
    sendButton = Plasma.PushButton()
    sendButton.setText('Add!')
    newActivityLayout.addItem(sendButton)
    newActivityFrame.setFrameShadow(Plasma.Frame.Sunken)
    self.layout.addItem(newActivityFrame)
    self.connect(sendButton, SIGNAL("clicked()"), self.addActivity)



    # recent activities

    label = Plasma.Label()
    label.setText('<html><b>Recent activities</b></html>')
#    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
#    label.setContentsMargins(50, 50, 50, 50)
    self.layout.addItem(label)

#    activities = QGraphicsWidget()
#    activities.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

#    recentLayout = QGraphicsLinearLayout(Qt.Vertical, activities)
#    recentLayout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #recentLayout.setContentsMargins(0, 0, 0, 0)

    for i in xrange(3):
      frame = Plasma.Frame()
#      frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
      frameLayout = QGraphicsLinearLayout(Qt.Vertical, frame)
      label = Plasma.Label()
#      label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
      label.setText('<html><b>Friday, 10 April - Cayox, 8h</b><br/>- implemented something<br/>- updated demo server</html>')
      self.label = label
      frameLayout.addItem(label)
      self.layout.addItem(frame)

#    scrollWidget = Plasma.ScrollWidget()
#    scrollWidget.setWidget(activities)
#    layout.addItem(activities)

    self.setLayout(self.layout)
#    self.resize(250, 300)

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
    # self.resize(128, 128)
    pass

  def setupTimers(self):
    # initial activities fetch
    self.initialTimer = QTimer(self)
    self.connect(self.initialTimer, SIGNAL("timeout()"), self.initialFetch)
    self.initialTimer.setSingleShot(True)
    self.initialTimer.start(1 * 1000)

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

  def contextualActions(self):
    return []

#  def paintInterface(self, painter, option, rect):
#    pass

#  def constraintsEvent(self, constraints):
#    pass

  def initialFetch(self):
    self.updateActivities()
    self.updateProjects()

  def setActivities(self, activities):
    pass

  def updateActivities(self):
    self.applet.setBusy(True)
#    self.updateActivitiesThread = workers.ActivitiesWorker(self)
#    self.connect(self.updateActivitiesThread, SIGNAL("finished()"), self.workerFinished)
#    self.connect(self.updateActivitiesThread, SIGNAL("terminated()"), self.workerFinished)
#    self.updateActivitiesThread.start()
    self.api.getActivities()

  def updateProjects(self):
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
  
  def addActivity(self):
#    self.applet.setBusy(True)
#    self.addActivityThread = workers.AddActivityWorker(self, { 'project_id': 1, 'date': '2009-04-13', 'hours': '', 'comments': '' })
#    self.connect(self.addActivityThread, SIGNAL("finished()"), self.workerFinished)
#    self.connect(self.addActivityThread, SIGNAL("terminated()"), self.workerFinished)
#    self.addActivityThread.start()
    pass

  def workerFinished(self):
    self.applet.setBusy(False)
#    self.updateActivitiesThread = None

  def sendNotification(self, body):
#    self.notificationsProxy.Notify('rubytime-plasmoid', 0, "someid", 'folder-red', 'Rubytime', body, [], [], 2000, dbus_interface='org.kde.VisualNotifications')
    #self.notifications.Notify('rubytime-plasmoid', 0, str(random.random() * 10), 'folder-red', 'Rubytime', body, [], [], 0, dbus_interface='org.kde.VisualNotifications')
    pass

#  def mousePressEvent(self, event):
#    pass

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

#  def dragEnterEvent(self, e):
#    e.accept()
#
#  def dropEvent(self, e):
#    t = e.mimeData().text().split("\n")
#    for src in t:
#      if src.isEmpty():
#        continue
#      dest = ""
#      for entry in self.entries:
#        format = QRegExp.RegExp2
#        if entry[2]:
#          format = QRegExp.Wildcard
#        regex = QRegExp(entry[0], Qt.CaseSensitive, format)
#        if not regex.isValid():
#          continue
#        if regex.indexIn(src) > -1:
#          dest = entry[1]
#          break
#      if QString(dest).isEmpty():
#        continue
#      KIO.move( KUrl(src), KUrl(dest) )


def CreateApplet(parent):
  return RubytimeApplet(parent)

