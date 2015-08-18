from PySide import QtGui, QtCore
import math
import Anvil.core
import Forge.core

# todo : refactor and implement better colorspace managment
class Colorpicker(QtGui.QWidget):

    def __init__( self, color=[ .5, .5, .5 ], x=0, y=0, w=500, h=50, name=None ):
        super(Colorpicker, self).__init__()
        self.setGeometry( x, y, w, h )
        self.color = Forge.core.Color( color )
        self.fieldChange = True

        self.name = name

        # define class
        Alayout     = Anvil.core.Layout
        Afloatfield = Anvil.core.Floatfield
        Abutton     = Anvil.core.Button

        # define layout
        layout_main = Alayout( parent=self )

        # define floatfield
        self.floatfield_red   = Afloatfield( value=self.color[0] )
        self.floatfield_green = Afloatfield( value=self.color[1] )
        self.floatfield_blue  = Afloatfield( value=self.color[2] )
        self.floatfield_red.valueChanged.connect(self._updateColor)
        self.floatfield_green.valueChanged.connect(self._updateColor)
        self.floatfield_blue.valueChanged.connect(self._updateColor)

        # buttons init
        self.colorDisplay = Abutton( name='', cmd=self.showPopup )

        # palettes init
        self.plt = self.colorDisplay.palette()
        self.updateDisplay( self )

        # define layouts content
        layout_main.add( [self.floatfield_red, self.floatfield_green, self.floatfield_blue, self.colorDisplay] )

    def _updateColor( self ):
        if self.fieldChange:
            self.color.setRgb([ self.floatfield_red.value(), self.floatfield_green.value(), self.floatfield_blue.value()] )
            self.updateDisplay( self )
        else:
            self.fieldChange = True

    def updateDisplay( self, source, field=False ):
        source.plt.setColor( source.colorDisplay.backgroundRole(), QtGui.QColor(
            max( min( self.color.getR255(), 255 ), 0 ),
            max( min( self.color.getG255(), 255 ), 0 ),
            max( min( self.color.getB255(), 255 ), 0 )
        ) )

        source.colorDisplay.setPalette( source.plt )

        if field:
            self.floatfield_red.setValue( self.color[0] )
            self.fieldChange = False
            self.floatfield_green.setValue( self.color[1] )
            self.fieldChange = False
            self.floatfield_blue.setValue( self.color[2] )
            self.fieldChange = False

    def showPopup( self ):
        self.popup = _Popup( source=self )
        self.popup.show()

    def getValue( self ):
        return self.color


