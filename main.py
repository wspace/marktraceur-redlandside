#!/usr/bin/python

# main.py 

import sys
import os.path
from PyQt4 import QtGui, QtCore


class LanguageDialogue(QtGui.QDialog):
	def __init__(self, parent=None):
        	QtGui.QDialog.__init__(self, parent)
        	self.setGeometry(300, 300, 350, 80)
		self.setWindowTitle('Select a Language')
	        self.button = QtGui.QPushButton('Dialog', self)
        	self.button.setFocusPolicy(QtCore.Qt.NoFocus)
		
	        self.label = QtGui.QLineEdit(self)
	        self.label.move(130, 22)

		self.dropdown = QtGui.QComboBox()
		self.dropdown.addItem('C++')
		self.dropdown.addItem('Python')
		self.dropdown.addItem('Lisp')
		self.dropdown.addItem('Prolog')
		self.dropdown.addItem('LOLcode')
		self.dropdown.addItem('Whitespace')

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		
		# Set the window size when opened, title the window, and set the icon
		
		self.resize(800,600)
		self.setWindowTitle('rIDE')
		self.setWindowIcon(QtGui.QIcon('icons/ride.png'))
		
		# Declare the text field widget, and make it the most important, because the Lady of the Lake raised aloft the blade Excalibur from the lake and gave it to the text widget. 
		
		self.textedit = QtGui.QTextEdit()
		self.setCentralWidget(self.textedit)
		self.textedit.setText('Welcome to rIDE\n\nPlease create a new file or open an existing one to be able to use rIDE.')
		self.textedit.setEnabled(False)
		
		# Creates an exit button, sets its icon and adds functionality.
		
		exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		
		# Creates a similar shortcut for a new file
		
		newfile = QtGui.QAction(QtGui.QIcon('icons/newfile.png'), 'New', self)
		newfile.setShortcut('Ctrl+N')
		newfile.setStatusTip('Create a new file')
		self.connect(newfile, QtCore.SIGNAL('triggered()'), self.createanewfile)
		
		# Creates a similar shortcut for opening a file
		
		openfile = QtGui.QAction(QtGui.QIcon('icons/openfile.png'), 'Open...', self)
		openfile.setShortcut('Ctrl+O')
		openfile.setStatusTip('Open a file')
		self.connect(openfile, QtCore.SIGNAL('triggered()'), self.openafile)
		
		# Creates a similar shortcut for saving a file
				
		savefile = QtGui.QAction(QtGui.QIcon('icons/savefile.png'), 'Save...', self)
		savefile.setShortcut('Ctrl+S')
		savefile.setStatusTip('Create a new file')
		self.connect(savefile, QtCore.SIGNAL('triggered()'), self.savethefile)
		
		# Creates a similar shortcut for saving a file
		
		buildonly = QtGui.QAction(QtGui.QIcon('icons/buildonly.png'), 'Build', self)
		buildonly.setShortcut('Ctrl+T')
		buildonly.setStatusTip('Build the project')
		self.connect(buildonly, QtCore.SIGNAL('triggered()'), self.onlybuild)
		
		# Creates a similar shortcut for saving a file
		
		buildrun = QtGui.QAction(QtGui.QIcon('icons/buildandrun.png'), 'Build and Run', self)
		buildrun.setShortcut('Ctrl+B')
		buildrun.setStatusTip('Build the project and run it')
		self.connect(buildrun, QtCore.SIGNAL('triggered()'), self.buildandrun)
		
		# Creates the run shortcut
		
		runonly = QtGui.QAction(QtGui.QIcon('icons/runonly.png'), 'Run', self)
		runonly.setShortcut('Ctrl+R')
		runonly.setStatusTip('Run the latest build')
		self.connect(runonly, QtCore.SIGNAL('triggered()'), self.onlyrun)
		
		copy = QtGui.QAction('Copy', self)
		copy.setShortcut('Ctrl+C')
		copy.setStatusTip('Copy the selected text')
		self.connect(copy, QtCore.SIGNAL('triggered()'), self.textedit, QtCore.SLOT('copy()'))
		
		cut = QtGui.QAction('Cut', self)
		cut.setShortcut('Ctrl+X')
		cut.setStatusTip('Cut the selected text')
		self.connect(cut, QtCore.SIGNAL('triggered()'), self.textedit, QtCore.SLOT('cut()'))
		
		paste = QtGui.QAction('Paste', self)
		paste.setShortcut('Ctrl+V')
		paste.setStatusTip('Paste text from the clipboard')
		self.connect(paste, QtCore.SIGNAL('triggered()'), self.textedit, QtCore.SLOT('paste()'))
		
		# Initializes the status bar
		
		self.statusBar()
		
		# Creates the munu bar and the file menu, adding in the appropriate actions
		
		menubar = self.menuBar()
		file = menubar.addMenu('&File')
		file.addAction(newfile)
		file.addAction(openfile)
		file.addAction(savefile)
		file.addAction(exit)
		
		# Creates the run/build menu, adding in the appropriate contents
		
		edit = menubar.addMenu('&Edit')
		edit.addAction(copy)
		edit.addAction(cut)
		edit.addAction(paste)
		
		# Make a toolbar with all the trimmings
		
		toolbar = self.addToolBar('Buttons')
		toolbar.addAction(newfile)
		toolbar.addAction(openfile)
		toolbar.addAction(savefile)
		toolbar.addAction(buildonly)
		toolbar.addAction(buildrun)
		toolbar.addAction(runonly)
		toolbar.addAction(exit)
		
		self.filename = ""
	
	def createanewfile(self):
		if self.filename != "" and not self.ischanged():
			# Ask them to save the file
			pass
		else:
			# Clear the text editor, open a dialog to get the program's language.
			lang = LanguageDialogue()
			lang.show()
			self.textedit.setEnabled(True)
			self.textedit.clear()
	
	def openafile(self):
		if self.filename != "" and not self.ischanged():
			# Ask them to save the file
			pass
		else:
			# Clear the text editor, find the file, feed the text in the file into the text editor.
			self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file...', os.path.expanduser('~'))
			self.textedit.setEnabled(True)
			self.textedit.clear()
	
	def savethefile(self):
		# Take all the text in the editor, put all the text into a file, and change the filename to that.
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Save file...', os.path.expanduser('~'))
		fileobject = open(filename, 'w')
		fileobject.write(self.textedit.toPlainText())
		fileobject.close()
	
	def onlybuild(self):
		# Ask if they want to save the file, then do so--otherwise, throw an error and tell them they want "onlyrun"--then save the file, build it with the appropriate command, and display the results.
		pass
	
	def buildandrun(self):
		# Ask if they want to save the file, then do so--otherwise, throw an error--then save the file, build it with the appropriate command, and display the results.
		# If the command used to build it exits with an error, we have a problem--make sure it doesn't close to allow review of the errors, but don't try to run the binary.
		# If it makes it through, close the build window and run the program.
		pass
	
	def onlyrun(self):
		# Find the binary created by the IDE. If it doesn't exist, throw an error. Then, run it.
		pass

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
