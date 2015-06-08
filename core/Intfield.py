
from PySide import QtGui, QtCore

class Intfield( QtGui.QLineEdit ):
	"""docstring for Intfield"""
	def __init__(self, value=1, min=0, max=2048, w=70, h=25, x=0, y=0 ):
		super(Intfield, self).__init__()
		self.setText( str(value) )
		self.setGeometry( x, y, w, h )
		self.min = min
		self.max = max
		self.textChanged.connect(self.__formatInput)
		self.editingFinished.connect(self.__checkInput)

		self.installEventFilter( self )

	def getValue( self ):
		return int( self.text() )

	def __checkMinMax( self ):
		if int( self.text() ) < self.min:
			self.setText( str(self.min) )
		if int( self.text() ) > self.max:
			self.setText( str(self.max) )

	def __checkInput(self):
		if self.text() == '-':
			self.setText( '0' )
		self.__checkMinMax()

	def __formatInput(self):
		text = self.text()
		number = [ '0', '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9', '-' ]

		if text != '' and not text[-1] in number:
			text = text[:-1]
		self.setText( text )
		self.__checkMinMax()

	def __editValue(self, style):
		value  = self.text()
		length = len( value )
		position = self.cursorPosition()
		digit    = length - position

		if position == len( value ) :
			return

		value = float( value )

		if   style == 'up'   : value += eval( '1e%s' %(digit-1) )
		elif style == 'down' : value -= eval( '1e%s' %(digit-1) )

		value = str( int(value) )
		self.setText( value )

		# fix curent decimal during decrease
		# if len( self.text() ) < length:
		# 	value = '0' + value
		# 	self.setText( value )
		# if '0-' in self.text():
		# 	value = self.text().replace( '0-', '-0' )
		# 	print value
		# 	self.setText( value )

		# adjust cursor position
		foo = len( self.text() ) - digit
		self.setCursorPosition( foo )

	def eventFilter( self, widget, event ):
		if ( event.type() == QtCore.QEvent.KeyPress and widget is self ):
			key = event.key()
			if key == QtCore.Qt.Key_Up:
				self.__editValue( 'up' )
			elif key == QtCore.Qt.Key_Down:
				self.__editValue( 'down' )
			elif key == QtCore.Qt.WA_UnderMouse:
				print 'mouse'

		return QtGui.QWidget.eventFilter(self, widget, event)

	# todo : add basic expression system 
	def expression(self):
		return