class _Popup( QtGui.QWidget ):
    def __init__( self, source ):
        self.source = source

        super(_Popup, self).__init__()
        self.resize( 250, 550 )
        self.setWindowTitle('Color Picker')
        self.fieldChange = False

        # define class
        Alayout     = Anvil.core.Layout
        Afloatfield = Anvil.core.Floatfield
        Abutton     = Anvil.core.Button
        Atext       = Anvil.core.Text

        # define layout
        layout_main = Alayout( parent=self )

        # buttons init
        self.colorDisplay = Abutton( name='', cmd=self.__dummy )
        # palettes init
        self.plt = self.colorDisplay.palette()
        self.plt.setColor( self.colorDisplay.backgroundRole(), QtGui.QColor(self.source.color.getR255(), self.source.color.getG255(), self.source.color.getB255()) )
        self.colorDisplay.setPalette( self.plt )

        # define texts
        self.text_hue        = Atext( text='   H', w=30 )
        self.text_saturation = Atext( text='   S', w=30 )
        self.text_value      = Atext( text='   V', w=30 )
        self.text_red        = Atext( text='   R', w=30 )
        self.text_green      = Atext( text='   G', w=30 )
        self.text_blue       = Atext( text='   B', w=30 )

        # define floatfield
        self.floatfield_hue        = Afloatfield( value=self.source.color['h'], w=30 )
        self.floatfield_saturation = Afloatfield( value=self.source.color['s'], w=30 )
        self.floatfield_value      = Afloatfield( value=self.source.color['v'], w=30 )
        self.floatfield_red        = Afloatfield( value=self.source.color[0]  , w=30 )
        self.floatfield_green      = Afloatfield( value=self.source.color[1]  , w=30 )
        self.floatfield_blue       = Afloatfield( value=self.source.color[2]  , w=30 )

        # define floatfield actions
        action_hue        = lambda : self.__updateByField( 'h' )
        action_saturation = lambda : self.__updateByField( 's' )
        action_value      = lambda : self.__updateByField( 'v' )
        action_red        = lambda : self.__updateByField( 'r' )
        action_green      = lambda : self.__updateByField( 'g' )
        action_blue       = lambda : self.__updateByField( 'b' )
        self.floatfield_hue.valueChanged.connect( action_hue )
        self.floatfield_saturation.valueChanged.connect( action_saturation )
        self.floatfield_value.valueChanged.connect( action_value )
        self.floatfield_red.valueChanged.connect( action_red )
        self.floatfield_green.valueChanged.connect( action_green )
        self.floatfield_blue.valueChanged.connect( action_blue )

        # define wheel
        self.draw_wheel = _Wheel( self.source )

        # define sliders
        self.slider_hue        = _ComponentSlider( component=0, source=self.source )
        self.slider_value      = _ComponentSlider( component=1, source=self.source )
        self.slider_saturation = _ComponentSlider( component=2, source=self.source )
        self.slider_red        = _ComponentSlider( component=3, source=self.source )
        self.slider_green      = _ComponentSlider( component=4, source=self.source )
        self.slider_blue       = _ComponentSlider( component=5, source=self.source )

        # define layouts content
        layout_main.add( [self.colorDisplay] )
        layout_main.add( [self.text_hue, self.text_saturation, self.text_value, self.text_red, self.text_green, self.text_blue] )
        layout_main.add( [self.floatfield_hue, self.floatfield_saturation, self.floatfield_value, self.floatfield_red, self.floatfield_green, self.floatfield_blue] )
        layout_main.add( [self.slider_hue, self.slider_saturation, self.slider_value, self.slider_red, self.slider_green, self.slider_blue] )
        layout_main.add( [self.draw_wheel] )

    def __updateByField( self, channel ):
        if self.fieldChange:
            if channel == 'h' and self.source.color['h'] != self.floatfield_hue.value() :
                self.source.color['h'] = self.floatfield_hue.value()
                self.update()
            elif channel == 's' and self.source.color['s'] != self.floatfield_saturation.value() :
                self.source.color['s'] = self.floatfield_saturation.value()
                self.update()
            elif channel == 'v' and self.source.color['v'] != self.floatfield_value.value() :
                self.source.color['v'] = self.floatfield_value.value()
                self.update()
            elif channel == 'r' and self.source.color['r'] != self.floatfield_red.value() :
                self.source.color['r'] = self.floatfield_red.value()
                self.update()
            elif channel == 'g' and self.source.color['g'] != self.floatfield_green.value() :
                self.source.color['g'] = self.floatfield_green.value()
                self.update()
            elif channel == 'b' and self.source.color['b'] != self.floatfield_blue.value() :
                self.source.color['b'] = self.floatfield_blue.value()
                self.update()
        else:
            self.fieldChange = True

    def setColorPopup( self, color=None ):
        if color:
            self.source.color.setRgb( color )
        self.source.updateDisplay( source=self )
        self.source.updateDisplay( source=self.source, field=True )

    def __dummy( self ):
        # dummy method
        pass

    def update( self ):
        # update
        self.draw_wheel.updateWheel( change=True )

        self.slider_hue.setValue( self.source.color.getHue() )
        self.slider_saturation.setValue( self.source.color.getSaturation() )
        self.slider_value.setValue( self.source.color.getValue() )
        self.slider_red.setValue( value=self.source.color[0] )
        self.slider_green.setValue( value=self.source.color[1] )
        self.slider_blue.setValue( value=self.source.color[2] )

        self.fieldChange = False
        self.floatfield_hue.setValue( self.source.color.getHue() )
        self.fieldChange = False
        self.floatfield_saturation.setValue( self.source.color.getSaturation() )
        self.fieldChange = False
        self.floatfield_value.setValue( self.source.color.getValue() )
        self.fieldChange = False
        self.floatfield_red.setValue( self.source.color[0] )
        self.fieldChange = False
        self.floatfield_green.setValue( self.source.color[1] )
        self.fieldChange = False
        self.floatfield_blue.setValue( self.source.color[2] )

    def setColor( self, color ):
        self.source.color.setRgb( color )
        self.source.updateDisplay( source=self )
        self.source.updateDisplay( source=self.source, field=True )


