
from PySide import QtGui, QtCore

class Tab( QtGui.QTabWidget ):
	"""docstring for Tab"""	
	def __init__( self, parent=None, tabs=None, name=None ):
		super( Tab, self ).__init__()

		if tabs:
			for tab in tabs : self.addTab( QtGui.QWidget(), tab )

		parent.setCentralWidget( self )

		self.name = name
