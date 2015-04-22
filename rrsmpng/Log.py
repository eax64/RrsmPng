from PySide import QtGui

class Log(object):
    def __init__(self, plainTextEdit):
        self.pte = plainTextEdit

    def add(self, text, color=None):
        if not color:
            self.pte.appendPlainText(text)
        else:
            self.pte.appendHtml('<font color="%s">%s</font>' % (color, text))

    def error(self, text):
        self.add(text, "red")

    def warning(self, text):
        self.add(text, "orange")

    def info(self, text):
        self.add(text, "green")
