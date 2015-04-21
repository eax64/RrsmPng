import sys
import argparse
from rrsmpng.ProcessImage import *
from rrsmpng.MyGraphicsView import *
from PySide import QtCore, QtGui, QtUiTools
from rrsmpng.MainWindow import Ui_MainWindow

class RrsmPngGui(QtGui.QWidget):
    def __init__(self, args):
        super(RrsmPngGui, self).__init__()
        self.args = args
        self.pi = ProcessImage(self.args.filename)
        self.initUI()
        self.setupEvent()
        self.display_image(self.pi.pilLoadPng())
        
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

