#!/usr/bin/env python3

import sys
import argparse
from rrsmpng.ProcessImage import *
from PySide import QtCore, QtGui, QtUiTools


class RrsmPngGui(QtGui.QWidget):
    def __init__(self, args):
        super(RrsmPngGui, self).__init__()
        self.args = args
        self.pi = ProcessImage(self.args.filename)
        self.initUI()
        self.display_image(self.pi.pilLoadPng())
        
    def initUI(self):
        self.MainWindow = self.loadUiWidget("rrsmpng/MainWindow.ui")

    def loadUiWidget(self, uifilename, parent=None):
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        ui = loader.load(uifile, parent)
        uifile.close()
        return ui
    
    def display_image(self, qtImg):
        scene = QtGui.QGraphicsScene()
        pixmap = QtGui.QPixmap.fromImage(qtImg);
        scene.addPixmap(pixmap)
        self.MainWindow.gvImage.setScene(scene)
        
    def show(self):
        self.MainWindow.show()

