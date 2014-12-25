
from PySide import QtCore, QtGui

class Text(QtGui.QWidget):
	"""docstring for Text"""

	def create( self, parent=None, text='defaultText' ):

		text = QtGui.QLabel( text )

		return text