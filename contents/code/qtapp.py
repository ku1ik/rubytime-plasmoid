# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import rubytime

class StartQT4(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.button = QPushButton(self)

        self.initialTimer = QTimer(self)
        self.connect(self.initialTimer, SIGNAL("timeout()"), self.initialFetch)
        self.initialTimer.setSingleShot(True)
        self.initialTimer.start(1 * 1000)

    def initialFetch(self):
        self.api = rubytime.RubytimeSession('http://localhost:4000', 'dev1', 'password', self)
        self.api.getActivities()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
