
from PySide import QtCore, QtGui

class Itemlist(QtGui.QWidget):
	"""docstring for Itemlist"""

	def create( self, items=[], click=None, dbclick=None ):

		itemList = QtGui.QListWidget()
		self.add( itemList=itemList, items=items )

		# actions
		if click : itemList.itemClicked.connect( click )
		if dbclick : itemList.itemDoubleClicked.connect( dbclick )

		return itemList

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

	def add(self, itemList=None, items=[], append=True, sort=True ):

		# remove all item if append egal False
		if append == False : self.remove( itemList=itemList, all=True )

		# add items in itemList
		for item in items:
			itemList.addItem( item )

		# class items
		if sort : itemList.sortItems()

	def remove(self, itemList=None, items=None, all=False ):

		# save the keep items
		if all == False:
			keepItems = []
			for item in  self.list( itemList=itemList ) :
				if not item in items : keepItems.append( item )

		# remove all
		itemList.clear()

		# add the keep items
		if all == False:
			self.add( itemlist=itemList, items=keepItems )

	@staticmethod
	def list( itemList=None, selected=False ):

		if selected == False:
			items = []
			for item in range( itemList.count() ) : items.append( itemList.item(item) )
			return items

		else :
			return itemList.selectedItems()
