
from PySide import QtCore, QtGui

class Layout( QtGui.QWidget ):
	"""docstring for Layout"""
	def __init__( self, parent=None, x=None, y=None, w=None, h=None, scroll=False, margin=[10,10], name=None ):
		super( Layout, self ).__init__()
		if parent:
			self.setParent( parent )
		self.__scroll = scroll
		self.__margin = margin

		self.layout = self

		if self.__scroll:
			self.scrollArea = QtGui.QScrollArea()
			self.scrollArea.setParent( self )
			self.layout = QtGui.QWidget()
			self.scrollArea.setWidget( self.layout )
			# self.layout.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
			# self.layout.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		# define size
		items  = [ x, y, w, h ]
		if parent:
			origin = [ parent.geometry().x(), parent.geometry().y(), parent.geometry().width(), parent.geometry().height() ]
		else:
			origin = [ 0, 0, 50, 50 ]

		values = []
		for i in range( len(items) ):
			if items[i] : values.append( items[i] )
			else : values.append( origin[i] )
		self.setGeometry( values[0], values[1], values[2], values[3] )

		if self.__scroll:
			self.scrollArea.setGeometry( values[0], values[1], values[2]-20, values[3]-20 )

		# init line offset vertical
		self.linesW = self.__margin[0]
		self.linesH = self.__margin[1]

		self.name = name

	def add( self, added=None ):
		try : iter( added )
		except TypeError, te : added = [ added ]

		offsetX = self.__margin[1]
		offsetY = 0
		for item in added :
			item.setParent( self.layout )
			item.setVisible( True )

			x = item.geometry().x()
			y = item.geometry().y()
			w = item.geometry().width()
			h = item.geometry().height()

			item.setGeometry( offsetX, self.linesH, w, h )

			# increment line offset horizontal
			offsetX += w + 10

			if offsetY < h : offsetY = h

		# increment line offset height and width
		self.linesH += offsetY + 5
		if self.linesW < offsetX:
			self.linesW = offsetX

		# resize the layout in the case of a scroll
		if self.__scroll : self.layout.resize( self.linesW+self.__margin[0], self.linesH+self.__margin[1] )

	def clean( self ):
		self.linesH = self.__margin[1]
		for children in self.getChildren():
			children.setParent( None )
			del children

	def getChildren( self ):
		return self.children()
