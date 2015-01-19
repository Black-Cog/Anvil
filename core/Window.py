
from PySide import QtCore, QtGui

class Window( QtGui.QMainWindow ):
	"""docstring for Window"""
	def __init__( self, title='undefind', size=[500, 400] ):
		super( Window, self ).__init__()
		self.setWindowTitle( title )
		self.resize( size[0], size[1] )

		menuBar    = QtGui.QMenuBar()
		fileMenu   = QtGui.QMenu("File", self)
		helpAction = fileMenu.addAction("Help")
		exitAction = fileMenu.addAction("Exit")

		menuBar.addMenu( fileMenu )
		self.setMenuBar( menuBar )	
