import pkg_resources
from PyQt5 import uic #type: ignore
from PyQt5.QtCore import QModelIndex, Qt, QSize, QRect #type: ignore
from PyQt5.QtGui import QPainter, QColor, QIcon, QBrush, QFont, QFontMetrics, QPalette #type: ignore
from PyQt5.QtWidgets import QMainWindow, QWidget, QStyle, QStyledItemDelegate, QStyleOptionViewItem #type: ignore
from kryptal.gui.controller.CreateFilesystemController import CreateFilesystemController
from kryptal.model.Filesystems import Filesystems
from kryptal.pluginmanager.KryptalPlugins import KryptalPlugins
from kryptal.services.FilesystemCreatorService import FilesystemCreatorService
from kryptal.utils import Paths


#class FilesystemListItemDelegate(QStyledItemDelegate):
#
#    _height = 50
#    _vertical_padding = 3
#    _icon_size = 50
#    _icon_margin_left = 5
#    _icon_margin_right = 10
#    _namecol_width = 100
#    _namecol_margin_right = 50
#
#    _fstypeHeader = "Type: "
#    _plaintextDirHeader = "Plaintext Directory: "
#    _ciphertextDirHeader = "Ciphertext Directory: "
#
#    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
#        return QSize(self._icon_margin_left + self._icon_size + self._icon_margin_right + self._namecol_width + self._namecol_margin_right + self._dircolWidth(index), self._height + 2*self._vertical_padding)
#
#    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
#        painter.save()
#        self.initStyleOption(option, index)
#        self._paintBackground(painter, option)
#        painter.translate(option.rect.x(), option.rect.y() + self._vertical_padding)
#        self._paintIcon(painter, QRect(self._icon_margin_left, 0, self._icon_size, self._icon_size))
#        painter.translate(self._icon_margin_left + self._icon_size + self._icon_margin_right, 0)
#        self._paintText(painter, QRect(0, 0, self._namecol_width, self._height/2), index.data().name, "")
#        self._paintText(painter, QRect(0, self._height/2, self._namecol_width, self._height/2), self._fstypeHeader, index.data().fstype)
#        painter.translate(self._namecol_width + self._namecol_margin_right, 0)
#        self._paintText(painter, QRect(0, 0, self._dircolWidth(index), self._height / 2), self._plaintextDirHeader, index.data().plaintextDirectory)
#        self._paintText(painter, QRect(0, self._height/2, self._dircolWidth(index), self._height / 2), self._ciphertextDirHeader, index.data().ciphertextDirectory)
#        painter.restore()
#
#    def _paintBackground(self, painter: QPainter, option: QStyleOptionViewItem) -> None:
#        if option.state & QStyle.State_Active:
#            color_group = QPalette.Active
#        else:
#            color_group = QPalette.Inactive
#        if option.state & QStyle.State_Selected:
#            color_role = QPalette.Highlight
#        else:
#            color_role = QPalette.Base
#        painter.fillRect(option.rect, QBrush(option.palette.color(color_group, color_role)))
#
#    def _paintIcon(self, painter: QPainter, rect: QRect) -> None:
#        icon = QIcon.fromTheme("drive-harddisk").pixmap(rect.width(), rect.height())
#        painter.drawPixmap(rect.x(), rect.y(), icon)
#
#    def _paintText(self, painter: QPainter, rect: QRect, header: str, text: str) -> None:
#        painter.save()
#        painter.setFont(self._headerFont())
#        painter.drawText(rect.x(), rect.y(), rect.width(), rect.height(), Qt.AlignVCenter, header)
#        painter.setFont(self._normalFont())
#        painter.drawText(rect.x() + QFontMetrics(self._headerFont()).width(header), rect.y(), rect.width(), rect.height(), Qt.AlignVCenter, text)
#        painter.restore()
#
#    def _dircolWidth(self, index: QModelIndex) -> int:
#        return max(
#            self._textWidth(self._plaintextDirHeader, index.data().plaintextDirectory),
#            self._textWidth(self._ciphertextDirHeader, index.data().ciphertextDirectory)
#        )
#
#    def _normalFont(self) -> QFont:
#        return QFont()
#
#    def _headerFont(self) -> QFont:
#        font = QFont()
#        font.setBold(True)
#        return font
#
#    def _textWidth(self, header: str, text: str) -> int:
#        return QFontMetrics(self._headerFont()).width(header) + QFontMetrics(self._normalFont()).width(text)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super(MainWindow, self).__init__(parent)

        uipath = pkg_resources.resource_filename(__name__, "mainwindow.ui")
        uic.loadUi(uipath, self)
        self.createFilesystemButton.clicked.connect(self.onCreateFilesystemButtonClick)

        self._plugins = KryptalPlugins()
        for name in self._plugins.filesystems():
            self.pluginsList.addItem("Filesystem: %s" % name)
        for name in self._plugins.storage_providers():
            self.pluginsList.addItem("StorageProvider: %s" % name)
        self.pluginsList.setDragDropMode(self.pluginsList.InternalMove)
        self.pluginsList.setDropIndicatorShown(True)

        self._filesystemModel = Filesystems(Paths.filesystems_state_file())
        #self.filesystemsTableView.setModel(FilesystemsModelAdapter(self.filesystemsTableView, self._filesystemModel))

        #self.filesystemsListView.setModel(FilesystemsModelAdapter(self.filesystemsListView, self._filesystemModel))
        #self.filesystemsListView.setItemDelegate(FilesystemListItemDelegate(self.filesystemsListView))
        #self.filesystemsListView.setSpacing(2)
        #self.filesystemsListView.setDragDropMode(self.filesystemsListView.InternalMove)
        #self.filesystemsListView.setDropIndicatorShown(True)

        self.fileSystemList.setModel(self._filesystemModel)

    def onCreateFilesystemButtonClick(self) -> None:
        creatorService = FilesystemCreatorService(self._plugins, self._filesystemModel)
        CreateFilesystemController(creatorService).create()
        self.fileSystemList._update()
