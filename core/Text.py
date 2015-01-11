
from PySide import QtCore, QtGui

class Text( QtGui.QLabel ):
	"""docstring for Text"""
	def __init__( self, text='defaultText', x=0, y=0, w=100, h=25 ):
		super( Text, self ).__init__()
		self.setText( text )
		self.setGeometry( x, y, w, h )
