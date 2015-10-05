from PySide.QtGui import *
from PySide.QtCore import *


class MyPainterScanline(QWidget, QObject):
    scanlinesChanged = Signal()
    
    def __init__(self, parent=None):
        # QObject.__init__(self)
        super(MyPainterScanline, self).__init__(parent)


        print("init")
        self.data = []

        self.scanline_height = 10
        self.header_size = 20
        self.w = 0
        self.h = 0
        self.lastx = 0
        self.lasty = 0

        
    def mousePressEvent(self, event):
        self.mouseEventPos(event.x(), event.y())
        
    def mouseMoveEvent(self, event):
        self.mouseEventPos(event.x(), event.y())
        
    def mouseEventPos(self, x, y):
        if y < self.header_size:
            return
        if (y-self.header_size)//self.scanline_height >= len(self.data):
            return

        self.lasty = (y-self.header_size)//self.scanline_height
        self.lastx = int(x//((self.w)/5))
        self.data[self.lasty] = self.lastx
        self.scanlinesChanged.emit()
        self.update()


    def paintEvent(self, event):

        print("paint", len(self.data))
        painter = QPainter(self)
        
        self.w = painter.device().width()
        self.h = painter.device().height()

        painter.setBrush(QColor(255, 150, 150))
        painter.drawRect(self.w/5*self.lastx,
                             self.lasty*self.scanline_height+self.header_size,
                             self.w/5,
                             self.scanline_height
            )

                    
        painter.setPen(QPen(QColor(255,150,150), 1))
        painter.drawLine(0,
                         self.header_size,
                         self.w,
                         self.header_size
        )

        
        for x in range(5):
            painter.setPen(QPen(QColor(0,0,0), 2))
            painter.drawText(self.w/5*x+self.w/5/2-5, self.header_size / 2 - 8, 10, 15, Qt.AlignCenter, str(x))
            painter.setPen(QPen(QColor(255,150,150), 1))
            painter.drawLine(self.w/5*x,
                             0,
                             self.w/5*x,
                             self.h
            )
            
        painter.setPen(QPen(QColor(0,0,0), 2))
        for i,d in enumerate(zip(self.data, self.data[1:])):
            painter.setPen(QPen(QColor(255,150,150), 1))
            painter.drawLine(0,
                             i*self.scanline_height+self.header_size,
                             self.w,
                             i*self.scanline_height+self.header_size,
            )
            painter.setPen(QPen(QColor(0,0,0), 2))
            painter.drawLine(self.w/5*d[0] + self.w/5/2,
                             i*self.scanline_height+self.header_size,
                             self.w/5*d[0] + self.w/5/2,
                             (i+1)*self.scanline_height+self.header_size
            )
            painter.drawLine(self.w/5*d[0] + self.w/5/2,
                             (i+1)*self.scanline_height+self.header_size,
                             self.w/5*d[1] + self.w/5/2,
                             (i+1)*self.scanline_height+self.header_size
            )

    # def paintEvent(self, event):
    #     qp = QtGui.QPainter(self)
        
    #     self.w = qp.device().width()
    #     self.h = qp.device().height()

    #     qp.setPen(QtGui.QPen(QtGui.QColor(255,150,150), 1))
    #     qp.drawLine(0,
    #                 self.header_size,
    #                 self.w,
    #                 self.header_size
    #     )


