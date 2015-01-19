
from PySide import QtGui, QtCore
import math


def _draw_checkerboard(painter, rect, size):
    color1 = QtGui.QColor(153, 153, 152)
    color2 = QtGui.QColor(102, 102, 102)

    painter.save()
    painter.fillRect(rect, color1)
    square = QtCore.QRect(0, 0, size, size)
    step_x = size * 2
    step_y = size
    odd = True
    while square.top() < rect.bottom():
        while square.left() < rect.right():
            painter.fillRect(square, color2)
            square.moveLeft(square.left() + step_x)
        square.moveLeft(0)
        if odd:
            square.moveLeft(square.left() + step_x / 2.0)
        square.moveTop(square.top() + step_y)
        odd = not odd
    painter.restore()


class ColorWidget(QtGui.QWidget):
    """
    Base class for widgets manipulating colors.
    """

    colorChanged = QtCore.Signal(QtGui.QColor)
    """
    Emitted when the color has changed. Contains a matching QColor.
    """

    def __init__(self, parent=None):
        super(ColorWidget, self).__init__(parent)

        self._color = QtGui.QColor()

    def color(self):
        """
        The QColor represented by this widget.
        :return: A color
        :rtype: QColor
        """
        return QtGui.QColor(self._color)

    def updateColor(self, color):
        """
        Updates the color represented by this widget.
        Does not emit a signal.
        :param color: The new color.
        :type color: QColor
        """
        self._color = QtGui.QColor(color)
        self.repaint()

    def setColor(self, color):
        """
        Updates the color represented by this widget.
        Emits a colorChanged signal.
        :param color: The new color.
        :type color: QColor
        """
        self.updateColor(color)
        self.colorChanged.emit(self.color())


