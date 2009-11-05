from PyQt4.QtCore import *

class RubytimeConfig(object):
  defaults = { 'instanceURL': QString('http://'), 'username': QString(), 'activitiesNumber': QVariant(3),
               'checkYesterday': QVariant(False), 'checkToday': QVariant(False),
               'checkYesterdayTime': QString("09:00:00"), 'checkTodayTime': QString("17:00:00") }

  def __init__(self, config):
    self.__dict__['cfg'] = config

  def __getattr__(self, name):
    val = self.__dict__['cfg'].readEntry(name, self.defaults.get(name))
    if val.type() == QVariant.String:
      return val.toString()
    else:
      return val

  def __setattr__(self, name, value):
    self.__dict__['cfg'].writeEntry(name, value)

  def isValid(self):
    return not self.instanceURL.trimmed().isEmpty() and not self.username.trimmed().isEmpty()
