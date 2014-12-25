
from PySide import QtGui, QtCore

class Button(QtGui.QPushButton):
	"""docstring for Button"""

	def create( self, name='button', cmd=None, font='Arial', size=10, w=70, h=25, x=0, y=0 ):
		bt = QtGui.QPushButton( name )
		bt.setGeometry( x, y, w, h )
		bt.clicked.connect( cmd )

		return bt