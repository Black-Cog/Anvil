
from PySide import QtGui, QtCore

class Box(QtGui.QPushButton):
	"""docstring for Box"""

	def create( self, parent=None, name='defaultBox', w=400, h=300, x=10, y=20 ):
		
		box = QtGui.QGroupBox( name, parent )

		box.setGeometry( x, y, w, h )

		return box