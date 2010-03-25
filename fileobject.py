import os.path
from PyQt4 import QtGui, QtCore

class FileObject(object):

	def __init__(self, parent=None):
		self.parent = parent
		self.filename = ""
		self.language = ""
		self.runcomm = ""
		self.buildcomm = ""		

	def newfile(self):
		languages = ["C++", "Python","Prolog", "Lisp", "Whitespace", "LOLCODE"]
		self.language, ok = QtGui.QInputDialog.getItem(self.parent, 'Choose a Language', 'Which language are you using today?', languages, 0, False)
		if ok:
			langlabel = "Current Language: " + self.language
			self.parent.textedit.clear()
			self.parent.textedit.setEnabled(True)
			self.parent.langlabel.setText("Current Language: " + self.language)

	def openfile(self):
		self.filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open file...', os.path.expanduser('~'))
		if self.filename == "":
			return (False, "")
		fileobject = open(self.filename, 'r')
		self.parent.textedit.setText(fileobject.read())
		self.findtype(self.filename.split(".")[-1])
		self.parent.langlabel.setText("Current Language: " + self.language)
		fileobject.close()
		self.parent.textedit.setEnabled(True)
		parent.langlabel.setText("Current Language: " + self.language)

	def savefile(self, forcedia = False):
		# Take all the text in the editor, put all the text into a file, and change the filename to that.
		if self.filename == "" or forcedia:
			self.filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Save file...', os.path.expanduser('~'))
		fileout = open(self.filename, 'w')
		fileout.write(self.parent.textedit.toPlainText())
		fileout.close()
		self.findtype(self.filename.split(".")[-1])

	def findtype(self, ext):
		if ext == "cpp":
			self.language = "C++"
			self.runcomm = str(self.filename[:-4])
			self.buildcomm = "g++ " + self.filename + " -o " + self.filename[:-4]

		elif ext == "py":
			self.language = "Python"
			self.runcomm = "python " + str(self.filename)
			self.buildcomm = ""

		elif ext == "pro":
			self.language = "Prolog"
			self.runcomm = "prolog -s " + str(self.filename)
			self.buildcomm = ""

		elif ext == "lisp":
			self.language = "Lisp"
			self.buildcomm = "clisp " + str(self.filename)

		elif ext == "ws":
			self.language = "Whitespace"
			self.buildcomm = ""

		elif ext == "LOL":
			self.language = "LOLCODE"
