
from PySide import QtCore, QtGui

class Window( QtGui.QWidget ):
	"""docstring for Window"""
	def __init__( self, title='undefind', size=[500, 400] ):
		super( Window, self ).__init__()
		self.setWindowTitle( title )
		self.resize( size[0], size[1] )

		self.menuBar    = QtGui.QMenuBar()
		self.fileMenu   = QtGui.QMenu("File", self)
		self.helpAction = self.fileMenu.addAction("Help")
		self.exitAction = self.fileMenu.addAction("Exit")
		self.content    = QtGui.QVBoxLayout()

		self.menuBar.addMenu( self.fileMenu )
		self.content.setMenuBar(self.menuBar)
		self.setLayout(self.content)
