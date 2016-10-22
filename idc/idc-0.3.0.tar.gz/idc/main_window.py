from PyQt4.QtGui import *
from PyQt4.QtCore import *


import sys
import logging
import multiprocessing
import threading
import time

import main_view
import log_utils
import phase_manager
import reciver
import utils
import config
import qt_vlc
import testlib
import os

LOGGER = logging.getLogger(__name__)

Daemon_Cls = threading.Thread
TEST_MODE = False


class MainView(QMainWindow, main_view.Ui_MainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        self.setupUi(self)

        self.setup_btn_slots()
        self.btn_start.setEnabled(False)

        self.callbacks = {
            '/muse/elements/horseshoe': self.update_hs,
            '/muse/elements/touching_forehead': self.update_headband
        }
        self.muse = self.setup_muse()

        self.muse_thread = Daemon_Cls(
            target=self.muse.start,
            name='muse_thread'
        )
        self.muse_thread.setDaemon(daemonic=True)
        self.muse_thread.start()
        self.setup_muse_slots()

        # vlc instance that will be used to play the sample videos
        self.vlc_instance = qt_vlc.Player(self)
        self.vlc_instance.resize(640, 480)
        self.vlc_instance.show()

        self.manager = None

        if TEST_MODE:
            self.run_tests()

    def run_tests(self):
        # Muse Mock Test
        muse_mock = testlib.MuseMock(
            sample_rate=200,
            data_src='../test/muse_data_test',
            server_addr=('localhost', 5000),
        )
        muse_mock.setDaemon(True)
        time.sleep(2)
        muse_mock.start()
        muse_mock.run_flag = True

    def load(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open File",
            os.path.expanduser('~')
        )

        self.manager = phase_manager.PhaseManager.from_yaml(filename)
        self.manager.add_next_instance_callback(self.muse.set_motion)
        self.setup_slots()
        self.btn_start.setEnabled(True)
        self.instance_list.clear()

    def setup_list(self, idx=0):
        for instance in self.manager.childs[idx].childs:
            item = QListWidgetItem("{}".format(instance.media))
            self.instance_list.addItem(item)

    def setup_muse(self):
        conf = config.Config()
        channels_to_save = conf['channels_to_save']
        channels_to_save = channels_to_save.replace(' ', '').split(',')
        LOGGER.debug('channels to save: {}'.format(channels_to_save))

        return reciver.Muse(
            address=(conf['server_ip'], int(conf['server_port'])),
            dst_file_path=utils.join_path(
                base_name=utils.gen_filename('muse_record'),
                path=conf.get_path_exp('output_file_path')
            ),
            callbacks=self.callbacks,
            addr_for_backup=channels_to_save
        )

    def start_session(self):
        LOGGER.debug("session started")
        if not self.manager.isRunning():
            self.manager.do_start()

        self.btn_start.setEnabled(False)
        self.btn_load.setEnabled(False)
        self.manager.flag_up()

    def pause_session(self):
        LOGGER.debug("session paused")
        if self.manager:
            self.manager.flag_down()
        self.btn_start.setEnabled(True)
        self.btn_load.setEnabled(True)
        self._stop_video()
        self.muse.stop()

    def pause_video(self):
        """
            pause is the break between videos
        :return:
        """
        LOGGER.debug('video paused')
        # self.video_play.pause()
        self.vlc_instance.Stop()

    def next_phase(self, idx):
        self.setup_list(idx)

    def setup_btn_slots(self):
        self.btn_start.clicked.connect(self.start_session)
        self.btn_stop.clicked.connect(self.pause_session)
        self.btn_load.clicked.connect(self.load)

    def setup_muse_slots(self):
        self.connect(self, SIGNAL('_update_hs(QString)'), self._update_hs)
        self.connect(self, SIGNAL('_update_headband(int)'), self._update_headband)

    def setup_slots(self):
        self.connect(self.manager, SIGNAL('next_video(QString)'), self._play_video)
        self.connect(self.manager, SIGNAL('stop()'), self.pause_session)
        self.connect(self.manager, SIGNAL('update_time(int)'), self.update_clock)
        self.connect(self.manager, SIGNAL('next_phase(int)'), self.next_phase)

        # pause is the break between videos
        self.connect(self.manager, SIGNAL('pause()'), self.pause_video)

    def _update_hs(self, args):
        args = str(args).split(',')

        for idx, status in enumerate(args):
            label = getattr(self, 'hs_{}'.format(idx))

            if status == '1.0':
                color = "QLabel { background-color : green; color : white; }"
            elif status == '2.0':
                color = "QLabel { background-color : yellow; color : white; }"
            else:
                color = "QLabel { background-color : red; color : white; }"

            label.setStyleSheet(color)

    def _update_headband(self, args):
        if args:
            color = "QLabel { background-color : green; color : white; }"
        else:
            color = "QLabel { background-color : red; color : white; }"

        self.headband.setStyleSheet(color)

    def update_hs(self, path, tags, args, source):
        data = ','.join(map(str, args))
        self.emit(SIGNAL('_update_hs(QString)'), QString(data))

    def update_headband(self, path, tags, args, source):
        self.emit(SIGNAL('_update_headband(int)'), args[0])

    def start_capture_vid(self):
        pass

    def stop_capture_vid(self):
        pass

    def start_rec_vid(self):
        pass

    def stop_rec_vid(self):
        pass

    def update_clock(self, data):
        self.clock.display(data)

    def _play_video(self, path):
        """
        :type path: QString
        :param path:
        :return:
        """
        # Video playback using opencv
        # self.video_play.next_video(str(path))

        # Video playback using vlc
        self.instance_list.takeItem(0)
        self.vlc_instance.next_instance(path)

    def _stop_video(self):
        self.vlc_instance.Stop()


def main():
    log_utils.set_log()
    app = QApplication(sys.argv)
    w = MainView()
    w.show()
    app.exec_()


def setup_manager():
    pass

if __name__ == '__main__':
    main()
