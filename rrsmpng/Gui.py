import sys
import argparse
from rrsmpng.ProcessImage import *
from rrsmpng.MyGraphicsView import *
from rrsmpng.Log import *
from PySide import QtCore, QtGui, QtUiTools
from rrsmpng.MainWindow import Ui_MainWindow

class RrsmPngGui(QtGui.QWidget):
    def __init__(self, args):
        super(RrsmPngGui, self).__init__()
        self.args = args
        self.pi = ProcessImage(self.args.filename)
        self.initUI()
        self.log = Log(self.ui.pteLog)
        
        self.tryNormalLaod()

    def tryNormalLaod(self):
        self.log.info("Tring to open the png with PIL...")
        try:
            im = self.pi.pilLoadPng()
            self.display_image(im)
        except Exception as e:
            err = "Exception: %s: %s" % (type(e).__name__, e)
            self.log.error(err)
    def initUI(self):
        self.MainWindow = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)


    
    def display_image(self, qtImg):
        scene = QtGui.QGraphicsScene()
        pixmap = QtGui.QPixmap.fromImage(qtImg);
        scene.addPixmap(pixmap)
        self.ui.gvImage.setScene(scene)
        
    def show(self):
        self.MainWindow.show()