class Colorpicker(ColorWidget):
    """
    A compact color picker widget with a hue, and saturation wheel.
    Additional sliders for value, red, green, blue and alpha channels.
    """

    def __init__( self, color=[ 1, 1, 1 ], parent=None ):
        """
        Constructs a Colorpicker instance.

        :param parent: parent widget (optional)
        """
        super(ColorWidget, self).__init__(parent)

        __popUpSize  = [ 380, 350 ]
        defaultAlpha = 1

        layout = QtGui.QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        self._display = ColorDisplay()
        self._display.setMinimumSize( 60, 30 )
        size_policy = QtGui.QSizePolicy()
        size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Minimum)
        self._display.setSizePolicy(size_policy)

        layout.addWidget(self._display)

        self.setLayout(layout)
        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self._popup = Colorpicker._Popup(self)
        self._popup.setMinimumSize( __popUpSize[0], __popUpSize[1] )
        self._popup.setMaximumSize( __popUpSize[0], __popUpSize[1] )

        self._display.clicked.connect(self._on_display_clicked)

        self._connection_list = [self._display,
                                 self._popup]

        for x in self._connection_list:
            x.colorChanged.connect(self.updateColor)
            x.colorChanged.connect(self.colorChanged)

        self.setColor(QtGui.QColor( color[0]*255, color[1]*255, color[2]*255, defaultAlpha*255))

    def updateColor(self, color):
        """
        Updates the color represented by this widget,
        and all child widgets in it.
        Does not emit a signal.

        :param color: The new color.
        :type color: QColor
        """
        for x in self._connection_list:
            if x is not self.sender():
                x.updateColor(color)
        super(Colorpicker, self).updateColor(color)

    def _on_display_clicked(self):
        self._popup.move(self.mapToGlobal(self.rect().topLeft()))
        self._popup.show()

    def value( self ):

        color  = self._display.color().getRgb()
        rgb    = []
        rgb.append( round(color[0] / 255.0, 6) )
        rgb.append( round(color[1] / 255.0, 6) )
        rgb.append( round(color[2] / 255.0, 6) )

        return rgb

    class _Popup(ColorWidget):

        def __init__(self, parent=None):
            """
            Constructs a Colorpicker._Popup instance.

            :param parent: parent widget (optional)
            """
            super(ColorWidget, self).__init__(parent)

            self.setWindowFlags(QtCore.Qt.Popup)

            main_layout = QtGui.QVBoxLayout()
            self._frame = QtGui.QFrame()
            self._frame.setFrameStyle(QtGui.QFrame.Panel)
            self._frame.setFrameShadow(QtGui.QFrame.Raised)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(self._frame)
            self.setLayout(main_layout)

            layout = QtGui.QVBoxLayout()

            self._display = ColorDisplay()
            self._display.setMinimumSize( 60, 30 )
            size_policy = QtGui.QSizePolicy()
            size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Minimum)
            self._display.setSizePolicy(size_policy)

            top_layout = QtGui.QHBoxLayout()
            top_layout.addWidget(self._display)
            top_layout.addStretch(100)

            self._wheel = HueSaturationWheel()
            size_policy = QtGui.QSizePolicy()
            size_policy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
            size_policy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
            self._wheel.setSizePolicy(size_policy)

            size = 15

            self._hue_slider = ComponentSlider(ComponentSlider.HSV_HUE)
            self._hue_slider.setMinimumWidth(size)
            self._hue_slider.setDirection(ComponentSlider.HORIZONTAL)
            self._hue_slider.setGradient(QtCore.Qt.black, QtCore.Qt.white)

            self._saturation_slider = ComponentSlider(ComponentSlider.HSV_SATURATION)
            self._saturation_slider.setMinimumWidth(size)
            self._saturation_slider.setDirection(ComponentSlider.HORIZONTAL)
            self._saturation_slider.setGradient(QtCore.Qt.black, QtCore.Qt.white)

            self._value_slider = ComponentSlider(ComponentSlider.HSV_VALUE)
            self._value_slider.setMinimumHeight(size)
            self._value_slider.setMaximumHeight(size)
            self._value_slider.setDirection(ComponentSlider.HORIZONTAL)
            self._value_slider.setGradient(QtCore.Qt.black, QtCore.Qt.white)

            self._red_slider = ComponentSlider(ComponentSlider.RGBA_RED)
            self._red_slider.setMinimumHeight(size)
            self._red_slider.setMaximumHeight(size)
            self._red_slider.setDirection(ComponentSlider.HORIZONTAL)
            self._red_slider.setGradient(QtCore.Qt.black, QtCore.Qt.red)

            self._green_slider = ComponentSlider(ComponentSlider.RGBA_GREEN)
            self._green_slider.setMinimumHeight(size)
            self._green_slider.setMaximumHeight(size)
            self._green_slider.setDirection(ComponentSlider.HORIZONTAL)
            self._green_slider.setGradient(QtCore.Qt.black, QtCore.Qt.green)

            self._blue_slider = ComponentSlider(ComponentSlider.RGBA_BLUE)
            self._blue_slider.setMinimumHeight(size)
            self._blue_slider.setMaximumHeight(size)
            self._blue_slider.setDirection(ComponentSlider.HORIZONTAL)
            self._blue_slider.setGradient(QtCore.Qt.black, QtCore.Qt.blue)

            mid_layout = QtGui.QHBoxLayout()
            mid_layout.addWidget(self._wheel)
            mid_layout.setContentsMargins(5, 0, 5, 0)

            font = QtGui.QFont("Monospace")
            font.setStyleHint(QtGui.QFont.TypeWriter)

            label = QtGui.QLabel("R")
            label.setFont(font)
            label.setMaximumHeight(size)
            label.setMinimumWidth(10)
            label.setMaximumWidth(10)
            r_layout = QtGui.QHBoxLayout()
            r_layout.addWidget(label)
            r_layout.addWidget(self._red_slider)

            label = QtGui.QLabel("G")
            label.setFont(font)
            label.setMaximumHeight(size)
            label.setMinimumWidth(10)
            label.setMaximumWidth(10)
            g_layout = QtGui.QHBoxLayout()
            g_layout.addWidget(label)
            g_layout.addWidget(self._green_slider)

            label = QtGui.QLabel("B")
            label.setFont(font)
            label.setMaximumHeight(size)
            label.setMinimumWidth(10)
            label.setMaximumWidth(10)
            b_layout = QtGui.QHBoxLayout()
            b_layout.addWidget(label)
            b_layout.addWidget(self._blue_slider)

            label = QtGui.QLabel("H")
            label.setFont(font)
            label.setMaximumHeight(size)
            label.setMinimumWidth(10)
            label.setMaximumWidth(10)
            h_layout = QtGui.QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addWidget(self._hue_slider)

            label = QtGui.QLabel("S")
            label.setFont(font)
            label.setMaximumHeight(size)
            label.setMinimumWidth(10)
            label.setMaximumWidth(10)
            s_layout = QtGui.QHBoxLayout()
            s_layout.addWidget(label)
            s_layout.addWidget(self._saturation_slider)

            label = QtGui.QLabel("V")
            label.setFont(font)
            label.setMaximumHeight(size)
            label.setMinimumWidth(10)
            label.setMaximumWidth(10)
            v_layout = QtGui.QHBoxLayout()
            v_layout.addWidget(label)
            v_layout.addWidget(self._value_slider)

            bottom_layout = QtGui.QVBoxLayout()
            bottom_layout.setSpacing(2)
            bottom_layout.addLayout(r_layout)
            bottom_layout.addLayout(g_layout)
            bottom_layout.addLayout(b_layout)
            bottom_layout.addLayout(h_layout)
            bottom_layout.addLayout(s_layout)
            bottom_layout.addLayout(v_layout)

            layout.addLayout(top_layout)
            layout.addLayout(mid_layout)
            layout.addLayout(bottom_layout)

            layout.setContentsMargins(2, 2, 2, 2)

            self._frame.setLayout(layout)

            self._display.clicked.connect(self.hide)

            self._connection_list = [self._wheel,
                                     self._display,
                                     self._hue_slider,
                                     self._saturation_slider,
                                     self._value_slider,
                                     self._red_slider,
                                     self._green_slider,
                                     self._blue_slider]

            for x in self._connection_list:
                x.colorChanged.connect(self.updateColor)
                x.colorChanged.connect(self.colorChanged)

            self._wheel.setColor(QtGui.QColor())

        def updateColor(self, color):
            """
            Updates the color represented by this widget,
            and all child widgets in it.
            Does not emit a signal.

            :param color: The new color.
            :type color: QColor
            """
            for x in self._connection_list:
                if x is not self.sender():
                    x.updateColor(color)
            super(Colorpicker._Popup, self).updateColor(color)

        def show(self):
            pos = self.pos()
            fw = self._frame.lineWidth()
            margins = self._frame.layout().contentsMargins()
            pos.setX(pos.x() - margins.left() - fw)
            pos.setY(pos.y() - margins.top() - fw)
            rect = QtGui.QApplication.desktop().screenGeometry(self)
            if pos.x() + self.width() > rect.x() + rect.width():
                pos.setX(rect.x() + rect.width() - self.width())
            if pos.y() + self.height() > rect.y() + rect.height():
                pos.setY(rect.y() + rect.height() - self.height())
            self.move(pos)
            super(Colorpicker._Popup, self).show()


