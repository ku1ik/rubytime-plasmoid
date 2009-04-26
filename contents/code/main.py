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
import dbus
import os
import sys
import datetime
import urllib
sys.path.append(os.path.dirname(__file__))
import simplejson
from widgets import *
import configgeneral
import confignotifications
from config import RubytimeConfig


class RubytimeApplet(plasmascript.Applet):
  def __init__(self, parent, args = None):
    plasmascript.Applet.__init__(self, parent)

  def init(self):
    self.cfg = RubytimeConfig(self.config())

    self.activities = []
    self.activitiesLabels = []
    self.projects = {}

    # setup notifications proxy
    self.sessionBus = dbus.SessionBus()
    self.notificationsProxy = self.sessionBus.get_object('org.kde.VisualNotifications', '/VisualNotifications')

    self.setHasConfigurationInterface(True) # it doesn't matter however
    self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
    self.theme = Plasma.Svg(self)
    self.theme.setImagePath("widgets/background")
    self.setBackgroundHints(Plasma.Applet.DefaultBackground)

    # build layout
    self.createLayout()

    # setup activities updates
    self.updateTimer = QTimer(self)
    self.connect(self.updateTimer, SIGNAL("timeout()"), self.fetchProjects)
    
    # conditionaly enable widget and timers
    self.resetWidget(self.cfg.isValid())


  def resetWidget(self, isEnabled):
    self.setConfigurationRequired(not isEnabled, "")
    self.updateTimer.stop()
    if isEnabled:
      self.fetchProjects()
      self.updateTimer.start(10 * 60 * 1000)

    # setup timers
#    self.setupTimers()

    # initial fetch
  

  def createLayout(self):
    # setup ui
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    self.setPreferredSize(350, 500)
    self.setMinimumSize(330, 420)


    # main vertical layout
    self.layout = QGraphicsLinearLayout(Qt.Vertical)
    self.layout.setSpacing(3)

    # header (flash + logo)
    headerLayout = QGraphicsLinearLayout(Qt.Horizontal)
    label = Plasma.Label()
    label.setText("")
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
    headerLayout.addItem(label)
    pixmap = QPixmap(os.path.dirname(__file__) + "/../logo-small.png")
    pixmapWidget = QGraphicsPixmapWidget(pixmap)
    pixmapWidget.setMinimumSize(pixmap.width(), pixmap.height())
    pixmapWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    headerLayout.addItem(pixmapWidget)
    self.layout.addItem(headerLayout)

    # new activity label

    label = Plasma.Label()
    label.setText('<html><b>New activity</b></html>')
    self.layout.addItem(label)

    # new activity form

    newActivityFrame = Plasma.Frame(self.applet)
    newActivityFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    newActivityLayout = QGraphicsLinearLayout(Qt.Vertical, newActivityFrame)

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
    self.projectNameCombo = Plasma.ComboBox()
    projectNameLayout.addItem(self.projectNameCombo)
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
    date = KDateWidget()
    date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    date.setAttribute(Qt.WA_NoSystemBackground)
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
#    hours.setMaximumSize(100, 10)
#    hours.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
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
    self.connect(sendButton, SIGNAL("clicked()"), self.postActivity)

    # recent activities

    label = Plasma.Label()
    label.setText('<html><br/><b>Recent activities</b></html>')
    self.layout.addItem(label)

    for i in xrange(3):
      frame = Plasma.Frame()
      frameLayout = QGraphicsLinearLayout(Qt.Vertical, frame)
      label = Plasma.Label()
      frameLayout.addItem(label)
      self.layout.addItem(frame)
      self.activitiesLabels.append(label)

    self.setLayout(self.layout)
    # self.resize(350, 500)


#    flashLayout = QGraphicsLinearLayout(Qt.Horizontal, self)
#    self.label = Plasma.FlashingLabel()#self)
#    self.label.setAutohide(True)
#    self.label.setMinimumSize(0, 20)
#    self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


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

  def setupTimers(self):
    pass
    # setup morning notifications
#    self.morningTimer = QTimer(self)
#    self.connect(self.morningTimer, SIGNAL("timeout()"), self.morningCheck)
#    self.morningTimer.start(10 * 1000)

    # setup afternoon notifications
#    self.afternoonTimer = QTimer(self)
#    self.connect(self.afternoonTimer, SIGNAL("timeout()"), self.afternoonCheck)
#    self.afternoonTimer.start(20 * 1000)

#  def constraintsEvent(self, constraints):
#    pass


  def fetchActivities(self):
