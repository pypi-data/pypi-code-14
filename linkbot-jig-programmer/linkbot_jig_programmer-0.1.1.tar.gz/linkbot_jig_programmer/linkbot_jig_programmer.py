#!/usr/bin/env python3

__version__ = "0.1.1"

import sys
from PyQt4 import QtCore, QtGui
try:
    from linkbot_jig_programmer.mainwindow import Ui_MainWindow
except:
    from mainwindow import Ui_MainWindow
import linkbot3 as linkbot
import time
import glob
import threading
import os
import subprocess
import serial
import pystk500v2 as stk
import random
import traceback

from pkg_resources import resource_filename, resource_listdir
fallback_hex_file = ''
fallback_eeprom_file = ''
firmware_files = resource_listdir(__name__, 'hexfiles')
firmware_files.sort()
firmware_basename = os.path.splitext(
    resource_filename(__name__, os.path.join('hexfiles', firmware_files[0])))[0]
fallback_hex_file = firmware_basename + '.hex'

bootloader_file = resource_filename(__name__, 
    os.path.join('bootloader', 'ATmegaBOOT_168_mega128rfa1_8MHz.hex'))

def _getSerialPorts():
  if os.name == 'nt':
    available = []
    for i in range(256):
      try:
        s = serial.Serial(i)
        available.append('\\\\.\\COM'+str(i+1))
        s.close()
      except Serial.SerialException:
        pass
    return available
  else:
    from serial.tools import list_ports
    return [port[0] for port in list_ports.comports()]

def findHexFiles():
    ''' Returns a list of hex file base names absolute paths with no extensions.
    '''
    hexfiles = [firmware_basename]
    try:
        files = glob.glob(
            os.environ['HOME'] + 
            '/.local/share/Barobo/LinkbotLabs/firmware/*.hex')
        files = map( lambda x: os.path.splitext(x)[0], files)
        # For each file, make sure the eeprom file also exists
        for f in files:
            if os.path.isfile(f + '.eeprom'):
                hexfiles += [f]

        files = glob.glob(
            os.environ['HOME'] + 
            '/usr/share/Barobo/LinkbotLabs/firmware/*.hex')
        files = map( lambda x: os.path.splitext(x)[0], files)
        # For each file, make sure the eeprom file also exists
        for f in files:
            if os.path.isfile(f + '.eeprom'):
                hexfiles += [f]
    except:
        pass

    return hexfiles

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.isRunning = True
        self.setWindowTitle('Linkbot Jig Main-Board Programmer')

        # Populate the firmware hex files combobox
        for f in sorted(findHexFiles()):
            self.ui.firmwareversion_comboBox.addItem(f)

        for p in sorted(_getSerialPorts()):
            self.ui.comport_comboBox.addItem(p)

        self.disableTestButtons()
        self.ui.robotid_lineEdit.textChanged.connect(self.robotIdChanged)
        self.ui.flash_pushButton.clicked.connect(self.startProgramming)
        self.ui.test_pushButton.clicked.connect(self.runTest)
        #self.ui.flashtest_pushButton.clicked.connect(self.flashAndTest)
        self.ui.checkBox_autoFlash.stateChanged.connect(self.processCheckButton)
        self.ui.progressBar.setValue(0)
        self.progressTimer = QtCore.QTimer(self)
        self.progressTimer.timeout.connect(self.updateProgress)
        self.progressTimerSilent = QtCore.QTimer(self)
        self.progressTimerSilent.timeout.connect(self.updateProgressSilent)
        self.autoTest = False
        try:
            self.daemon = linkbot.Daemon()
        except:
            self.daemon = None

    def robotIdChanged(self, text):
        if len(text) == 4:
            self.enableTestButtons()
        else:
            self.disableTestButtons()

    def disableTestButtons(self):
        self.ui.test_pushButton.setEnabled(False)
        #self.ui.flashtest_pushButton.setEnabled(False)

    def enableTestButtons(self):
        self.ui.test_pushButton.setEnabled(True)
        #self.ui.flashtest_pushButton.setEnabled(True)

    def disableButtons(self):
        self.disableTestButtons()
        self.ui.flash_pushButton.setEnabled(False)

    def enableButtons(self):
        self.enableTestButtons()
        self.ui.flash_pushButton.setEnabled(True)

    def startProgramming(self): 
        serialPort = self.ui.comport_comboBox.currentText()
        firmwareFile = self.ui.firmwareversion_comboBox.currentText()+'.hex'
        try:
          self.programmer = stk.ATmega128rfa1Programmer(serialPort)
        except Exception as e:
          QtGui.QMessageBox.warning(self, "Programming Exception",
            'Unable to connect to programmer at com port '+ serialPort + 
            '. ' + str(e))
          traceback.print_exc()
          return
        
        # Generate a random ID for the new board
        self.serialID = "{:04d}".format(random.randint(1000, 9999))
        try:
            self.disableButtons()
            self.programmer.programAllAsync( serialID=self.serialID,
                                             hexfiles=[firmwareFile, bootloader_file],
                                             verify=False
                                           )
            self.progressTimer.start(1000)
        except Exception as e:
          QtGui.QMessageBox.warning(self, "Programming Exception",
            'Unable to connect to programmer at com port '+ serialPort + 
            '. ' + str(e))
          traceback.print_exc()
          return

    def startProgrammingSilent(self):
        print('Trying to start programming...')
        serialPort = self.ui.comport_comboBox.currentText()
        firmwareFile = self.ui.firmwareversion_comboBox.currentText()+'.hex'
        self.programmer = stk.ATmega128rfa1Programmer(serialPort)
        
        # Generate a random ID for the new board
        self.serialID = "{:04d}".format(random.randint(1000, 9999))
        self.programmer.serialID = self.serialID
        self.programmer.programAll( 
                                    hexfiles=[firmwareFile, bootloader_file],
                                    verify=False
                                  )
    
    def runTest(self):
        self.disableButtons()
        testThread = RobotTestThread(self)
        testThread.setTestRobotId(self.ui.robotid_lineEdit.text())
        testThread.threadFinished.connect(self.testFinished)
        testThread.threadException.connect(self.testException)
        testThread.start()

    def processCheckButton(self, enabled):
        if enabled:
            self.disableButtons()
            # Start the listening thread
            self.listenThread = AutoProgramThread(self)
            self.listenThread.is_active = True
            self.listenThread.start()
        else:
            self.listenThread.is_active = False
            self.listenThread.wait()
            self.enableButtons()

    def flashAndTest(self):
        self.autoTest = True
        self.startProgramming()

    def testFinished(self):
        self.enableButtons()

    def testException(self, e):
        QtGui.QMessageBox.warning(self, "Error", 
            "Test failed: " + str(e) )

    def updateProgress(self):
        # Multiply progress by 200 because we will not be doing verification
        progress = self.programmer.getProgress()*200
        if progress > 100:
            progress = 100
        self.ui.progressBar.setValue(progress)
        if not self.programmer.isProgramming():
            if self.programmer.getLastException() is not None:
              QtGui.QMessageBox.warning(self, "Programming Exception",
                str(self.programmer.getLastException()))

            self.progressTimer.stop()
            if self.daemon:
                self.daemon.cycle(1)
            if self.autoTest:
                self.runTest()
                '''
                timer = QtCore.QTimer(self)
                timer.timeout.connect(self.runTest)
                timer.setSingleShot(True)
                timer.start(8000)
                '''
            else:
                self.enableButtons()
            self.autoTest = False

    def updateProgressSilent(self):
        # Multiply progress by 200 because we will not be doing verification
        try:
            progress = self.programmer.getProgress()*200
            if progress > 100:
                progress = 100
            self.ui.progressBar.setValue(progress)
        except:
            pass

