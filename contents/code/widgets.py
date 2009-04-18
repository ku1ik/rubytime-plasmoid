from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QGraphicsPixmapWidget(QGraphicsWidget):
  def __init__(self, pixmap):
    QGraphicsWidget.__init__(self)
    self.pixmap = pixmap

  def paint(self, painter, option, widget=None):
    painter.drawPixmap(0, 0, self.pixmap)

  def sizeHint(self, which, constraint):
    return QSizeF(self.pixmap.size())
