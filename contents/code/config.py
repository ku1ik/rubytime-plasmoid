from PyQt4.QtCore import *

class RubytimeConfig(object):

  def __init__(self, config):
    self.cfg = config

  def isValid(self):
    return not self.instanceURL.isEmpty() and not self.username.isEmpty()
  
  def getInstanceURL(self):
    return self.cfg.readEntry('instanceURL', 'http://localhost:4000')
  
  def setInstanceURL(self, value):
    self.cfg.writeEntry('instanceURL', value.trimmed())

  def getUsername(self):
    return self.cfg.readEntry('username', '')

  def setUsername(self, value):
    self.cfg.writeEntry('username', value.trimmed())

  def getActivitiesNumber(self):
    return self.cfg.readEntry('activitiesNumber', QVariant(3)).toInt()[0]

  def setActivitiesNumber(self, value):
    self.cfg.writeEntry('activitiesNumber', QVariant(int(value)))

  instanceURL = property(getInstanceURL, setInstanceURL)
  username = property(getUsername, setUsername)
  activitiesNumber = property(getActivitiesNumber, setActivitiesNumber)
