
from PySide import QtGui, QtCore

class Intfield( QtGui.QSpinBox ):
	"""docstring for Intfield"""
	def __init__(self, value=1, min=0, max=2048, w=70, h=25, x=0, y=0 ):
		super(Intfield, self).__init__()
		self.setMinimum( min )
		self.setMaximum( max )
		self.setValue( value )
		self.setGeometry( x, y, w, h )
		self.setButtonSymbols( QtGui.QAbstractSpinBox.NoButtons )

	def getValue( self ):
		return self.value()
