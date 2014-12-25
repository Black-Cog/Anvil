
from PySide import QtCore, QtGui

class Window(QtGui.QWidget):
	"""docstring for Window"""

	def create( self, title='undefind', size=[500, 400] ):
		w = QtGui.QWidget()
		w.setWindowTitle( title )
		w.resize( size[0], size[1] )

		self.mainLayout( win=w )

		return w

	@staticmethod
	def mainLayout( win ):
		win.menuBar    = QtGui.QMenuBar()
		win.fileMenu   = QtGui.QMenu("File", win)
		win.helpAction = win.fileMenu.addAction("Help")
		win.exitAction = win.fileMenu.addAction("Exit")
		win.content    = QtGui.QVBoxLayout()

		win.menuBar.addMenu( win.fileMenu )
		win.content.setMenuBar(win.menuBar)
		win.setLayout(win.content)

	def addBox( self, box=None ):
		# w.mainLayout.addWidget( box_general )
		self.w.content.addWidget( box )