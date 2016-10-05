import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QString

class ModelItem(QtGui.QStandardItem):
    def __init__(self):
        super(QtGui.QStandardItem,self).__init__(QString("Default Model"))
        self.setEditable(False)
        self.layouts = {}
        self.listeners = []
        self.default = ""
        self.path = "."
        self.status = None

    def update_status(self):
        status = 7
        for idx in range(self.rowCount()):
            self.child(idx).update_status()
            status = min(status, self.child(idx).get_status())
        if status != self.status:
            self.status = status
            self.emitDataChanged()

    def get_status(self):
        return self.status

    def set_path(self, a_path):
        self.path = a_path

    def get_path(self):
        return self.path

    def set_name(self, name):
        self.setText(name)

    def get_name(self):
        return self.text()

    def add_set(self, new_set):
        for idx in range(self.rowCount()):
            if new_set.get_name() == self.child(idx).text():
                return False
        self.appendRow(new_set)
        self.emitDataChanged()
        return True

    def has_set(self, name):
        for idx in range(self.rowCount()):
            if name == self.child(idx).text():
                return True
        return False

    def get_set(self, name):
        for idx in range(self.rowCount()):
            if name == self.child(idx).text():
                return self.child(idx)

    def get_set_names(self):
        names = []
        for idx in range(self.rowCount()): names.append(self.child(idx).text())
        return names

    def add_layout(self, layout):
        if not self.layouts.has_key(layout.get_name()):
            self.layouts[layout.get_name()] = layout
            if len(self.layouts) == 1:
                self.default = layout.get_name()
            self.emitDataChanged()
            return True
        return False

    def get_layout(self, name):
        return self.layouts[name]

    def get_layout_names(self):
        return self.layouts.keys()

    def get_default_layout(self):
        return self.layouts[self.default]

    def set_default_layout(self, layout):
        self.default = layout.get_name()

#===============================================================================
# Status 
# -1 = error
# 0 = unprepared
# 1 = in preparation
# 2 = prepared
# 3 = syncing
# 4 = syncs not validated
# 5 = synced
# 6 = create video
# 7 = done
#===============================================================================

class SetItem(QtGui.QStandardItem):
    def __init__(self, name):
        super(QtGui.QStandardItem,self).__init__(QString(name))
        self.setEditable(False)
        self.layout = None
        self.status = None
        self.listeners = []

    def add_audio(self, audio):
        if not isinstance(audio, AudioItem):
            audio = AudioItem(audio)
        self.appendRow(audio)

    def update_status(self):
        status = 7
        for idx in range(self.rowCount()):
            self.child(idx).update_status()
            status = min(status, self.child(idx).get_status())
        if status is not self.status:
            self.status = status
            self.emitDataChanged()

    def get_status(self):
        return self.status

    def get_name(self):
        return self.text()

    def set_layout(self, layout):
        if layout is not self.layout:
            self.layout = layout
            for idx, container_name in enumerate(layout.get_container_names()):
                if self.rowCount() > idx:
                    self.child(idx).setText(container_name)
                else:
                    new_container = ContainerItem(container_name)
                    self.appendRow(new_container)
            self.emitDataChanged()
            for listener in self.listeners: listener.set_layout_changed(self)

    def get_layout(self):
        return self.layout

    def get_container(self, template_name):
        for idx in range(self.rowCount()):
            if template_name == self.child(idx).text():
                return self.child(idx)
        return None

    def get_audios(self):
        a_list = []
        for idx in range(self.rowCount()):
            ch = self.child(idx)
            if isinstance(ch,AudioItem):
                a_list.append(ch)
        return a_list

    def set_status(self, status):
        self.status = status
        self.emitDataChanged()

