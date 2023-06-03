"""
Original software copyright 2010 Mark Holmquist and Logan May.

Some recent modifications copyright 2012 Mark Holmquist.

This file is part of redlandside.

redlandside is licensed under the GNU GPLv3 or later, please see the
COPYING file in this directory or http://www.gnu.org/licenses/gpl-3.0.html for
more information.
"""

#!/usr/bin/python

import os.path
import os
import subprocess

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QLabel, QMessageBox, QTextEdit

import fileobject
import synhigh

class MainWindow (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Set the window size when opened, title the window, and set the icon

        self.currentfile = fileobject.FileObject(parent=self)

        self.resize(800,600)
        self.setWindowTitle('rIDE')
        self.setWindowIcon(QIcon('icons/ride.png'))

        # Declare the text field widget, and make it the most important,
        # because the Lady of the Lake raised aloft the blade Excalibur from
        # the lake and gave it to the text widget.

        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)
        self.textedit.setFontFamily("monospace")
        self.textedit.setLineWrapMode(0)
        welcomemsg = 'Welcome to rIDE\n\n'
        welcomemsg += 'Please create a new file or open an existing one.'
        self.textedit.setText(welcomemsg)
        self.textedit.setEnabled(False)
        self.textedit.textChanged.connect(self.whenchanged)

        self.highlighter = synhigh.SyntaxHighlighter(self.currentfile)

        # Creates an exit button, sets its icon and adds functionality.

        exit = QAction(QIcon('icons/exit.png'),
                                   'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.close)

        # Creates a similar shortcut for a new file

        newfile = QAction(QIcon('icons/newfile.png'),
                                      'New', self)
        newfile.setShortcut('Ctrl+N')
        newfile.setStatusTip('Create a new file')
        newfile.triggered.connect(self.currentfile.newfile)

        # Creates a similar shortcut for opening a file

        openfile = QAction(QIcon('icons/openfile.png'),
                                       'Open...', self)
        openfile.setShortcut('Ctrl+O')
        openfile.setStatusTip('Open a file')
        openfile.triggered.connect(self.currentfile.openfile)

        # Creates a similar shortcut for saving a file

        self.savefile = QAction(QIcon('icons/savefile.png'),
                                       'Save...', self)
        self.savefile.setShortcut('Ctrl+S')
        self.savefile.setStatusTip('Save this file')
        self.savefile.setEnabled(False)
        self.savefile.triggered.connect(self.currentfile.savefile)

        # Creates a similar shortcut for saving a file, forcing a dialog.

        self.saveas = QAction(QIcon('icons/savefile.png'),
                                     'Save as...', self)
        self.saveas.setStatusTip('Save this file with a different filename')
        self.saveas.setEnabled(False)
        self.saveas.triggered.connect(self.currentfile.saveas)

        # Creates a similar shortcut for building a file

        buildicon = QIcon('icons/buildonly.png')
        self.buildonly = QAction(buildicon, 'Build (Ctrl-T)', self)
        self.buildonly.setShortcut('Ctrl+T')
        self.buildonly.setStatusTip('Build the project')
        self.buildonly.setEnabled(False)
        self.buildonly.triggered.connect(self.onlybuild)

        # Creates the build-and-run shortcut
        bricon = QIcon('icons/buildandrun.png')
        self.buildrun = QAction(bricon, 'Build and Run (Ctrl-B)', self)
        self.buildrun.setShortcut('Ctrl+B')
        self.buildrun.setStatusTip('Build the project and run it')
        self.buildrun.setEnabled(False)
        self.buildrun.triggered.connect(self.buildandrun)

        # Creates the run shortcut

        self.runonly = QAction(QIcon('icons/runonly.png'),
                                      'Run (Ctrl-R)', self)
        self.runonly.setShortcut('Ctrl+R')
        self.runonly.setStatusTip('Run the latest build')
        self.runonly.setEnabled(False)
        self.runonly.triggered.connect(self.onlyrun)

        # Creates the copy shortcut

        self.copy = QAction('Copy', self)
        self.copy.setShortcut('Ctrl+C')
        self.copy.setStatusTip('Copy the selected text')
        self.copy.setEnabled(False)
        self.copy.triggered.connect(self.textedit.copy)

        # Create the cut shortcut

        self.cut = QAction('Cut', self)
        self.cut.setShortcut('Ctrl+X')
        self.cut.setStatusTip('Cut the selected text')
        self.cut.setEnabled(False)
        self.cut.triggered.connect(self.textedit.cut)

        # Create the paste shortcut

        self.paste = QAction('Paste', self)
        self.paste.setShortcut('Ctrl+V')
        self.paste.setStatusTip('Paste text from the clipboard')
        self.paste.setEnabled(False)
        self.paste.triggered.connect(self.textedit.paste)

        # Initialize Status bar

        statusbar = self.statusBar()
        self.langlabel = QLabel()
        statusbar.addWidget(self.langlabel)

        # Creates the menu bar and the file menu,
        # adding in the appropriate actions

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(newfile)
        file.addAction(openfile)
        file.addAction(self.savefile)
        file.addAction(self.saveas)
        file.addAction(exit)

        # Creates the edit menu, adding in the appropriate contents

        edit = menubar.addMenu('&Edit')
        edit.addAction(self.copy)
        edit.addAction(self.cut)
        edit.addAction(self.paste)

        # Make a toolbar with all the trimmings

        self.toolbar = self.addToolBar('Buttons')
        self.toolbar.addAction(newfile)
        self.toolbar.addAction(openfile)
        self.toolbar.addAction(self.savefile)
        self.toolbar.addAction(self.buildonly)
        self.toolbar.addAction(self.buildrun)
        self.toolbar.addAction(self.runonly)
        self.toolbar.addAction(exit)

    def onlybuild(self):
        # Ask if they want to save the file, then do so--otherwise, throw an
        # error and tell them they want "onlyrun"--then save the file, build it
        # with the appropriate command, and display the results.
        saved = True
        if os.path.isfile(self.currentfile.filename):
            test = open(self.currentfile.filename)
            if test.read() != self.textedit.toPlainText():
                saved = False
        else:
            saved = False
        if not saved:
            t = "WARNING: Save the file!"
            msg = "You should save the file before continuing!"
            ok = "OK"
            c = "Cancel"
            needsave = QMessageBox.question(self, t, msg, ok, c)
            if needsave == 0:
                self.currentfile.savefile(True)

        br = "Build results"
        if self.currentfile.language not in ["C++"]:
            msg = "This language doesn't need to be built! Just hit 'Run'!"
            QMessageBox.about(self, br, msg)
            raise Exception("This is an interpreted language...")
        statz, outz = subprocess.getstatusoutput(self.currentfile.buildcomm)
        if statz != 0:
            rbc = "xterm -e '" + self.currentfile.buildcomm
            rbc += "; python pause.py'"
            os.system(rbc)
        else:
            QMessageBox.about(self, br, "The build succeeded!")

    def buildandrun(self):
        # Ask if they want to save the file, then do so--otherwise, throw an
        # error--then save the file, build it with the appropriate command, and
        # display the results.
        #
        # If the command used to build it exits with an error, we have a
        # problem--make sure it doesn't close to allow review of the errors,
        # but don't try to run the binary.
        #
        # If it makes it through, close the build window and run the program.
        if self.currentfile.language == "C++":
            self.onlybuild()
        self.onlyrun()

    def onlyrun(self):
        # Find the binary created by the IDE. If it doesn't exist, throw an
        # error. Then, run it.
        if self.currentfile.language not in ['C++']:
            saved = True
            if os.path.isfile(self.currentfile.filename):
                test = open(self.currentfile.filename)
                if test.read() != self.textedit.toPlainText():
                    saved = False
            else:
                saved = False
            if not saved:
                t = "WARNING: Save the file!"
                m = "You should save the file before continuing!"
                ok = QMessageBox.Ok
                c = QMessageBox.Cancel
                needsave = QMessageBox.question(self, t, m, ok, c)
                if needsave == 0:
                    self.currentfile.savefile(True)
        rbc = "xterm -e '" + self.currentfile.runcomm + "; python pause.py'"
        os.system(rbc)

    def whenchanged(self):
        self.textedit.setFontFamily("monospace")
        self.currentfile.saved = False

    def enable_controls(self):
        self.savefile.setEnabled(True)
        self.saveas.setEnabled(True)
        self.buildonly.setEnabled(True)
        self.buildrun.setEnabled(True)
        self.runonly.setEnabled(True)
        self.copy.setEnabled(True)
        self.paste.setEnabled(True)
        self.cut.setEnabled(True)
