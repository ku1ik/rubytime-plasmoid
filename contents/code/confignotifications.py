from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyKDE4.kdeui import *
import confignotificationsform

class ConfigNotifications(QWidget, confignotificationsform.Ui_form):
  def __init__(self):
    QWidget.__init__(self)
    self.setupUi(self)
