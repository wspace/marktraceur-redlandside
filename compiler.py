from PyQt4 import QtGui, QtCore

class CompilerWindow(QtGui.QDialog):
	def __init__(self, text, parent=None):
		QtGui.QDialog.__init__(self, parent)
		
		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Compiler Output')
		quit = QtGui.QPushButton('Close', self)
		quit.setGeometry(10, 10, 60, 35)
		self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
		self.display = QtGui.QLabel()
		self.display.setText(text)