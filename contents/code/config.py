from PyQt4.QtCore import *

class RubytimeConfig(object):
  defaults = { 'instanceURL': QString('http://'), 'activitiesNumber': QVariant(3),
               'checkYesterday': QVariant(False), 'checkToday': QVariant(False),
               'checkYesterdayTime': QString("09:00:00"), 'checkTodayTime': QString("17:00:00") }

  def __init__(self, config):
    self.__dict__['cfg'] = config

  def __getattr__(self, name):
    return self.__dict__['cfg'].readEntry(name, self.defaults.get(name))

  def __setattr__(self, name, value):
#    print "setting %s to %s" % (name, value)
    self.__dict__['cfg'].writeEntry(name, value)

  def isValid(self):
    return not self.instanceURL.trimmed().isEmpty() and not self.username.trimmed().isEmpty()
