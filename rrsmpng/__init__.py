import sys
import argparse
from PySide import  QtGui, QtUiTools
import rrsmpng.Gui
import rrsmpng.MyGraphicsView

def main():
    app = QtGui.QApplication(sys.argv)

    parser = argparse.ArgumentParser(description='Really Really Show My Png')
    parser.add_argument('filename',
                        help='The file to be process')

    args = parser.parse_args()

    # loader = QtUiTools.QUiLoader()
    # loader.registerCustomWidget(MyGraphicsView)

    rrsmpngui = rrsmpng.Gui.RrsmPngGui(args)
    rrsmpngui.show()
    sys.exit(app.exec_())