class _ComponentSlider(QtGui.QWidget):
    def __init__( self, component=4, direction='vertical', source=None ):
        self.source = source
        super(_ComponentSlider, self).__init__()
        self.resize( 30, 200 )

        self.direction = 1
        if direction == 'horizontal' : self.direction = 0

        self.hueId        = 0
        self.valueId      = 1
        self.saturationId = 2
        self.redId        = 3
        self.greenId      = 4
        self.blueId       = 5
        self._component   = component

        if component == self.hueId :
            self.color1 = QtGui.QColor( 255, 0, 0 )
            self.color2 = QtGui.QColor( 0, 255, 0 )
            self.color3 = QtGui.QColor( 0, 0, 255 )
            value  = self.source.color['h']

        elif component == self.valueId :
            self.color1 = QtGui.QColor(   0,   0,   0 )
            self.color2 = QtGui.QColor( 255, 255, 255 )
            value  = self.source.color['v']

        elif component == self.saturationId :
            self.color1 = QtGui.QColor( 123, 123, 123 )
            self.color2 = QtGui.QColor( 255, 0, 0 )
            value  = self.source.color['s']

        elif component == self.redId :
            self.color1 = QtGui.QColor(   0, 0, 0 )
            self.color2 = QtGui.QColor( 255, 0, 0 )
            value  = self.source.color[0]

        elif component == self.greenId :
            self.color1 = QtGui.QColor( 0,   0, 0 )
            self.color2 = QtGui.QColor( 0, 255, 0 )
            value  = self.source.color[1]

        elif component == self.blueId :
            self.color1 = QtGui.QColor( 0, 0,   0 )
            self.color2 = QtGui.QColor( 0, 0, 255 )
            value  = self.source.color[2]

        self.setValue( value )

    def paintEvent( self, event ):
        rect = self.rect()
        painter = QtGui.QPainter( self )
        painter.save()
        painter.setRenderHint( QtGui.QPainter.Antialiasing )

        if self.direction == 1:
            gradient = QtGui.QLinearGradient(rect.bottomLeft(), rect.topLeft())
        else:
            gradient = QtGui.QLinearGradient(rect.topLeft(), rect.topRight())

        if self._component == self.hueId :
            gradient.setColorAt(0,    self.color1)
            gradient.setColorAt(0.33, self.color2)
            gradient.setColorAt(0.66, self.color3)
            gradient.setColorAt(1,    self.color1)
        else:
            gradient.setColorAt(0, self.color1)
            gradient.setColorAt(1, self.color2)
        painter.fillRect(rect, gradient)

        component = self.__getComponentValue()
        if self.direction == 1:
            pos = rect.height() - component * (rect.bottom() - rect.top())
            line2 = QtCore.QLineF(rect.left(), pos, rect.right(), pos)
            line1 = line2.translated(0, -1)
            line3 = line2.translated(0, 1)
        else:
            pos = component * (rect.right() - rect.left())
            line2 = QtCore.QLineF(pos, rect.top(), pos, rect.bottom())
            line1 = line2.translated(-1, 0)
            line3 = line2.translated(1, 0)

        pen = QtGui.QPen()
        pen.setWidth(1)
        painter.setRenderHint( QtGui.QPainter.Antialiasing, False )

        pen.setColor( QtGui.QColor(0, 0, 0) )
        painter.setPen( pen )
        painter.drawLine( line1 )
        pen.setColor( QtGui.QColor(255, 255, 255) )
        painter.setPen( pen )
        painter.drawLine( line2 )
        pen.setColor( QtGui.QColor(0, 0, 0) )
        painter.setPen( pen )
        painter.drawLine( line3 )

        painter.restore()

    def __getComponentValue(self):
        if self._component == self.redId        : return self.source.color[0]
        if self._component == self.greenId      : return self.source.color[1]
        if self._component == self.blueId       : return self.source.color[2]
        if self._component == self.hueId        : return self.source.color['h']
        if self._component == self.saturationId : return self.source.color['s']
        if self._component == self.valueId      : return self.source.color['v']

    def __updateDisplay(self, value):
        if self._component in [ self.redId, self.greenId, self.blueId ]:
            r = value if self._component == self.redId else self.source.color[0]
            g = value if self._component == self.greenId else self.source.color[1]
            b = value if self._component == self.blueId else self.source.color[2]
            self.source.color.setRgb( [r, g, b] )

        elif self._component in [ self.hueId, self.saturationId, self.valueId ]:
            h = value if self._component == self.hueId else self.source.color.getHue()
            s = value if self._component == self.saturationId else self.source.color.getSaturation()
            v = value if self._component == self.valueId else self.source.color.getValue()
            self.source.color.setHsv( [h, s, v] )

        else:
            return

        self.repaint()

    def __clamp(self, val, minimum, maximum):
        if val < minimum:
            val = minimum
        elif val > maximum:
            val = maximum
        return val

    def __updateSliderPosition(self, pos):
        rect = self.rect()

        if self.direction == 1:
            top = rect.top()
            bottom = rect.bottom()
            component_value = 1 - float(self.__clamp(pos.y(), top, bottom)) / float(bottom - top)
        else:
            left = rect.left()
            right = rect.right()
            component_value = float( self.__clamp(pos.x(), left, right)) / float(right - left)

        self.__updateDisplay(component_value)

    def mousePressEvent(self, event):
        # on click
        self.updateSlider( event )

    def mouseMoveEvent(self, event):
        # on move
        self.updateSlider( event )

    def updateSlider( self, event ):
        self.__updateSliderPosition(event.pos())
        self.source.popup.update()

    def setValue( self, value ):
        # set slider value
        self.__updateDisplay( value )

    def getValue( self ):
        if self._component == 0 : return self.source.color['h']
        if self._component == 1 : return self.source.color['v']
        if self._component == 2 : return self.source.color['s']
        if self._component == 3 : return self.source.color[0]
        if self._component == 4 : return self.source.color[1]
        if self._component == 5 : return self.source.color[2]


