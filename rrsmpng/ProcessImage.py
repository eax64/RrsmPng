import random
from PIL import Image
from PySide import QtGui
from rrsmpng.Log import *
from rrsmpng.Chunk import *


class ProcessImage(object):
    def __init__(self, filename=""):
        self.filename = filename
        self.log = None
        self.chunks = []

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

    def cleanParsingPng(self):
        data = open(self.filename, "rb").read()

        wdata = data
        if not data.startswith(b"\x89PNG\x0d\x0a\x1a\x0a"):
            self.log.error("Bad file header. Stop clean parsing")
        wdata = wdata[8:]
        
        try:
            c = Chunk()
            cc = c.parseChunk(wdata)
            self.chunks.append(cc)
            print(cc)
            while cc.fieldName != b"IEND":
                cc = c.parseChunk(cc.remainData)
                self.chunks.append(cc)
        except struct.error as e:
            err = "Exception: %s: %s" % (type(e).__name__, e)
            self.log.error(err)
            return False
        return True

