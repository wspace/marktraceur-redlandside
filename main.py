#!/usr/bin/python

# main.py 

import sys
import os.path
from PyQt4 import QtGui, QtCore
from maingui import MainWindow

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())