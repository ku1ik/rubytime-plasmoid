from PyQt4.QtCore import QThread
#from threading import Thread
import time

#class ActivitiesWorker(Thread):
class ActivitiesWorker(QThread):
  def __init__(self, widget):
    QThread.__init__(self) #, widget.applet)
#    self.widget = widget

  def run(self):
    time.sleep(3)
    print "1"
#    self.widget.setActivities(self.widget.api.getActivities())
    pass

class ProjectsWorker(QThread):
  def __init__(self, widget):
    QThread.__init__(self) #, widget.applet)
    self.widget = widget

  def run(self):
    self.widget.setProjects(self.widget.api.getProjects())

class AddActivityWorker(QThread):
  def __init__(self, widget, activity):
    QThread.__init__(self) #, widget.applet)
    self.widget = widget
    self.activity = activity

  def run(self):
    res = self.widget.api.addActivity(self.activity)
    if res[0]:
      self.widget.updateActivities()
    else:
      print "errors: " + str(res[1])
