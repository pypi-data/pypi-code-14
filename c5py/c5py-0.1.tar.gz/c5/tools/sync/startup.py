import sys

from PyQt4 import QtGui

from .control import itemcontrol
from .control.xmlwrapper import XMLWrapper
from .model import itemmodel


def startApp():
    if len(sys.argv) != 2:
        print "wrong usage:  <configfile>"
        sys.exit(1)
    app = QtGui.QApplication(sys.argv)
    a_model = itemmodel.ModelItem()
    wrapper = XMLWrapper(a_model)
    wrapper.load_model(sys.argv[1])

    controller = itemcontrol.ItemController(a_model)
    do_run = True
    while do_run is True:
        controller.gui.show()
        status = app.exec_()
        del controller.gui
        inp = raw_input("console mode. q <enter> to quit. everything else restarts gui: ")
        if inp == "q":
            do_run = False
        else:
            controller.restart_gui()
    wrapper.save_model(sys.argv[1])
    print "kill controller"
    controller.dispatcher.stop()

if __name__ == '__main__':
    startApp()
