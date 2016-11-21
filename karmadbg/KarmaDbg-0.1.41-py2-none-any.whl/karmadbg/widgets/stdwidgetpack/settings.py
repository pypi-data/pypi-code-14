
from PySide.QtGui import QTreeView, QStandardItemModel, QStandardItem,  QDockWidget, QMenu, QAction
from PySide.QtCore import Qt

from operator import attrgetter

class QReadOnlyItem(QStandardItem):
    def __init__(self, text, uimanager, *args, **kwargs):
        super(QReadOnlyItem,self).__init__(text, *args, **kwargs)
        self.uimanager = uimanager
        self.setEditable(False)

    def getContextMenu(self):
        return None

class WidgetItem(QReadOnlyItem):
    def __init__(self, *args, **kwargs):
        super(WidgetItem,self).__init__(*args, **kwargs)

    def getContextMenu(self):
        menu = QMenu()
        menu.addAction( QAction("Remove Widget",self.uimanager.mainwnd) )
        return menu

class WidgetRootItem(QReadOnlyItem):
    def __init__(self, *args, **kwargs):
        super(WidgetRootItem,self).__init__(*args, **kwargs)

    def getContextMenu(self):
        menu = QMenu()
        menu.addAction( QAction("Add widget",self.uimanager.mainwnd) )
        return menu
        

class SettingsWidget(QDockWidget):

    def __init__(self, widgetSettings, uimanager):
        super(SettingsWidget, self).__init__()
        self.uimanager = uimanager
        self.uimanager.mainwnd.addDockWidget(Qt.LeftDockWidgetArea,self)

        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeModel = QStandardItemModel(0,1)
        self.treeModel.itemChanged.connect(self.onItemChanged)
        self.treeView.setModel(self.treeModel)

        self.loadModel()

        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.onCustomContextMenu)

        self.setWidget(self.treeView)

    def loadModel(self):
        self.loadMainWindow()
        self.loadWidgets()
        self.loadExt()
        self.treeView.resizeColumnToContents(0)
        self.treeView.setColumnWidth( 0, 250 ) 


    def loadWidgets(self):
        rootNode = WidgetRootItem("Widgets", self.uimanager)
        self.treeModel.appendRow( rootNode )

        for widgetSetting in sorted(self.uimanager.dbgSettings.widgets, key=attrgetter('name')):
            widgetRoot = WidgetItem(widgetSetting.name, self.uimanager)
            rootNode.appendRow(widgetRoot)
            widgetRoot.appendRow( [ QReadOnlyItem( "Module: " + widgetSetting.module, self.uimanager) ] )
            widgetRoot.appendRow( [ QReadOnlyItem( "Class: " + widgetSetting.className, self.uimanager) ] )
            if widgetSetting.title:
                widgetRoot.appendRow( [QReadOnlyItem("Title: " + widgetSetting.title, self.uimanager) ] )

    def loadMainWindow(self):
        rootNode = QReadOnlyItem("Main Window, self.uimanager", self.uimanager)
        self.treeModel.appendRow( rootNode )

        rootNode.appendRow( [ QReadOnlyItem( "Title: " + self.uimanager.dbgSettings.mainWindow.title, self.uimanager) ] )
        rootNode.appendRow( [ QReadOnlyItem( "Width: " + str(self.uimanager.dbgSettings.mainWindow.width), self.uimanager) ] )
        rootNode.appendRow( [ QReadOnlyItem( "Height: " + str(self.uimanager.dbgSettings.mainWindow.height), self.uimanager) ] )

    def loadExt(self):
        rootNode = QReadOnlyItem("DbgEng Extensions", self.uimanager)
        self.treeModel.appendRow( rootNode )

        for extSettings in self.uimanager.dbgSettings.dbgEngExtensions:
            extRoot = QReadOnlyItem(extSettings.path, self.uimanager)
            extRoot.setColumnCount(2)
            extRoot.appendRow( [ QReadOnlyItem( "Startup: " + str(extSettings.startup), self.uimanager) ] )
            rootNode.appendRow(extRoot)

    def onItemChanged(self, item):
        pass

    def onCustomContextMenu(self,point):
        item = self.treeModel.itemFromIndex( self.treeView.indexAt(point) )
        if item:
            contextMenu = item.getContextMenu()
            if contextMenu:
                contextMenu.exec_(self.treeView.mapToGlobal(point))


    