class _Wheel( QtGui.QWidget ):
    def __init__( self, source ):
        self.source = source
        super(_Wheel, self).__init__()

        self.setGeometry( 0, 0, 225, 225 )
        self.setFocusPolicy( QtCore.Qt.ClickFocus )

        self.__wheelImage = None
        self._marker_pos = QtCore.QPointF(0, 0)
        self.setMinimumSize(10, 10)

    def __length( self, p1, p2 ):
        # return length
        return math.sqrt( self.__length2(p1, p2) )

    def __length2( self, p1, p2 ):
        # return length2
        return pow( (p2.x() - p1.x()), 2) + pow((p2.y() - p1.y()), 2 )

    def __updateColorWheel( self, pos ):
        square = self.__square()

        radius = square.width() * 0.5
        line = QtCore.QLineF(square.center(), pos)
        distance = self.__length(line.p1(), line.p2())

        if distance > radius : distance = radius

        line.setAngle(line.angle() + 90.0)
        h = (360.0 - line.angle()) / 360.0
        s = distance / radius
        v = self.source.color.getValue()

        self.source.color.setHsv([h, s, v])

    def __square( self ):
        rect = self.rect()
        w = rect.width()
        h = rect.height()
        if w > h:
            offset = (w - h) * 0.5
            rect.setWidth(h)
            rect.moveLeft(rect.left() + offset)
        else:
            offset = (h - w) * 0.5
            rect.setHeight(w)
            rect.moveTop(rect.top() + offset)
        return rect

    def __updateMarkerPosition( self ):
        square = self.__square()
        radius = square.width() * 0.5

        hue = self.source.color.getHue()
        sat = self.source.color.getSaturation()

        distance = sat * radius
        center = square.center()
        line = QtCore.QLineF( center.x(), center.y(), center.x(), center.y() + distance )
        line.setAngle(360.0 - hue * 360.0)
        line.setAngle(line.angle() - 90)

        self._marker_pos = line.p2()

    def __rebuildColorWheel( self ):
        image_format = QtGui.QImage.Format_ARGB32_Premultiplied
        self.__wheelImage = QtGui.QImage( self.__square().size(), image_format )
        self.__wheelImage.fill( 0 )
        rect = self.__wheelImage.rect()
        painter = QtGui.QPainter( self.__wheelImage )
        painter.save()
        painter.setRenderHint( QtGui.QPainter.Antialiasing )
        pen = QtGui.QPen()
        pen.setColor( QtCore.Qt.transparent )
        painter.setPen( pen )
        painter.setBrush( QtCore.Qt.transparent )
        painter.drawRect( rect )

        radius = rect.width() * 0.5
        path = QtGui.QPainterPath()
        path.addEllipse( rect )
        painter.setClipPath( path )

        hue = QtGui.QConicalGradient( rect.center(), -90 )
        color = QtGui.QColor()
        step = 0
        value = self.source.color.getValue()
        while step < 1.0:
            color.setHsvF( 1 - step, 1, value )
            hue.setColorAt( step, color )
            step += 0.1
        painter.fillPath( path, hue )

        # Saturation. May not be completely accurate,
        # but it's only used as a visual representation
        saturation = QtGui.QRadialGradient( rect.center(), radius )
        color.setRgbF( value, value, value )
        color.setAlphaF( 1 )
        saturation.setColorAt( 0, color )
        color.setRgbF( value, value, value )
        color.setAlphaF( 0 )
        saturation.setColorAt( 1, color )
        painter.fillPath( path, saturation )
        painter.restore()

        self.repaint()

    def resizeEvent( self, event ):
        self.__rebuildColorWheel()
        self.__updateMarkerPosition()
        return super(_Wheel, self).resizeEvent(event)

    def paintEvent( self, event ):
        painter = QtGui.QPainter( self )
        painter.save()
        painter.setRenderHint( QtGui.QPainter.Antialiasing )
        painter.setClipRect( self.rect() )
        painter.drawImage( self.__square(), self.__wheelImage )

        pen = QtGui.QPen()
        v = 0 if self.source.color.getValue() > 0.5 else 255
        pen.setColor( QtGui.QColor(v, v, v) )
        painter.setPen( pen )
        marker = QtCore.QRectF( self._marker_pos.x() - 2, self._marker_pos.y() - 2, 5, 5 )

        # angles are specified in 1/16 of a degree; draws a full circle
        painter.drawArc( marker, 0, 5760 )
        painter.restore()

    def mousePressEvent( self, event ):
        # on click
        self.updateWheel( event=event, change=True )
        self.source.popup.update()

    def mouseMoveEvent( self, event ):
        # on move
        self.updateWheel( event=event, change=True )
        self.source.popup.update()

    def mouseReleaseEvent( self, event ):
        # callback
        self.source.popup.update()
        pass

    def updateWheel( self, event=False, change=False ):
        if change : 
            if event:
                position = event.pos()
            else:
                square = self.__square()
                radius = square.width() * 0.5
                distance = self.source.color.getSaturation() * radius
                center = square.center()
                line = QtCore.QLineF( center.x(), center.y(), center.x(), center.y() + distance )
                line.setAngle( 360.0 - self.source.color.getHue() * 360.0 )
                line.setAngle( line.angle() - 90 )

                position = line.p2()

            self.__updateColorWheel( position )
            self.__updateMarkerPosition()
            self.__rebuildColorWheel()

            self.source.popup.setColorPopup()
