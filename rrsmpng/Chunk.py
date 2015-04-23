import struct
import zlib

def crc(tag, data):
    checksum = zlib.crc32(tag)
    checksum = zlib.crc32(data, checksum)
    checksum &= 2**32-1
    return checksum

 
class Chunk(object):

    def __init__(self, size=0, name=b""):
        self.remainData = b""
        self.fieldSize = size
        self.fieldName = name
        self.fieldCrc = 0

    def parseChunk(self, data):
        self.fieldSize = struct.unpack(">I", data[:4])[0]
        data = data[4:]
        self.fieldName = data[:4]
        data = data[4:]

        return self.factory(data)

    def factory(self, data):
        if self.fieldName == b"IHDR":
            return IHDR(data, self.fieldSize, self.fieldName)
        elif self.fieldName == b"IDAT":
            return IDAT(data, self.fieldSize, self.fieldName)
        elif self.fieldName == b"IEND":
            return IEND(data, self.fieldSize, self.fieldName)
        else:
            return Unknown(data, self.fieldSize, self.fieldName)
        
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        fields = [(a[5:], getattr(self, a)) for a in self.__dict__.keys() if a.startswith("field")]
        return repr(["%s: %s" % (k,repr(v))  if not hasattr(v, "__len__") or len(v) < 10 else bytes(k + ": ", "utf8") + v[:5] + b"..." + v[:5] for k,v in fields])

class IHDR(Chunk):
    def __init__(self, data, size, name):
        super(self.__class__, self).__init__(size, name)
        self.fieldWidth = 0
        self.fieldHeight = 0
        self.parseChunk(data)

    def parseChunk(self, data):
        self.fieldWidth = struct.unpack(">I", data[:4])[0]
        data = data[4:]
        self.fieldHeight = struct.unpack(">I", data[:4])[0]
        data = data[4:]
        
        (self.fieldBitDepth,
         self.fieldColorType,
         self.fieldCompressionMethod,
         self.fieldFilterMethod,
         self.fieldInterlaceMethod) = struct.unpack(">BBBBB", data[:5])
        data = data[5:]
        self.fieldCrc = struct.unpack(">I", data[:4])[0]
        data = data[4:]
        self.remainData = data

    def toBytes(self):
        return struct.pack(">I4sIIBBBBBI",
                           self.fieldSize,
                           self.fieldName,
                           self.fieldWidth,
                           self.fieldHeight,
                           self.fieldBitDepth,
                           self.fieldColorType,
                           self.fieldCompressionMethod,
                           self.fieldFilterMethod,
                           self.fieldInterlaceMethod)

class IDAT(Chunk):
    def __init__(self, data, size, name):
        super(self.__class__, self).__init__(size, name)
        self.fieldData = b""
        self.parseChunk(data)

    def parseChunk(self, data):
        self.fieldData = data[:self.fieldSize]
        data = data[self.fieldSize:]
        self.fieldCrc = struct.unpack(">I", data[:4])[0]
        data = data[4:]
        self.remainData = data

class IEND(Chunk):
    def __init__(self, data, size, name):
        super(self.__class__, self).__init__(size, name)
        self.data = b""
        self.parseChunk(data)

    def parseChunk(self, data):
        self.fieldCrc = struct.unpack(">I", data[:4])[0]
        data = data[4:]
        self.remainData = data

class Unknown(Chunk):
    def __init__(self, data, size, name):
        super(self.__class__, self).__init__(size, name)
        self.data = b""
        self.parseChunk(data)

    def parseChunk(self, data):
        self.fieldData = data[:self.fieldSize]
        data = data[self.fieldSize:]
        self.fieldCrc = struct.unpack(">I", data[:4])[0]
        data = data[4:]
        self.remainData = data

