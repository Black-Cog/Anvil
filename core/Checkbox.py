
from PySide import QtCore, QtGui

class Checkbox( QtGui.QCheckBox ):
	"""docstring for Checkbox"""
	def __init__( self, value=False, w=25, h=25, x=0, y=0 ):
		super( Checkbox, self ).__init__()

		if value == False : stateValue = QtCore.Qt.Unchecked
		elif value == True : stateValue = QtCore.Qt.Checked

		self.setCheckState( stateValue )
		self.setGeometry( x, y, w, h )

	def getValue( self ):
		if self.checkState() == QtCore.Qt.CheckState.Checked:
			return True
		else:
			return False
