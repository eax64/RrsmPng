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
        self.initUI()
        self.log = Log(self.ui.pteLog)
        self.pi = ProcessImage(self.args.filename)
        self.pi.log = self.log
        
        self.loadImage()
        model = QtGui.QStandardItemModel()
        for c in self.pi.chunks:
            model.appendRow(QtGui.QStandardItem(str(c)))
        self.ui.lvChunks.setModel(model)
        

    def loadImage(self):
        if self.tryNormalLaod():
            return
        self.log.info("Trying to open the png with custom parsing...")
        
        if self.pi.cleanParsingPng():
            return
        self.log.info("Trying to open the png by seeking correct chunk...")
        
        if self.pi.chunksSeekingParsing():
            self.display_image(self.pi.idatToImage())
            return
        self.log.info("Couldn't parse as a valid png file. Try to read it as a raw png chunk")
        
    def tryNormalLaod(self):
        self.log.info("Trying to open the png with PIL...")
        try:
            im = self.pi.pilLoadPng()
            self.display_image(im)
        except Exception as e:
            err = "Exception: %s: %s" % (type(e).__name__, e)
            self.log.error(err)
            return False
        return True
    
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

