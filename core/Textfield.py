
from PySide import QtCore, QtGui

class Textfield( QtGui.QLineEdit ):
	"""docstring for Textfield"""
	def __init__( self, text='', enable=True, x=0, y=0, w=200, h=25, name=None ):
		super( Textfield, self ).__init__()
		self.setText( text )
		self.setEnabled( enable )
		self.setGeometry( x, y, w, h )

		self.name = name

	def getValue( self ):
		return self.text()

	def setValue( self, value ):
		self.setText( value )

