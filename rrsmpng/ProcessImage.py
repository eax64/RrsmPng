import random
import zlib
from PIL import Image
from PySide import QtGui
from rrsmpng.Log import *
from rrsmpng.Chunk import *


class ProcessImage(object):
    def __init__(self, filename=""):
        self.filename = filename
        self.log = None
        self.chunks = []
        self.size = (200,200)

    def pilLoadPng(self, filename=None):
        fn = self.filename
        if filename:
            fn = filename
        im = Image.open(fn)
        return self.pilToQImage(im, im.size)

    def pilToQImage(self, im, size):
        return QtGui.QImage(im.tobytes("raw", "BGRX"), size[0], size[1], QtGui.QImage.Format_RGB32)
        
    def genRandomTest(self):
        im = Image.new("RGB", self.size)
        d = []
        for i in range(self.size[0]*self.size[1]):
            v = (random.randint(0, 255),
                 random.randint(0, 255),
                 random.randint(0, 255))
            d.append(v)
        im.putdata(d)
        
        return self.pilToQImage(im, self.size)

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


    def chunksSeekingParsing(self):
        data = open(self.filename, "rb").read()
        known = [b"IHDR", b"IDAT", b"IEND"]
        chunks_offsets = []
        offs = 0
        while True:
            idx = []
            for k in known:
                i = data.find(k, offs)
                if i > -1:
                    idx.append((i, k))
            if not idx:
                break
            idx = sorted(idx, key=lambda x: x[0])
            offs = idx[0][0]+4
            chunks_offsets.append(idx[0])

        chunks_offsets.append((len(data), ""))
        sizes = map(lambda x:x[1][0]-x[0][0]-8, zip(chunks_offsets , chunks_offsets[1:]))
        chunks_offsets = [c+(s,) for c,s in list(zip(chunks_offsets, sizes))]
        print(chunks_offsets)
        print("")
        self.chunks = []
        for coff,cname,csize in chunks_offsets:
            c = Chunk(csize, cname)
            cc = c.factory(data[coff+4:])
            if (cc.fieldName == b"IHDR"):
                self.size = (cc.fieldWidth, cc.fieldHeight)
            self.chunks.append(cc)

        return True

    def idatToImage(self):
        all_chunks = b"".join(c.fieldData for c in self.chunks if c.fieldName == b"IDAT")
        i = 0
        while i < len(all_chunks):
            try:
                raw = zlib.decompressobj(-zlib.MAX_WBITS).decompress(all_chunks[i:])
            except zlib.error:
                i += 1
                continue
            break

        raw2 = bytearray()
        for vv in range(0, len(raw)):
            if vv % (self.size[0]*3 + 1) == 0:
                if raw[vv] > 4:
                    raw2.append(3)
                else:
                    raw2.append(raw[vv])
            else:
                raw2.append(raw[vv])
                    
        raw2 = zlib.compress(raw2)
        newf = open("/tmp/rrsmpng-tmp.png", "wb")
        s = b"\x89PNG\x0d\x0a\x1a\x0a"
        s +=  struct.pack(">I4s",
                         13,
                         b"IHDR")
                         
        chunk = struct.pack(">IIBBBBB",
                         self.size[0],
                         self.size[1],
                         8,
                         2,
                         0,
                         0,
                         0)
        chunk += struct.pack(">I", crc(b"IHDR", chunk))
        s += chunk

        s += struct.pack(">I", len(raw2))
        s += b"IDAT"
        s += raw2
        s += struct.pack(">I", crc(b"IDAT", raw2))
        newf.write(s)

        s += struct.pack(">I", 0)
        s += b"IEND"
        s += struct.pack(">I", crc(b"IEND", b""))
        newf.write(s)
        
       
        
        # im = Image.new("RGB", size)
        # d = []
        # for i in range(size[0]*size[1]):
        #     v = (50,0,0)
        #     if i*3 + 3 <= len(raw):
        #         v = (raw[i*3], raw[i*3+1], raw[i*3+2])
        #     d.append(v)
        # im.putdata(d)
        
        return self.pilLoadPng("/tmp/rrsmpng-tmp.png")
