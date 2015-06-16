
from PySide import QtGui, QtCore

class Tree( QtGui.QTreeView ):
	def __init__( self, x=0, y=0, w=400, h=300, lineH=35, name=None ):
		super(Tree, self).__init__()
		self.setGeometry( x, y, w, h )
		self.__lineH = lineH

		# signals
		self.c = _Communicate()
		self.signalKeySpacePress = self.c.signalKeySpacePress
		self.signalLeftClick = self.c.signalLeftClick
		self.signalRightClick = self.c.signalRightClick
		self.signalDoubleClick = self.c.signalDoubleClick

		self.name = name

	def add( self, items ):
		'''
		items need to be format like that : [ { 'name':'', 'id':1, 'iconPath':'', 'tooltip':'', 'iconTooltip':'', 'parentId':None, }, ]
		'''

		root_model = QtGui.QStandardItemModel()
		self.setModel( root_model )
		self.__populateTree(items, root_model.invisibleRootItem())
		self.setHeaderHidden(True)

	def __populateTree(self, items, parent):
		orderItems = self.__formatList( items )

		for item in orderItems:
			icon = _Icon( item['iconPath'], item['iconTooltip'] )

			newItem = _Item( item['name'] )
			newItem.setItemId( item['id'] )
			newItem.setToolTip( item['tooltip'] )
			newItem.setIcon( icon.pixmap )
			newItem.setSizeHint( QtCore.QSize(self.__lineH, self.__lineH) )

			if not item['parentId']:
				parent.appendRow(newItem)
			else:
				# define childrenList
				childList = []
				for i in range( parent.rowCount() ) : childList.append( parent.child(i) )

				for childItem in childList:
					# add children in the childList
					for j in range( childItem.rowCount() ) : childList.append( childItem.child(j) )

					if childItem.itemId == item['parentId']:
						childItem.appendRow( newItem )
						break

	def __formatList( self, items ):
		newList = []
		dirtyList = []

		for item in items:
			name   = item['id']
			parent = item['parentId']

			if not parent:
				newList.append( item )
				dirtyList.append( name )
			elif parent in dirtyList:
				newList.append( item )
				dirtyList.append( name )
			else:
				items.append( item )

		return newList

	def keyPressEvent( self, event ):
		k = event.key()
		if k == QtCore.Qt.Key_Space:
			self.signalKeySpacePress.emit()

		super(Tree, self).keyPressEvent(event)

	def mouseReleaseEvent( self, event ):
		if event.button() == QtCore.Qt.LeftButton:
			self.signalLeftClick.emit()

		if event.button() == QtCore.Qt.RightButton:
			self.signalRightClick.emit()

		super(Tree, self).mouseReleaseEvent(event)

	def mouseDoubleClickEvent(self, event):
		self.signalDoubleClick.emit()

		super(Tree, self).mouseDoubleClickEvent(event)

	def getCurrentItemId( self ):
		'''
		return the itemId of the current item.
		'''
		index = self.currentIndex()
		item = self.model().itemFromIndex( index )
		if item:
			itemId = item.itemId

			return itemId

		return None



class _Item( QtGui.QStandardItem ):
	def setItemId( self, itemId ):
		self.itemId = itemId

class _Icon():
	def __init__(self, icon, tooltip, w=50, h=50):
		self.pixmap = QtGui.QPixmap(icon)
		self.tooltip = tooltip
		# todo : fix icon size
		# self.pixmap.scaled( w, h, QtCore.Qt.KeepAspectRatio)
		# self.pixmap.setGeometry( x, y, w, h )
		# self.pixmap.scaledToHeight( h )

class _Communicate( QtCore.QObject ):
	signalKeySpacePress = QtCore.Signal()
	signalLeftClick = QtCore.Signal()
	signalRightClick = QtCore.Signal()
	signalDoubleClick = QtCore.Signal()




