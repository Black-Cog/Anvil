
from PySide import QtGui, QtCore

class Button( QtGui.QPushButton ):
	"""docstring for Button"""
	def __init__(self, name='button', cmd=None, font='Arial', size=10, w=70, h=25, x=0, y=0, icon=None, iconSize=[32,32] ):
		super(Button, self).__init__()
		self.setText( name )
		self.setGeometry( x, y, w, h )
		self.clicked.connect( cmd )

		self.name = name

		if icon:
			self.setIcon( QtGui.QIcon( icon ) )
			self.setIconSize( QtCore.QSize(iconSize[0], iconSize[1]) )