class ContainerItem(QtGui.QStandardItem):
    def __init__(self, name):
        super(QtGui.QStandardItem,self).__init__(QString(name))
        self.setEditable(False)
        self.syncevents = {}
        self.original = False
        self.status = -1
        self.listeners = []
        self.path = None
        self.used_events = []

    def update_status(self):
        if self.rowCount() < 1:
            self.status = -1
            return

        status = max(0, self.status)
        for idx in range(self.rowCount()):
            self.child(idx).update_status()
            if not self.child(idx).get_status():
                status = -1
        if status != self.status:
            self.status = status

    def get_status(self):
        return self.status

    def get_name(self):
        return self.text()

    def add_file(self, file_path):
        file_item = FileItem(file_path)
        self.appendRow(file_item)
        self.status = 0
        self.emitDataChanged()
        return True

    def set_used_events(self, events):
        self.used_events = events

    def get_used_events(self):
        return self.used_events

    def add_sync_event(self, frame, confidence):
        if frame > 0:
            self.syncevents[frame] = confidence
            return True
        return False

    def get_sync_events(self):
        return self.syncevents

    def set_status(self, status_number):
        if self.status is not status_number:
            self.status = status_number
            self.emitDataChanged()

    def use_original(self):
        return self.original

    def set_original(self, use_original):
        self.original = use_original
        self.emitDataChanged()

    def get_file(self, index):
        return self.child(index)

    def get_file_count(self):
        return self.rowCount()

    def remove_file(self, a_file):
        for idx in range(self.rowCount()):
            if a_file.text() == self.child(idx).text():
                self.removeRow(idx)
                self.emitDataChanged()
        if self.rowCount() < 1:
            self.status = -1

    def move_file(self, a_file, diff):
        print "FAIL IMPLEMENT THAT RIGHT"

class FileItem(QtGui.QStandardItem):
    def __init__(self, path):
        super(QtGui.QStandardItem,self).__init__(QString(path))
        self.setEditable(False)
        self.setRowCount(0)
        self.status = 0
        self.update_status()

    def get_status(self):
        return self.status

    def update_status(self):
        status = os.path.exists(self.text())
        if self.status is not status:
            self.status = status

    def get_path(self):
        return str(self.text())

class AudioItem(FileItem):
    def __init__(self, path):
        FileItem.__init__(self, path)
        self.sync = None
        self.events = []
        self.container = None

    def set_sync(self, sync_time):
        self.sync = sync_time

    def set_events(self, events):
        self.events = events

    def get_events(self):
        return self.events

    def get_sync(self):
        return self.sync

    def set_status(self, status):
        if self.status is not status:
            self.status = status
            self.emitDataChanged()

    def update_status(self):
        if os.path.exists(self.get_path()) is True:
            status = max(self.status, 2)
        else:
            status = -1
        if self.status is not status:
            self.status = status

# Not View Related
class SetLayout:
    def __init__(self, name):
        self.name = name
        self.containers = {}
        self.width = 100
        self.height = 100
        self.listeners = []
        self.ref = ""

    def set_ref_name(self, ref):
        self.ref = ref

    def get_ref_name(self):
        return self.ref

    def get_name(self):
        return self.name

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_dimension(self, width, height):
        if width > 0 and height > 0:
            self.width = width
            self.height = height
            return True
        return False

    def get_container_names(self):
        container_names = []
        for container in sorted(self.containers.values()):
            container_names.append(container.get_name())
        return container_names

    def get_container(self, name):
        return self.containers[name]

    def add_container(self, container):
        self.containers[container.get_name()] = container

class ContainerLayout:
    def __init__(self, name):
        self.name = name
        self.pos_x = 0
        self.pos_y = 0
        self.width = 100
        self.height = 100
        self.listeners = []
        self._use_audio = False

    def set_use_audio(self, use_audio):
        self._use_audio = use_audio

    def use_audio(self):
        return self._use_audio

    def get_name(self):
        return self.name

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_position(self, x, y):
        if x >= 0 and y >= 0:
            self.pos_x = x
            self.pos_y = y

    def set_dimension(self, width, height):
        if width > 0 and height > 0:
            self.width = width
            self.height = height
