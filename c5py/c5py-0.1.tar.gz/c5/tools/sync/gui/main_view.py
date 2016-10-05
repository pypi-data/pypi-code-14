from PyQt4 import QtGui
from PyQt4 import QtCore

from mainViewUi import Ui_MainWindow
import os.path

import pygame.mixer

from .cvvideowidget import VideoDialog
from ..model import itemmodel


class MainWindow(QtGui.QMainWindow):
    def __init__(self, a_model):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.progress = None

        self.icon_set=False

        self.model = QtGui.QStandardItemModel()
        a_model.listeners.append(self)
        tree_root = self.model.invisibleRootItem()
        tree_root.appendRow(a_model)
        self.ui.outline.setModel(self.model)

        self.ui.outline.clicked.connect(self.outline_item_selected)
        self.ui.createSetButton.clicked.connect(self.create_set)
        self.ui.newSetName.textEdited.connect(self.check_set_name)
        self.ui.layoutChooserAddSet.activated.connect(self.add_set_preview_changed)
        self.ui.setLayoutButton.clicked.connect(self.set_layout)
        self.ui.addFileButton.clicked.connect(self.add_file)
        self.ui.moveUp.clicked.connect(self.move_file_up)
        self.ui.moveDown.clicked.connect(self.move_file_down)
        self.ui.removeFile.clicked.connect(self.remove_file)
        self.ui.changeSyncButton.clicked.connect(self.call_sync_dialog)
        self.ui.addAudioButton.clicked.connect(self.add_audio)
        self.ui.removeAudio.clicked.connect(self.remove_audio)
        self.ui.playSampleButton.clicked.connect(self.play_sample)
        self.ui.changeAudioButton.clicked.connect(self.resync_audio)
        self.ui.verifyButton.clicked.connect(self.verify_syncs)
        self.ui.verifyAudioButton.clicked.connect(self.verify_syncs)
        self.ui.removeSetButton.clicked.connect(self.remove_set)

        self.ui.outline.setCurrentIndex(a_model.index())
        self.ui.widgetStack.setCurrentIndex(0)
        self.ui.outline.setExpanded(a_model.index(), True)
        self.ui.previewContainer.setEditable(False)
        self.ui.previewAddSet.setEditable(False)
        self.ui.previewEditSet.setEditable(False)
        self.model.itemChanged.connect(self.model_changed)

    #    self.ui.containerTabs.currentChanged.connect(self.container_tab_changed)

        for idx in range(a_model.rowCount()):
            a_model.child(idx).emitDataChanged()

        self.update_layout_view()
        self.add_set_preview_changed(None)

    def set_busy(self):
        self.progress = QtGui.QProgressDialog("Processing...", "Hide", 0, 100, self)
        self.progress.setWindowModality(1)
        self.progress.setValue(0)

        self.timer = QtCore.QTimer(self);
        self.timer.timeout.connect(self.timer_tick)
        self.timer.start(1000);

    def timer_tick(self):
        if self.progress.wasCanceled():
            self.timer.stop()
            self.close()

        if self.listener.is_busy() is False:
            self.timer.stop()
            self.reset_busy()

    def closeEvent(self, event):
        print "close event"
        self.model.invisibleRootItem().takeRow(0)
        self.listener.gui_shutdown()
        QtGui.QMainWindow.closeEvent(self, event)

    def update_progress(self,progress):
        self.progress.setValue(progress)

    def reset_busy(self):
        self.progress.accept()

    def verify_syncs(self):
        an_item= self.model.itemFromIndex(self.ui.outline.currentIndex())
        an_item.set_status(5)

    def resync_audio(self):
        audio = self.model.itemFromIndex(self.ui.outline.currentIndex())
        guess_string = self.ui.changeAudioEdit.text()
        if len(guess_string) == 0:
            guess = None
        else:
            guess = float(guess_string)
        self.listener.sync_audio(audio, initial_guess = guess, force_exact_time = self.ui.forceExactTime.isChecked())

    def play_sample(self):
        audio = self.model.itemFromIndex(self.ui.outline.currentIndex())
        pygame.mixer.init()
        pygame.mixer.music.load(audio.get_path()+".sync.wav")
        pygame.mixer.music.play()

    def remove_audio(self):
        item = self.model.itemFromIndex(self.ui.outline.currentIndex())
        a_set = item.parent()
        a_set.removeRow(item.row())
        a_set.emitDataChanged()

    def add_audio(self):
        a_set = self.model.itemFromIndex(self.ui.outline.currentIndex())
        file_path = QtGui.QFileDialog.getOpenFileName(self, "Add Audio",".", "WAV (*.wav)")
        a_set.add_audio(str(file_path))

    def call_sync_dialog(self):
        container = self.model.itemFromIndex(self.ui.outline.currentIndex())
        dialog = VideoDialog(container.path)
        dialog.set_events(container.get_sync_events().keys(), container.get_used_events())
        dialog.setWindowTitle('SyncEvent')
        status = dialog.exec_()
        if status > 0:
            container.set_used_events(dialog.return_events())

    def model_changed(self, item):
        if self.icon_set is True:
            self.icon_set = False
            return

        elif isinstance(item, itemmodel.ModelItem):
            status = item.get_status()
            self.ui.prepareButton.setEnabled(status == 0)
            self.ui.syncButton.setEnabled(status == 2)
            self.ui.mergeButton.setEnabled(status == 5)

        elif isinstance(item, itemmodel.SetLayout):
            self.update_layout_view()

        elif isinstance(item, itemmodel.ContainerItem):
            item.parent().emitDataChanged()

        elif isinstance(item, itemmodel.SetItem):
            item.parent().update_status()
            if item.get_status() % 2 == 0:
                self.set_icon(item, 1)
            else:
                self.set_icon(item, -1)

            for idx1 in range(item.rowCount()):
                container = item.child(idx1)
                if container.get_status() < 0:
                    self.set_icon(container, -1)
                elif container.get_status() in [0,2,5]:
                    self.set_icon(container, 1)
                for idx2 in range(container.rowCount()):
                    a_file = container.child(idx2)
                    if a_file.get_status() is True:
                        self.set_icon(a_file, 1)
                    else:
                        self.set_icon(a_file, -1)

    def set_icon(self, item, status):
        if status > 0:
            icon = QtGui.QIcon("img/okay.png")
        elif status < 0:
            icon = QtGui.QIcon("img/error.png")
        else:
            icon = QtGui.QIcon("img/unknown.png")
        self.icon_set = True
        item.setIcon(icon)

    def add_file(self):
        file_path = QtGui.QFileDialog.getOpenFileName(self, "Add File",".", "Video Files (*.mts *.mp4 *.avi *.mpeg *.mpg *.ogv)")
        container = self.model.itemFromIndex(self.ui.outline.currentIndex())
        container.add_file(file_path)

    def remove_file(self):
        item = self.model.itemFromIndex(self.ui.outline.currentIndex())
        container = item.parent()
        container.removeRow(item.row())
        container.emitDataChanged()

    #TODO: Implement
    def move_file_up(self):
        self.move_file_diff(-1)

    #TODO: Implement
    def move_file_down(self):
        self.move_file_diff(1)

    def move_file_diff(self, diff):
        a_file = self.model.itemFromIndex(self.ui.outline.currentIndex())
        new_row = max(0, min(a_file.row()+diff, a_file.parent().rowCount()-1))

        if new_row != a_file.row():
            container = a_file.parent()
            container.takeRow(a_file.row())
            container.insertRow(new_row, a_file)
            self.ui.outline.setCurrentIndex(a_file.index())

    def set_layout(self):
        a_set = self.model.itemFromIndex(self.ui.outline.currentIndex())
        self.listener.set_layout(str(a_set.text()),str(self.ui.layoutChooserEditSet.currentText()))

    def remove_set(self):
        a_set = self.model.itemFromIndex(self.ui.outline.currentIndex())
        a_set.parent().removeRow(a_set.row())

    def add_set_preview_changed(self, index):
        layout = self.model.item(0).get_layout(str(self.ui.layoutChooserAddSet.currentText()))
        self.ui.previewAddSet.setLayout(layout)

    def set_listener(self, listener):
        self.listener = listener
        self.ui.prepareButton.clicked.connect(self.listener.merge_files)
        self.ui.syncButton.clicked.connect(self.listener.detect_syncs)
        self.ui.mergeButton.clicked.connect(self.listener.create_movies)

    def outline_item_selected(self, index):
        item = self.model.itemFromIndex(index)
        if isinstance(item, itemmodel.ModelItem):
            idx = 0
        elif isinstance(item, itemmodel.SetItem):
            idx = 1
        elif isinstance(item, itemmodel.ContainerItem):
            idx = 2
        elif isinstance(item, itemmodel.AudioItem):
            idx = 3
        else:
            idx = 4

        self.ui.widgetStack.setCurrentIndex(idx)
        self.stack_changed(idx, index)

    def stack_changed(self, idx, index):
        if self.ui.widgetStack.indexOf(self.ui.editSet) == idx:
            set = self.model.itemFromIndex(index)
            layout_name = set.get_layout().get_name()
            self.ui.layoutChooserEditSet.setCurrentIndex(self.ui.layoutChooserEditSet.findText(layout_name))
            self.ui.previewEditSet.setLayout(set.get_layout())
        elif self.ui.widgetStack.indexOf(self.ui.editContainer) == idx:
            self.ui.containerTabs.setCurrentIndex(0)
            container = self.model.itemFromIndex(index)
            self.ui.containerName.setText("Name: %s" % (container.get_name()))
            if container.get_status() < 2:
                status = "not prepared"
            elif container.get_status() < 4:
                status = "not synced"
            else:
                status = "ready"
            self.ui.previewContainer.setLayout(container.parent().get_layout())
            self.ui.previewContainer.setSelected(container.get_name())
            self.ui.containerName.setText("Name: %s" % (container.get_name()))
            self.ui.containerStatus.setText("Status: %s" % (status))
            self.ui.containerTabs.setTabEnabled(1,container.get_status() > 3)
            self.ui.containerTabs.setTabEnabled(2,container.get_status() > 3)
            if container.get_status() > 3:
                events = container.get_used_events()
                print "%s.%s.png" % (container.path, str(events[0]))
                i1 = QtGui.QPixmap("%s.%s.png" % (container.path, str(events[0])), "PNG").scaledToHeight(200)
                i2 = QtGui.QPixmap("%s.%s.png" % (container.path, str(events[1])), "PNG").scaledToHeight(200)

                self.ui.event1pic.setPixmap(i1)
                self.ui.event2pic.setPixmap(i2)

                all_secs = int(events[0]) / 25
                secs = str(all_secs % 60).zfill(2)
                mins = str((all_secs/60) % 60).zfill(2)
                hours = str(all_secs/3600).zfill(2)
                time_string = "%s:%s:%s" % (hours,mins,secs)
                self.ui.event1text.setText(time_string)

                all_secs = int(events[1]) / 25
                secs = str(all_secs % 60).zfill(2)
                mins = str((all_secs/60) % 60).zfill(2)
                hours = str(all_secs/3600).zfill(2)
                time_string = "%s:%s:%s" % (hours,mins,secs)
                self.ui.event2text.setText(time_string)

        elif self.ui.widgetStack.indexOf(self.ui.editFile) == idx:
            a_file = self.model.itemFromIndex(self.ui.outline.currentIndex())
            self.ui.filenameLabel.setText(os.path.basename(a_file.get_path()))

        elif self.ui.widgetStack.indexOf(self.ui.editAudio) == idx:
            audio = self.model.itemFromIndex(self.ui.outline.currentIndex())
            self.ui.audioLabel.setText(os.path.basename(audio.get_path()))
            event = audio.get_sync()
            if event is None: event = "not set"
            self.ui.audioSyncLabel.setText(str(event))

    def create_set(self):
        self.listener.create_set(str(self.ui.newSetName.text()).strip(), str(self.ui.layoutChooserAddSet.currentText()).strip())
        self.ui.newSetName.setText(QtCore.QString(""))
        if self.ui.setDefaultLayout.isChecked() is True:
            self.ui.setDefaultLayout.setChecked(False)
            new_layout = self.model.item(0).get_layout(str(self.ui.layoutChooserAddSet.currentText()).strip())
            self.model.item(0).set_default_layout(new_layout)

        layout = self.model.item(0).get_default_layout()
        self.ui.layoutChooserAddSet.setCurrentIndex(self.ui.layoutChooserAddSet.findText(layout.get_name()))
        self.ui.previewAddSet.setLayout(layout)

    def check_set_name(self, q_string):
        name = str(q_string).strip()
        if self.model.item(0).has_set(name):
            self.ui.createSetButton.setEnabled(False)
        else:
            self.ui.createSetButton.setEnabled(True)

    def update_layout_view(self):
        self.ui.layoutChooserAddSet.clear()
        self.ui.layoutChooserEditSet.clear()
        model = self.model.item(0)
        for layout_name in model.get_layout_names():
            self.ui.layoutChooserAddSet.addItem(layout_name)
            self.ui.layoutChooserEditSet.addItem(layout_name)
        layout = model.get_default_layout()
        self.ui.layoutChooserAddSet.setCurrentIndex(self.ui.layoutChooserAddSet.findText(layout.get_name()))
