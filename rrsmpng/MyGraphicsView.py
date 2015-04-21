from PySide import QtGui

class MyGraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(MyGraphicsView, self).__init__(parent)


    def wheelEvent(self, event):
        scaleFactor = 1.15;
        if event.delta() > 0:
            self.scale(scaleFactor, scaleFactor)
        else:
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor)
        event.accept()

