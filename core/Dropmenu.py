
from PySide import QtCore, QtGui

class Dropmenu( QtGui.QComboBox ):
	"""docstring for Dropmenu"""
	def __init__( self, items=[], w=70, h=25, x=0, y=0, name=None ):
		super( Dropmenu, self ).__init__()
		self.setGeometry( x, y, w, h )
		self.add( items=items )

		self.name = name

	def value( self ):

		return self.currentText()

	def add(self, items=[], append=True, sort=True ):

		# TODO add append and sort functions
		self.addItems( items )

	def remove(self, items=None, all=False ):

		# TODO add check if items list
		# TODO add removeAll function
		for item in items:
			self.removeItem( item )

	def list( self ):

		# TODO add list fucntion
		return None