'''
# WIP STUFF
#-------------------------------------------------------------------------------
# my test data
class Icon():
	def __init__(self, icon, tooltip):
		self.pixmap = QtGui.QPixmap(icon)
		self.tooltip = tooltip

#-------------------------------------------------------------------------------
# my test data
class MyData():
	def __init__(self, txt, parent=None):
		self.txt = txt
		self.tooltip = None
		self.parent = parent
		self.child = []
		self.icon = []
		self.index = None
		self.widget = None

	#---------------------------------------------------------------------------
	def position(self):
		position = 0
		if self.parent is not None:
			count = 0
			children = self.parent.child
			for child in children:
				if child == self:
					position = count
					break
				count += 1
		return position

	#---------------------------------------------------------------------------
	# test initialization
	@staticmethod
	def init():
		root = MyData("root")
		root.icon.append(Icon("F:/dev/BCgit/icons/check.png", "ToolTip icon.png"))
		root.tooltip = "root tooltip"

		# list objects
		hierarchy = [
			{ 'object_001':{ 'type':'obj',    'child':'' } },
			{ 'object_002':{ 'type':'obj',    'child':'' } },
			{ 'object_003':{ 'type':'obj',    'child':'' } },
			{ 'object_004':{ 'type':'obj',    'child':'' } },
			{ 'object_005':{ 'type':'obj',    'child':'' } },
			{ 'object_006':{ 'type':'obj',    'child':'' } },
			{ 'object_007':{ 'type':'obj',    'child':'' } },
			{ 'light_001': { 'type':'light',  'child':'' } },
			{ 'light_002': { 'type':'light',  'child':'' } },
			{ 'camera_001':{ 'type':'camera', 'child':'' } }
		]

		for i in hierarchy:
			item = MyData( i.keys()[0], root )

			if i.values()[0]['type'] == 'obj':
				iconPath = 'F:/dev/BCgit/icons/master.png'
				tooltipValue = 'Inforamtion about object'
			elif i.values()[0]['type'] == 'light':
				iconPath = 'F:/dev/BCgit/icons/new.png'
				tooltipValue = 'Inforamtion about light'
			elif i.values()[0]['type'] == 'camera':
				iconPath = 'F:/dev/BCgit/icons/edit.png'
				tooltipValue = 'Inforamtion about camera'

			item.icon.append( Icon(iconPath, "ToolTip icon.png") )
			item.tooltip = tooltipValue
			root.child.append( item )

		# for i in range(0, 5):
		# 	child1 = MyData("child %i" % (i), root)
		# 	child1.icon.append(Icon("F:/dev/BCgit/icons/new.png", "ToolTip icon1.png"))
		# 	child1.tooltip = "child1 tooltip"
		# 	root.child.append(child1)
		# 	for x in range(0, 2):
		# 		child2 = MyData("child %i %i" % (i, x), child1)
		# 		child2.icon.append(Icon("F:/dev/BCgit/icons/edit.png", "ToolTip icon1.png"))
		# 		child2.icon.append(Icon("F:/dev/BCgit/icons/master.png", "ToolTip icon2.png"))
		# 		child2.tooltip = "child2 tooltip"
		# 		child1.child.append(child2)

		return root

#-------------------------------------------------------------------------------
class TreeViewModel(QtCore.QAbstractItemModel):
	#---------------------------------------------------------------------------
	def __init__(self, tree):
		super(TreeViewModel, self).__init__()
		self.__tree = tree
		self.__current = tree
		self.__view = None

	#---------------------------------------------------------------------------
	def flags(self, index):
		flag = QtCore.Qt.ItemIsEnabled
		if index.isValid():
			flag |= QtCore.Qt.ItemIsSelectable \
				 | QtCore.Qt.ItemIsUserCheckable \
				 | QtCore.Qt.ItemIsEditable \
				 | QtCore.Qt.ItemIsDragEnabled \
				 | QtCore.Qt.ItemIsDropEnabled
		return flag

	#---------------------------------------------------------------------------
	def index(self, row, column, parent=QtCore.QModelIndex()):
		node = QtCore.QModelIndex()
		if parent.isValid():
			nodeS = parent.internalPointer()
			nodeX = nodeS.child[row]
			node = self.__createIndex(row, column, nodeX)
		else:
			node = self.__createIndex(row, column, self.__tree)
		return node

	#---------------------------------------------------------------------------
	def parent(self, index):
		node = QtCore.QModelIndex()
		if index.isValid():
			nodeS = index.internalPointer()
			parent = nodeS.parent
			if parent is not None:
				node = self.__createIndex(parent.position(), 0, parent)
		return node

	#---------------------------------------------------------------------------
	def rowCount(self, index=QtCore.QModelIndex()):
		count = 1
		node = index.internalPointer()
		if node is not None:
			count = len(node.child)
		return count

	#---------------------------------------------------------------------------
	def columnCount(self, index=QtCore.QModelIndex()):
		return 1

	#---------------------------------------------------------------------------
	def data(self, index, role=QtCore.Qt.DisplayRole):
		data = None
		return data

	#---------------------------------------------------------------------------
	def setView(self, view):
		self.__view = view

	#---------------------------------------------------------------------------
	def __createIndex(self, row, column, node):
		if node.index == None:
			index = self.createIndex(row, column, node)
			node.index = index
		if node.widget is None:
			node.widget = Widget(node)
			self.__view.setIndexWidget(index, node.widget)
		return node.index


#-------------------------------------------------------------------------------
class TreeView(QtGui.QTreeView):
	#---------------------------------------------------------------------------
	def __init__(self, model, parent=None):
		super(TreeView, self).__init__(parent)
		self.setModel(model)
		model.setView(self)
		root = model.index(0, 0)
		self.setCurrentIndex(root)
		self.setHeaderHidden(True)

	#---------------------------------------------------------------------------
	def keyPressEvent(self, event):
		k = event.key()
		if k == QtCore.Qt.Key_F2:
			self.__editMode()

		super(TreeView, self).keyPressEvent(event)

	#---------------------------------------------------------------------------
	def __editMode(self):
		index = self.currentIndex()
		node = index.internalPointer()
		node.widget.editMode(True, True)


#-------------------------------------------------------------------------------
class Label(QtGui.QLabel):
	#---------------------------------------------------------------------------
	def __init__(self, parent, text):
		super(Label, self).__init__(text)
		self.__parent = parent

	#---------------------------------------------------------------------------
	def mouseDoubleClickEvent(self, event):
		#print("mouseDoubleClickEvent")
		if self.__parent is not None:
			self.__parent.editMode(True, True)
		else:
			super(Label, self).mouseDoubleClickEvent(event)


#-------------------------------------------------------------------------------
class LineEdit(QtGui.QLineEdit):
	#---------------------------------------------------------------------------
	def __init__(self, parent, text):
		super(LineEdit, self).__init__(text)
		self.__parent = parent
		self.editingFinished.connect(self.__editingFinished)

	#---------------------------------------------------------------------------
	def keyPressEvent(self, event):
		k = event.key()
		if k == QtCore.Qt.Key_Escape:
			print("ESC 2")
			self.__editingFinished(False)
		super(LineEdit, self).keyPressEvent(event)

	#---------------------------------------------------------------------------
	def __editingFinished(self, bCopy=True):
		print("editingFinished")
		self.__parent.editMode(False, bCopy)

#-------------------------------------------------------------------------------
class Widget(QtGui.QWidget):
	#---------------------------------------------------------------------------
	def __init__(self, node):
		super(Widget, self).__init__()
		self.autoFillBackground()
		self.__node = node
		self.__bEditMode = False
		self.__txt = None
		self.__create(self.__node, self.__bEditMode)

	#---------------------------------------------------------------------------
	def __create(self, node, bEditMode):
		layout = QtGui.QHBoxLayout()
		for icon in node.icon:
			label = Label(None, node.txt)
			label.setPixmap(icon.pixmap)
			label.setToolTip("label tooltip %s %s" % (node.txt, icon.tooltip))
			layout.addWidget(label)

		self.__changeTxt(layout, node, bEditMode, False)
		self.setLayout(layout)

	#---------------------------------------------------------------------------
	def __changeTxt(self, layout, node, bEditMode, bCopy):
		if self.__txt is not None:
			if bCopy:
				node.txt = self.__txt.text()
			if isinstance(self.__txt, LineEdit):
				self.__txt.deselect()
			self.__txt.hide()
			layout.removeWidget(self.__txt)
			self.__txt = None

		if bEditMode:
			self.__txt = LineEdit(self, node.txt)
			self.__txt.setFrame(False)
			self.__txt.selectAll()
			QtCore.QTimer.singleShot(0, self.__txt, QtCore.SLOT('setFocus()'));
		else:
			self.__txt = Label(self, node.txt)
		self.__txt.setToolTip("Text tooltip %s %s" % (node.txt, node.tooltip))
		layout.addWidget(self.__txt, 1)

	#---------------------------------------------------------------------------
	def editMode(self, bEditMode, bCopy):
		if self.__bEditMode != bEditMode:
			self.__bEditMode = bEditMode
			layout = self.layout()
			self.__changeTxt(layout, self.__node, bEditMode, bCopy)

#-------------------------------------------------------------------------------
# class MyTree(QtGui.QMainWindow):
#	 def __init__(self, parent=None):
#		 super(MyTree, self).__init__(parent)

#		 data = MyData.init()
#		 frame = QtGui.QFrame();
#		 frame.setLayout( QtGui.QHBoxLayout() );

#		 treeViewModel = TreeViewModel(data)
#		 treeView = TreeView(treeViewModel)
#		 frame.layout().addWidget( treeView );

#		 self.setCentralWidget(frame)

# class Tree(TreeView):
#	 def __init__(self, treeViewModel):
#	 	super(TreeView, self).__init__(parent)

#		 # data = MyData.init()

#		 # self.treeViewModel = TreeViewModel(data)
#		 self.treeView = TreeView(self.treeViewModel)
		


treeViewModel = TreeViewModel( MyData.init() )

form = TreeView( treeViewModel )
form.show()
'''