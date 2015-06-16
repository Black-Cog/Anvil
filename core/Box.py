
from PySide import QtGui, QtCore

class Box( QtGui.QGroupBox ):
	"""docstring for Box"""	
	def __init__( self, parent=None, name='defaultBox', w=400, h=300, x=10, y=20 ):
		super( Box, self ).__init__()
		self.setParent( parent )
		self.setTitle( name )
		self.setGeometry( x, y, w, h )

		self.name = name
