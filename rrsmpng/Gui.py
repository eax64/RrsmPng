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
        self.setup_update()


    def setup_update(self, setMax=True):
        print(self.pi.size)
        self.ui.sbWidth.setMinimum(0)
        self.ui.sbWidth.setMaximum(self.pi.size[0]*2)
        self.ui.sbWidth.setValue(self.pi.size[0])
        self.ui.sbHeight.setMinimum(0)
        self.ui.sbHeight.setMaximum(self.pi.size[1]*2)
        self.ui.sbHeight.setValue(self.pi.size[1])

        self.ui.hsWidth.setMinimum(0)
        self.ui.hsWidth.setMaximum(self.pi.size[0]*2)
        self.ui.hsWidth.setValue(self.pi.size[0])
        self.ui.hsHeight.setMinimum(0)
        self.ui.hsHeight.setMaximum(self.pi.size[1]*2)
        self.ui.hsHeight.setValue(self.pi.size[1])

    def loadImage(self):
        self.log.info("Trying to open the png with PIL...")
        if self.tryNormalLaod():
            return

        self.log.info("Trying to open the png with custom parsing...")
        if self.pi.cleanParsingPng():
            return
        
        self.log.info("Trying to open the png by seeking correct chunk...")
        if self.pi.chunksSeekingParsing():
            self.display_image(self.pi.idatToImage())
            self.ui.pntScanlines.data = self.pi.scanlines
            self.ui.pntScanlines.update()
            return
        
        self.log.info("Couldn't parse as a valid png file. Try to read it as a raw png chunk")
        
    def tryNormalLaod(self):
        try:
            im = self.pi.pilLoadPng()
            self.display_image(im)
        except Exception as e:
            err = "Exception: %s: %s" % (type(e).__name__, e)
            self.log.error(err)
            return False
        return True

    def onScanlinesChanged(self):
        self.pi.newScanlines = self.ui.pntScanlines.data
        self.display_image(self.pi.idatToImage())
    
    def event_hsWidth(self, val):
        self.pi.size = (val, self.pi.size[1])
        self.display_image(self.pi.idatToImage())

    def event_hsHeight(self, val):
        self.pi.size = (self.pi.size[0], val)
        self.display_image(self.pi.idatToImage())
    
    def initUI(self):
        self.MainWindow = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.hsWidth.valueChanged.connect(self.ui.sbWidth.setValue)
        self.ui.hsWidth.valueChanged.connect(self.event_hsWidth)
        self.ui.hsHeight.valueChanged.connect(self.ui.sbHeight.setValue)
        self.ui.hsHeight.valueChanged.connect(self.event_hsHeight)
        self.ui.pntScanlines.scanlinesChanged.connect(self.onScanlinesChanged)
        


    
    def display_image(self, qtImg):
        scene = QtGui.QGraphicsScene()
        pixmap = QtGui.QPixmap.fromImage(qtImg);
        scene.addPixmap(pixmap)
        self.ui.gvImage.setScene(scene)
        
    def show(self):
        self.MainWindow.show()

