from PyQt4 import QtGui, QtCore


class LayoutPreview(QtGui.QWidget):
    selectionChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(QtGui.QWidget, self).__init__(parent)
        self.selected_container = None
        self.layout = None
        self.editable = True

    def mousePressEvent(self, event):
        if self.editable is False or self.layout is None:
            return

        selected = QtCore.QPoint(event.x(), event.y())

        preview_pos_x = min(20,self.width()/20, self.height()/10)
        preview_pos_y = preview_pos_x
        preview_width = self.width()-2*preview_pos_x-1
        preview_height = self.height()-2*preview_pos_y-1

        for container_name in self.layout.get_container_names():
            container = self.layout.get_container(container_name)
            pos_x = container.get_pos_x() * (preview_width) / self.layout.width + preview_pos_x
            pos_y = container.get_pos_y() * (preview_height) / self.layout.height + preview_pos_y
            width = container.get_width() * (preview_width) / self.layout.width
            height = container.get_height() * (preview_height) / self.layout.height

            rect = QtCore.QRect(pos_x,pos_y,width,height)
            if rect.contains(selected): self.setSelected(container.get_name())


    def setSelected(self, container_name):
        if self.selected_container != container_name:
            self.selected_container = container_name
            self.selectionChanged.emit(self.selected_container)
            self.update()

    def setEditable(self, is_editable):
        self.editable = is_editable

    def setLayout(self, layout):
        self.layout = layout
        self.update()

    def paintEvent(self, event):
        if self.layout is None:
            return

        preview_pos_x = min(20,self.width()/20, self.height()/10)
        preview_pos_y = preview_pos_x
        preview_width = self.width()-2*preview_pos_x-1
        preview_height = self.height()-2*preview_pos_y-1

        font = QtGui.QFont(QtCore.QString("Arial"))

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(preview_pos_x,preview_pos_y,preview_width, preview_height, QtGui.QColor(0,0,255,50))
        painter.setPen(QtGui.QColor(0,0,255))
        painter.drawRect(preview_pos_x, preview_pos_y, preview_width, preview_height)

        font.setPixelSize(preview_pos_x)
        metrics = QtGui.QFontMetrics(font)
        painter.setFont(font)

        painter.drawText(self.width()/2-metrics.width(str(self.layout.get_width()))/2, preview_pos_y, str(self.layout.get_width()))
        painter.save()
        painter.translate(preview_pos_x,self.height()/2 + metrics.width(str(self.layout.get_height()))/2)
        painter.rotate(270)
        painter.drawText(0,0,str(self.layout.get_height()))
        painter.restore()

        for container_name in self.layout.get_container_names():
            container = self.layout.get_container(container_name)
            pos_x = container.get_pos_x() * (preview_width) / self.layout.width + preview_pos_x
            pos_y = container.get_pos_y() * (preview_height) / self.layout.height + preview_pos_y
            width = container.get_width() * (preview_width) / self.layout.width
            height = container.get_height() * (preview_height) / self.layout.height

            if self.selected_container == container.get_name():
                borderColor = QtGui.QColor(255,255,0)
                fillColor = QtGui.QColor(255,255,0,50)
            else:
                borderColor = QtGui.QColor(255,0,0)
                fillColor = QtGui.QColor(255,0,0,50)

            painter.fillRect(pos_x, pos_y, width, height, fillColor)
            painter.setPen(borderColor)
            painter.drawRect(pos_x, pos_y, width, height)

            painter.drawText((pos_x+width/2)-metrics.width(str(container.get_width()))/2, pos_y+metrics.height(), str(container.get_width()))
            painter.save()
            painter.translate(pos_x+metrics.height(),(pos_y+height/2) + metrics.width(str(container.get_height()))/2)
            painter.rotate(270)
            painter.drawText(0,0,str(container.get_height()))
            painter.restore()
            tmp_font = QtGui.QFont(font)
            tmp_metrics = QtGui.QFontMetrics(tmp_font)
            while tmp_metrics.width(str(container.get_name())) > width/2:
                tmp_font.setPixelSize(tmp_font.pixelSize()-1)
                tmp_metrics = QtGui.QFontMetrics(tmp_font)
            painter.setFont(tmp_font)
            painter.drawText((pos_x+width/2)-tmp_metrics.width(str(container.get_name()))/2,
                                    (pos_y+height/2) + tmp_metrics.height()/2,
                                    str(container.get_name()))
            painter.setFont(font)

        painter.end()
