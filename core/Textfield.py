
from PySide import QtCore, QtGui

class Textfield( QtGui.QLineEdit ):
	"""docstring for Textfield"""
	def __init__( self, text='', enable=True, x=0, y=0, w=200, h=25 ):
		super( Textfield, self ).__init__()
		self.setText( text )
		self.setEnabled( enable )
		self.setGeometry( x, y, w, h )