class RobotTestThread(QtCore.QThread):
    threadFinished = QtCore.pyqtSignal()
    threadException = QtCore.pyqtSignal(Exception)

    def __init__(self, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)

    def setTestRobotId(self, id):
        self.testBotId = id

    def run(self):
        # Power the motors forward and backward
        try:
            l = linkbot.CLinkbot()
            if l.getFormFactor() != 3:
                l.setMotorPowers(255, 255, 255)
                time.sleep(1)
                l.setMotorPowers(-255, -255, -255)
                time.sleep(1)
                l.setMotorPowers(0,0,0)
                time.sleep(1)
                (x,y,z) = l.getAccelerometerData()
                if abs(x) < 0.1 and abs(y) < 0.1 and (abs(z)-1) < 0.1:
                    pass
                else:
                    self.threadException.emit(
                        Exception("Accelerometer anomaly detected."))

            testbot = linkbot.CLinkbot(self.testBotId)
            print(testbot.getJointAngles())
            del testbot
            l.setBuzzerFrequency(220)
            time.sleep(0.5)
            l.setBuzzerFrequency(0)
        except Exception as e:
            self.threadException.emit(e)
        self.threadFinished.emit()

class AutoProgramThread(QtCore.QThread):
    threadFinished = QtCore.pyqtSignal()
    threadException = QtCore.pyqtSignal(Exception)

    IDLE = 0
    DONE_PROGRAMMING = 1

    def __init__(self, parent):
        super().__init__(parent)
        self.is_active = True
        self._main_window = parent
        self.state = self.IDLE
        self._main_window.progressTimerSilent.start(1000)

    def run(self):
        while self.is_active:
            if self.state == self.IDLE:
                self.idle()
            elif self.state == self.DONE_PROGRAMMING:
                self.done_programming()

    def idle(self):
        try:
            self._main_window.startProgrammingSilent()
            self.state = self.DONE_PROGRAMMING
            print('Done programming.')
        except Exception as e:
            print('Caught exception: ', str(e), 'Trying again...')
            time.sleep(1)

    def done_programming(self):
        try:
            print('Trying sign-on...')
            self._main_window.programmer.check_signature()
            time.sleep(1)
            print('Success.')
        except:
            self.state = self.IDLE


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
