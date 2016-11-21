from PySide.QtCore import Qt
from PySide.QtGui import QDockWidget, QMainWindow

#class DockManager(QObject):

#    def __init__(self, widgetSettings, uimanager):
#        super(DockManager,self).__init__()
#        pass

class DockWindow(QMainWindow):

    def __init__(self, uimanager):
        super(DockWindow,self).__init__()
        self.uimanager = uimanager
        
    def dropEvent(event):
        pass

    def enterEvent(self, event):
        if self.uimanager.dockingWidget:
            self.uimanager.dockingWidget.setFloating(False)
            self.addDockWidget(Qt.TopDockWidgetArea, self.uimanager.dockingWidget)
            self.uimanager.dockingWidget = None
    


