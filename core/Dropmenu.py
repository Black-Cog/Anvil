
from PySide import QtCore, QtGui

class Dropmenu( QtGui.QComboBox ):
	"""docstring for Dropmenu"""
	def __init__( self, items=[], w=70, h=25, x=0, y=0, name=None ):
		super( Dropmenu, self ).__init__()
		self.setGeometry( x, y, w, h )
		self.__items = {}
		self.add( items=items )

		self.name = name

	def value( self ):

		return self.currentText()

	def getData( self ):
		currentText = self.currentText()
		return currentText

	def getValue( self ):
		currentText = self.currentText()
		
		for key, value in self.__items.iteritems():
			if value == currentText:
				return key

	def add(self, items=[], append=True, sort=True ):

		# TODO add append and sort functions
		for item in items:
			if isinstance( item, dict):
				self.__items.update( item )				
				if isinstance( item.values()[0], str):
					self.addItems( [item.values()[0]] )
					# print [item.values()[0]]
	def remove(self, items=None, all=False ):

		# TODO add check if items list
		# TODO add removeAll function
		for item in items:
			self.removeItem( item )

	def list( self, data=False ):

		if data:
			return self.__items.values()

		else:
			return self.__items.keys()
