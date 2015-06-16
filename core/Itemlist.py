
from PySide import QtCore, QtGui

class Itemlist( QtGui.QListWidget ):
	"""docstring for Itemlist"""
	def __init__( self, parent=None, items=[], click=None, dbclick=None, x=0, y=0, w=200, h=200, name=None ):
		super( Itemlist, self ).__init__()
		self.setParent( parent )
		self.setGeometry( x, y, w, h )

		self.add( items=items )

		# actions
		if click : self.itemClicked.connect( click )
		if dbclick : self.itemDoubleClicked.connect( dbclick )

		self.name = name

	@staticmethod
	def itemConvert( dic={} ):

		items = []
		# add items in itemList
		for item in range( len(dic) ):
			addedItem = QtGui.QListWidgetItem( QtGui.QIcon( dic[item][1] ), dic[item][0] )

			# conversion rgb 0/1 to 0/255
			red   = dic[item][2][0] * 255
			green = dic[item][2][1] * 255
			blue  = dic[item][2][2] * 255

			addedItem.setForeground( QtGui.QColor(red, green, blue) )
			items.append( addedItem )

		return items

	def add(self, items=[], append=True, sort=True ):

		# remove all item if append egal False
		if append == False : self.remove( all=True )

		# add items in itemList
		for item in items :	self.addItem( item )

		# class items
		if sort : self.sortItems()

	def remove(self, items=None, all=False ):

		# save the keep items
		if all == False:
			keepItems = []
			for item in  self.list() :
				if not item in items : keepItems.append( item )

		# remove all
		self.clear()

		# add the keep items
		if all == False : self.add( items=keepItems )

	def list( self, selected=False ):

		if selected == False:
			items = []
			for item in range( self.count() ) : items.append( self.item(item) )
			return items

		else : return self.selectedItems()
