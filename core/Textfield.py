
from PySide import QtCore, QtGui

class Textfield(QtGui.QWidget):
	"""docstring for Textfield"""

	def create( self, text='', enable=True ):

		textField = QtGui.QLineEdit()

		textField.setText( text )
		textField.setEnabled( enable )

		return textField