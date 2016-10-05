import sys
import os.path

from PyQt4 import QtGui, QtCore
from videoWidgetUi import Ui_videoWidget

from cvtools import CVVideo

class VideoDialog(QtGui.QDialog):
    def __init__(self, file_path):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_videoWidget()
        self.ui.setupUi(self)
        self.processor = CVVideo(self.ui.videoLayer)
        self.ui.videoLayer.set_processor(self.processor)
        self.processor.set_capture(file_path)
        self.ui.gotoButton.clicked.connect(self.goto_frame)
        self.ui.previousButton.clicked.connect(self.previous_frame)
        self.ui.nextButton.clicked.connect(self.next_frame)
        self.ui.e1List.itemDoubleClicked.connect(self.set_e1)
        self.ui.e2List.itemDoubleClicked.connect(self.set_e2)
        self.ui.setE1Button.clicked.connect(self.set_e1)
        self.ui.setE2Button.clicked.connect(self.set_e2)
        self.ui.gotoE1Button.clicked.connect(self.goto_e1)
        self.ui.gotoE2Button.clicked.connect(self.goto_e2)

    def set_events(self, events_list, selected_events):
        selected_events = sorted(selected_events)
        print events_list
        print selected_events
        for selected in selected_events:
            if selected not in events_list:
                events_list.append(selected)
        for event in sorted(events_list):
            item = QtGui.QListWidgetItem()
            file_path = "%s.%s.png" % (self.processor.path, str(event))
            print file_path
            pixmap = QtGui.QPixmap(file_path, "PNG").scaledToHeight(200)
            item.setIcon(QtGui.QIcon(pixmap))
            item.setToolTip(str(event))
            item2 = QtGui.QListWidgetItem(item)
            self.ui.e1List.addItem(item)
            self.ui.e2List.addItem(item2)
            if event in selected_events:
                if selected_events.index(event) > 0:
                    self.set_e2(item2)
                else:
                    self.set_e1(item)

    def set_e1(self, item=None):
        if isinstance(item, QtGui.QListWidgetItem):
            self.ui.event1Label.setPixmap(item.icon().pixmap(300,200))
            self.e1 = int(item.toolTip())
        else:
            self.ui.event1Label.setPixmap(QtGui.QPixmap.fromImage(self.processor.get_current_image()).scaledToWidth(300))
            self.e1 = int(self.processor.get_current_frame())

    def set_e2(self, item=None):
        if isinstance(item, QtGui.QListWidgetItem):
            self.ui.event2Label.setPixmap(item.icon().pixmap(300,200))
            self.e2 = int(item.toolTip())
        else:
            self.ui.event2Label.setPixmap(QtGui.QPixmap.fromImage(self.processor.get_current_image()).scaledToWidth(300))
            self.e2 = int(self.processor.get_current_frame())

    def goto_e1(self):
        self.processor.set_current_frame(self.e1)

    def goto_e2(self):
        self.processor.set_current_frame(self.e2)

    def return_events(self):
        return [self.e1, self.e2]

    def paintEvent(self,event):
        QtGui.QWidget.paintEvent(self,event)
        current = str(self.processor.get_current_frame())
        self.ui.currentFrameLabel.setText("Frame: " + current)

    def goto_frame(self):
        frame = int(self.ui.frameInput.text())
        self.processor.set_current_frame(frame)

    def next_frame(self):
        self.processor.frame_step()

    def previous_frame(self):
        self.processor.frame_step(reverse=True)

    def accept(self):
        file_path = "%s.%s.png" % (self.processor.path, str(self.e1))
        if os.path.exists(file_path) is False:
            self.ui.event1Label.pixmap().save(file_path,"PNG")
        file_path = "%s.%s.png" % (self.processor.path, str(self.e2))
        if os.path.exists(file_path) is False:
            self.ui.event2Label.pixmap().save(file_path,"PNG")
        QtGui.QDialog.accept(self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = VideoDialog(os.path.abspath("../img/Test_Set_rechts.mp4"))
    events = [52641,35044,2949,37899,58381,34553]
    dialog.set_events(events,[2949,52641])
    dialog.setWindowTitle('PyQt - OpenCV Test')
    print dialog.exec_()

    sys.exit(app.exec_())
