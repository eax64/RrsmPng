import sys
import argparse
from PySide import  QtGui
import rrsmpng.Gui

def main():
    app = QtGui.QApplication(sys.argv)

    parser = argparse.ArgumentParser(description='Really Really Show My Png')
    parser.add_argument('filename',
                        help='The file to be process')

    args = parser.parse_args()

    rrsmpngui = rrsmpng.Gui.RrsmPngGui(args)
    rrsmpngui.show()
    sys.exit(app.exec_())