class ColorDisplay(ColorWidget):
    """
    A simple widget for displaying a color, including alpha values.
    """

    clicked = QtCore.Signal()
    """
    Emitted when the widget is clicked on.
    """

    def __init__(self, parent=None):
        """
        Constructs a ColorDisplay instance.

        :param parent: parent widget (optional)
        """
        super(ColorDisplay, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.save()
        rect = self.rect()
        painter.setClipRect(rect)

        _draw_checkerboard(painter, rect, 5)

        painter.fillRect(rect, self._color)

        painter.restore()


class ComponentSlider(ColorWidget):
    """
    A custom slider for manipulating a color component.
    Although it only manipulates a single component,
    it holds a QColor for convenience.
    """

    HORIZONTAL = 0
    VERTICAL = 1
    """
    Direction of the slider.
    """

    HSV_HUE = 0
    HSV_VALUE = 1
    HSV_SATURATION = 2
    RGBA_RED = 3
    RGBA_GREEN = 4
    RGBA_BLUE = 5
    RGBA_ALPHA = 6
    """
    Supported QColor components.
    """

    _component_names = {HORIZONTAL: 'Horizontal',
                        VERTICAL: 'Vertical',
                        HSV_HUE: 'Hue',
                        HSV_VALUE: 'Value',
                        HSV_SATURATION: 'Saturation',
                        RGBA_RED: 'Red',
                        RGBA_GREEN: 'Green',
                        RGBA_BLUE: 'Blue',
                        RGBA_ALPHA: 'Alpha'}

    def __init__(self, component, parent=None):
        """
        Constructs a ComponentSlider instance.

        :param component: The component managed by this slider.
        :type component:
          Any of class variables HSV_HUE, HSV_VALUE, HSV_SATURATION,
          RGBA_RED, RGBA_GREEN, RGBA_BLUE, RGBA_ALPHA
        :param parent: parent widget (optional)
        """
        super(ComponentSlider, self).__init__(parent)

        self._direction = self.HORIZONTAL

        self._gradient_color1 = QtCore.Qt.white
        self._gradient_color2 = QtCore.Qt.black
        self._component = component

    def setActiveComponent(self, component):
        """
        Sets the color component managed by this slider.

        :param component: The new component.
        :type component:
          Any of class variables HSV_HUE, HSV_VALUE, HSV_SATURATION, RGBA_RED,
          RGBA_GREEN, RGBA_BLUE, RGBA_ALPHA
        :type color: QColor
        """
        self._component = component

    def setDirection(self, direction):
        """
        Sets the direction of this slider.

        :param direction: The direction
        :type direction: Either of the class variables HORIZONTAL, and VERTICAL
        """
        self._direction = direction

    def setGradient(self, color1, color2):
        """
        Sets the color gradient of this slider's visual representation.

        :param color1: The first color of the gradient
        :param color2: The second color of the gradient
        """
        self._gradient_color1 = color1
        self._gradient_color2 = color2

    def _clamp(self, val, minimum, maximum):
        if val < minimum:
            val = minimum
        elif val > maximum:
            val = maximum
        return val

    def _get_component_value(self):
        if self._component == self.RGBA_RED:
            return self._color.redF()
        if self._component == self.RGBA_GREEN:
            return self._color.greenF()
        if self._component == self.RGBA_BLUE:
            return self._color.blueF()
        if self._component == self.RGBA_ALPHA:
            return self._color.alphaF()
        if self._component == self.HSV_HUE:
            return self._color.hsvHueF()
        if self._component == self.HSV_SATURATION:
            return self._color.hsvSaturationF()
        if self._component == self.HSV_VALUE:
            return self._color.valueF()

    def _update_component(self, value):
        color = self._color
        if self._component in [self.RGBA_RED, self.RGBA_GREEN,
                               self.RGBA_BLUE, self.RGBA_ALPHA]:
            c = self._component
            r = value if c == self.RGBA_RED else color.redF()
            g = value if c == self.RGBA_GREEN else color.greenF()
            b = value if c == self.RGBA_BLUE else color.blueF()
            a = value if c == self.RGBA_ALPHA else color.alphaF()
            color.setRgbF(r, g, b)
            color.setAlphaF(a)
        elif self._component in [self.HSV_HUE, self.HSV_SATURATION,
                                 self.HSV_VALUE]:
            c = self._component
            a = color.alphaF()
            h = value if c == self.HSV_HUE else color.hsvHueF()
            s = value if c == self.HSV_SATURATION else color.hsvSaturationF()
            v = value if c == self.HSV_VALUE else color.valueF()
            color.setHsvF(h, s, v)
            color.setAlphaF(a)
        else:
            return

        self.repaint()

    def _update_color(self, pos):
        if self._component not in self._component_names.iterkeys():
            return

        rect = self.rect()

        if self._direction == self.VERTICAL:
            top = rect.top()
            bottom = rect.bottom()
            component_value = 1 - \
                float(self._clamp(pos.y(), top, bottom)) / float(bottom - top)
        else:
            left = rect.left()
            right = rect.right()
            component_value = float(
                self._clamp(pos.x(), left, right)) / float(right - left)

        self._update_component(component_value)

    def mousePressEvent(self, event):
        self._update_color(event.pos())
        self.colorChanged.emit(QtGui.QColor(self._color))

    def mouseMoveEvent(self, event):
        self._update_color(event.pos())
        self.colorChanged.emit(QtGui.QColor(self._color))

    def mouseReleaseEvent(self, event):
        self._update_color(event.pos())

    def mouseDoubleClickEvent(self, event):
        value = self._get_component_value()

        # can't use getDouble() because we need to update the dialog position.
        dialog = QtGui.QInputDialog(self, QtCore.Qt.Popup)
        dialog.setInputMode(QtGui.QInputDialog.DoubleInput)
        dialog.setDoubleRange(0.0, 1.0)
        dialog.setDoubleDecimals(4)
        dialog.setDoubleValue(value)
        dialog.setLabelText(self._component_names.get(self._component,
                                                      "Unknown"))

        def _update(value):
            self._update_component(value)
            self.colorChanged.emit(QtGui.QColor(self._color))
        dialog.doubleValueSelected.connect(_update)

        dialog.show()
        pos = QtGui.QCursor.pos()
        pos.setX(pos.x() - dialog.geometry().width() / 2)
        pos.setY(pos.y() - dialog.height() / 2)
        dialog.move(pos)

    def paintEvent(self, event):
        rect = self.rect()
        painter = QtGui.QPainter(self)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setClipRect(rect)

        size = min(rect.width(), rect.height()) * 0.5
        _draw_checkerboard(painter, rect, size)

        if self._direction == self.VERTICAL:
            gradient = QtGui.QLinearGradient(rect.bottomLeft(), rect.topLeft())
        else:
            gradient = QtGui.QLinearGradient(rect.topLeft(), rect.topRight())
        gradient.setColorAt(0, self._gradient_color1)
        gradient.setColorAt(1, self._gradient_color2)
        painter.fillRect(rect, gradient)

        component = self._get_component_value()
        if self._direction == self.VERTICAL:
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
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)

        pen.setColor(QtGui.QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawLine(line1)
        pen.setColor(QtGui.QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawLine(line2)
        pen.setColor(QtGui.QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawLine(line3)

        painter.restore()


class HueSaturationWheel(ColorWidget):
    """
    A color wheel for manipulating the hue and saturation of a given QColor.
    """

    def __init__(self, parent=None):
        """
        Constructs a HueSaturationWheel instance.

        :param parent: parent widget (optional)
        """
        super(HueSaturationWheel, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._color = QtGui.QColor(255, 255, 255)
        self._wheel_img = None
        self._marker_pos = QtCore.QPointF(0, 0)
        self.setMinimumSize(10, 10)

    def updateColor(self, color):
        """
        Updates the color represented by this widget.
        Does not emit a signal.

        :param color: The new color.
        :type color: QColor
        """

        if color.rgb() == self._color.rgb():
            return

        old_value = self._color.value()

        square = self._square()

        radius = square.width() * 0.5

        hue = color.hsvHueF()
        sat = color.hsvSaturationF()

        self._color.setRgba(color.rgba())

        distance = sat * radius

        center = square.center()
        line = QtCore.QLineF(center.x(), center.y(),
                             center.x(), center.y() + distance)
        line.setAngle(360.0 - hue * 360.0)
        line.setAngle(line.angle() - 90)

        self._update_color(line.p2())
        self._update_marker_pos()
        if old_value != color.value():
            self._rebuild_color_wheel()

        super(HueSaturationWheel, self).updateColor(color)

    def _length2(self, p1, p2):
        return pow((p2.x() - p1.x()), 2) + pow((p2.y() - p1.y()), 2)

    def _length(self, p1, p2):
        return math.sqrt(self._length2(p1, p2))

    def _update_color(self, pos):
        square = self._square()

        radius = square.width() * 0.5
        line = QtCore.QLineF(square.center(), pos)
        distance = self._length(line.p1(), line.p2())
        if distance > radius:
            distance = radius
        line.setAngle(line.angle() + 90.0)
        h = (360.0 - line.angle()) / 360.0
        s = distance / radius
        v = self._color.valueF()
        a = self._color.alphaF()
        self._color.setHsvF(h, s, v)
        self._color.setAlphaF(a)

    def _square(self):
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

    def _update_marker_pos(self):
        square = self._square()

        radius = square.width() * 0.5

        hue = self._color.hsvHueF()
        sat = self._color.hsvSaturationF()

        distance = sat * radius

        center = square.center()
        line = QtCore.QLineF(center.x(), center.y(),
                             center.x(), center.y() + distance)
        line.setAngle(360.0 - hue * 360.0)
        line.setAngle(line.angle() - 90)

        self._marker_pos = line.p2()

    def _rebuild_color_wheel(self):
        image_format = QtGui.QImage.Format_ARGB32_Premultiplied
        self._wheel_img = QtGui.QImage(self._square().size(), image_format)
        self._wheel_img.fill(0)
        rect = self._wheel_img.rect()
        painter = QtGui.QPainter(self._wheel_img)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.transparent)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.transparent)
        painter.drawRect(rect)

        radius = rect.width() * 0.5
        path = QtGui.QPainterPath()
        path.addEllipse(rect)

        painter.setClipPath(path)

        # hue, value
        hue = QtGui.QConicalGradient(rect.center(), -90)
        color = QtGui.QColor()
        step = 0
        value = self._color.valueF()
        while step < 1.0:
            color.setHsvF(1 - step, 1, value)
            hue.setColorAt(step, color)
            step += 0.1
        painter.fillPath(path, hue)

        # Saturation. May not be completely accurate,
        # but it's only used as a visual representation
        saturation = QtGui.QRadialGradient(rect.center(), radius)
        color.setRgbF(value, value, value)
        color.setAlphaF(1)
        saturation.setColorAt(0, color)
        color.setRgbF(value, value, value)
        color.setAlphaF(0)
        saturation.setColorAt(1, color)
        painter.fillPath(path, saturation)
        painter.restore()

        self.repaint()

    def resizeEvent(self, event):
        self._rebuild_color_wheel()
        self._update_marker_pos()
        return super(HueSaturationWheel, self).resizeEvent(event)

    def mousePressEvent(self, event):
        self._update_color(event.pos())
        self._update_marker_pos()
        self.repaint()
        self.colorChanged.emit(self.color())

    def mouseMoveEvent(self, event):
        self._update_color(event.pos())
        self._update_marker_pos()
        self.repaint()
        self.colorChanged.emit(self.color())

    def mouseReleaseEvent(self, event):
        self._update_color(event.pos())
        self._update_marker_pos()
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setClipRect(self.rect())

        painter.drawImage(self._square(), self._wheel_img)

        pen = QtGui.QPen()
        v = 0 if self._color.valueF() > 0.5 else 255
        pen.setColor(QtGui.QColor(v, v, v))
        painter.setPen(pen)
        marker = QtCore.QRectF(self._marker_pos.x() - 2,
                               self._marker_pos.y() - 2, 5, 5)
        # angles are specified in 1/16 of a degree; draws a full circle
        painter.drawArc(marker, 0, 5760)

        painter.restore()
