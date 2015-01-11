
from PySide import QtCore, QtGui

class Layout( QtGui.QWidget ):
	"""docstring for Layout"""
	def __init__( self, parent=None, x=None, y=None, w=None, h=None ):
		super( Layout, self ).__init__()
		self.setParent( parent )

		# define size
		items  = [ x, y, w, h ]
		origin = [ parent.geometry().x(), parent.geometry().y(), parent.geometry().width(), parent.geometry().height() ]
		values = []
		for i in range( len(items) ):
			if items[i] : values.append( items[i] )
			else : values.append( origin[i] )
		self.setGeometry( values[0], values[1], values[2], values[3] )

		# init line offset vertical
		self.linesH = 0

	def add( self, added=None ):
		try : iter( added )
		except TypeError, te : added = [ added ]

		offsetX = 0
		offsetY = 0
		for item in added :
			item.setParent( self )

			x = item.geometry().x()
			y = item.geometry().y()
			w = item.geometry().width()
			h = item.geometry().height()

			item.setGeometry( offsetX, self.linesH, w, h )

			# increment line offset horizontal
			offsetX += w + 10

			if offsetY < h : offsetY = h

		# increment line offset vertical
		self.linesH += offsetY + 5