#    print int(self.cfg.activitiesNumber)
    return self.makeRequest('/activities?' + urllib.urlencode({ 'search_criteria[limit]': self.cfg.activitiesNumber }))


  def fetchProjects(self):
    return self.makeRequest('/projects')


  def postActivity(self):
    activity = {}
    data = urllib.urlencode({ 'activity[date]': activity['date'], 'activity[project_id]': activity['project_id'],
                              'activity[hours]': activity['hours'], 'activity[comments]': activity['comments'] })
    return self.makeRequest('/activities', data)


  def makeRequest(self, path, data=None):
    self.applet.setBusy(True)
    url = str((self.cfg.instanceURL + path).replace("://", "://" + self.cfg.username + "@"))
    if url.find("?") == -1:
      url += "?auth=basic"
    else:
      url += "&auth=basic"
    if data:
#    job.addMetaData("content-type", "Content-Type: application/x-www-form-urlencoded" )
      pass
    else:
      job = KIO.storedGet(KUrl(url), KIO.Reload, KIO.HideProgressInfo)
    # we want JSON
    job.addMetaData("accept", "application/json, text/javascript, */*")
    job.addMetaData("cookies", "none")
    QObject.connect(job, SIGNAL("result(KJob*)"), self.requestResults)


  def requestResults(self, job):
    self.applet.setBusy(False)
    if job.error() > 0:
      self.showFlash(job.errorString())
    elif job.isErrorPage():
      self.showFlash("Error while connecting to Rubytime instance.")
    else:
      data = simplejson.JSONDecoder().decode(str(job.data()))
      path = str(job.url().path())
      if path.find("/activities") > -1:
        self.updateActivities(data)
      elif path.find("/projects") > -1:
        self.updateProjects(data)


  def updateProjects(self, projects):
    self.projects = {}
    self.projectNameCombo.clear()
    for project in projects:
      self.projects[project["id"]] = project["name"]
      self.projectNameCombo.addItem(project["name"])
    self.fetchActivities()


  def updateActivities(self, activities):
    self.activities = activities
    print activities
    for i in xrange(len(self.activitiesLabels)):
      activity, label = activities[i], self.activitiesLabels[i]
      d = activity["date"].split("-")
      date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
      dateFormatted = date.strftime("%A, %d. %B")
      projectName = self.projects[int(activity["project_id"])]
      time = self.formatMinutes(activity["minutes"])
      label.setText('<html><b>%s</b>: %s on %s</html>' % (dateFormatted, time, projectName))
      

  def formatMinutes(self, minutes):
    h = minutes / 60
    m = minutes % 60
    s = str(h) + "h"
    if m > 0:
      s += " " + str(m) + "m"
    return s
  

  def morningCheck(self):
    self.morningTimer.stop()
    self.sendNotification("<html><b>Morning!</b><br/>Did you fill Rubytime for yesterday?</html>")
    pass


  def afternoonCheck(self):
    self.afternoonTimer.stop()
    self.sendNotification("<html><b>Good afternoon!</b><br/>Don't forget to add today's activities to Rubytime.</html>")
    pass


  def showFlash(self, msg):
    print "flash: " + msg


  def sendNotification(self, body):
#    self.notificationsProxy.Notify('rubytime-plasmoid', 0, "someid", 'folder-red', 'Rubytime', body, [], [], 2000, dbus_interface='org.kde.VisualNotifications')
    #self.notifications.Notify('rubytime-plasmoid', 0, str(random.random() * 10), 'folder-red', 'Rubytime', body, [], [], 0, dbus_interface='org.kde.VisualNotifications')
    pass


  def createConfigurationInterface(self, parent):
    # create general page
    self.configGeneralForm = QWidget()
    self.configGeneral = configgeneral.Ui_form()
    self.configGeneral.setupUi(self.configGeneralForm)
    p = parent.addPage(self.configGeneralForm, ki18n("General").toString())
    p.setIcon( KIcon("user-identity") )
    # init general page
    self.configGeneral.instanceURL.setText(self.cfg.instanceURL)
    self.configGeneral.username.setText(self.cfg.username)

    # create notifications page
    self.configNotificationsForm = QWidget()
    self.configNotifications = confignotifications.Ui_form()
    self.configNotifications.setupUi(self.configNotificationsForm)
    p = parent.addPage(self.configNotificationsForm, ki18n("General").toString())
    p.setIcon( KIcon("preferences-desktop-notification") )
    # init notifications page
#    self.configNotifications.username.setText("jola")

    # buttons
    parent.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel))
    self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
    self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)


  def showConfigurationInterface(self):
    dialog = KPageDialog()
    dialog.setFaceType(KPageDialog.List)
    self.createConfigurationInterface(dialog)
    dialog.exec_()


  def configAccepted(self):
    self.cfg.instanceURL = self.configGeneral.instanceURL.text()
    self.cfg.username = self.configGeneral.username.text()
    self.resetWidget(self.cfg.isValid())
    self.configDenied()


  def configDenied(self):
    self.configGeneralForm.deleteLater()
    self.configNotificationsForm.deleteLater()


def CreateApplet(parent):
  return RubytimeApplet(parent)

