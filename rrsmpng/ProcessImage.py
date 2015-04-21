#!/usr/bin/env python3

import random
from PIL import Image
from PySide import QtGui

class ProcessImage(object):
    def __init__(self, filename=""):
        self.filename = filename
        pass

    def pilLoadPng(self):
        im = Image.open(self.filename)
        return self.pilToQImage(im, im.size)

    def pilToQImage(self, im, size):
        return QtGui.QImage(im.tobytes("raw", "BGRX"), size[0], size[1], QtGui.QImage.Format_RGB32)
        
    def genRandomTest(self):
        size = (200,200)
        im = Image.new("RGB", size)
        d = []
        for i in range(size[0]*size[1]):
            v = (random.randint(0, 255),
                 random.randint(0, 255),
                 random.randint(0, 255))
            d.append(v)
        im.putdata(d)
        
        return self.pilToQImage(im, size)

