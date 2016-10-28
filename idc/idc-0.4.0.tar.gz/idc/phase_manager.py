import utils
import logging
import time
import threading
import os
import config
import contextlib
import functools
import random
import numbers

from PyQt4.QtCore import *

LOGGER = logging.getLogger(__name__)

# base class for all classes that holds another objects


class Container(object):

    @classmethod
    def from_yaml(cls, path):
        raise NotImplementedError

    def __init__(self, childs=[]):

        self._childs = childs
        self._duration = self.calc_duration()

    def calc_duration(self):
        return sum([child.duration for child in self.childs])

    def gen_childs(self):
        for child in self.childs:
            yield child

    def run_child(self):
        raise NotImplementedError

    @property
    def childs(self):
        return self._childs

    @childs.setter
    def childs(self, data):
        self._childs = data

    @property
    def duration(self):
        return self._duration


class PhaseManager(QThread):

    THREAD_WAIT_INTERVAL = int(config.Config()['thread_wait_interval'])

    @classmethod
    def from_yaml(cls, path):
        LOGGER.debug('creating session from {0}'.format(path))
        phases = []
        data = utils.yaml_from_file(path)
        session = data['session']
        factor = data['settings']['factor']
        shuffle = data['settings']['shuffle']

        for phase in session:
            phase_object = Phase.decode_ds(phase)

            if factor and isinstance(factor, numbers.Number):
                phase_object.do_extend(factor, shuffle)
            else:
                if shuffle:
                    phase_object.do_shuffle()

            phases.append(phase_object)

        return PhaseManager(phases, settings=data['settings'])

    def __init__(self, phases=[], parent=None, settings=None):
        super(PhaseManager, self).__init__(parent=parent)

        # Thread configurations
        self.exiting = False

        self._childs = phases
        self._settings = settings
        LOGGER.debug('Current sessions settings: {}'.format(self._settings))

        self.next_phase_callbacks = []
        self.next_instance_callbacks = []
        # that wait method blocks until run_event
        # is true
        self._run_event = threading.Event()
        self.time_stamp_me = None

    @property
    def childs(self):
        return self._childs

    def __del__(self):
        """
        Before the worker is destroyed we need to ensure that it
        stops processing
        :return:
        """
        self.exiting = True
        self.wait()

    def do_start(self):
        self.start()

    def add_next_phase_callback(self, callback):
        self.next_phase_callbacks.append(callback)

    def add_next_instance_callback(self, callback):
        self.next_instance_callbacks.append(callback)

    def invoke(self, callback_list, msg):
        for callback in callback_list:
            callback(msg)

    def flag_up(self):
        self._run_event.set()

    def flag_down(self):
        self._run_event.clear()

    def run(self):

        # Returns a function
        self.time_stamp_me = utils.timestamp_with_offset()
        with self._open_fd():

            for idx, phase in enumerate(self.childs):
                LOGGER.info('{0} started'.format(phase))
                self.invoke(
                    self.next_phase_callbacks, phase
                )

                self.emit(SIGNAL('next_phase(int)'), idx)

                instances_gen = phase.gen_childs()

                for instance in instances_gen:
                    if not self._run_event.is_set():
                        LOGGER.info('flag is down, {0}'.format(threading.current_thread()))

                    self._run_event.wait()
                    self.run_child(instance)
                    if self._settings['break_duration']:
                        self.emit(SIGNAL('pause()'))
                        utils.do_in_intervals(
                            timeout=self._settings['break_duration'],
                            interval=self.THREAD_WAIT_INTERVAL,
                            report_interval=1000,
                            action=functools.partial(self.emit, SIGNAL('update_time(int)')),
                            sleep_func=self.msleep
                        )

            self.emit(SIGNAL('stop()'))
            LOGGER.debug('Sessions end')

    def run_child(self, instance):
        LOGGER.debug('flag is up {0}'.format(threading.current_thread()))

        time_tuple = self.time_stamp_me()

        # callback

        self.invoke(
            self.next_instance_callbacks,
            instance.media.rsplit('/', 1)[1].split('.')[0]
        )

        # qt signal
        self.emit(SIGNAL('next_video(QString)'), QString(instance.media))

        # write to file

        self._save_to_disk(time=time_tuple, name=instance.media)

        LOGGER.debug(instance)

        utils.do_in_intervals(
            timeout=instance.duration,
            interval=self.THREAD_WAIT_INTERVAL,
            report_interval=1000,
            action=functools.partial(self.emit, SIGNAL('update_time(int)')),
            sleep_func=self.msleep
        )

    @contextlib.contextmanager
    def _open_fd(self):
        file_name = utils.gen_filename('session')
        path = utils.join_path(
            config.Config().get_path_exp('artifacts_path'),
            file_name
        )

        self.fd = open(path, 'wt', buffering=100)
        LOGGER.debug('writing results to: {0}'.format(path))
        yield
        self.fd.close()

    def _close_fd(self):
        if self.fd is not None:
            self.fd.close()

    def _save_to_disk(self, **kwargs):
        self.fd.writelines(
            "{0},{1},{2}{nl}".format(
                kwargs['time'][0], # now
                kwargs['time'][1], # offset
                kwargs['name'],
                nl=os.linesep
            )
        )


class Phase(Container):

    __id = 0

    @classmethod
    def get_id(cls):
        """
        :Returns:
            id of the next instance
        """
        cls.__id += 1
        return cls.__id

    @classmethod
    def decode_ds(self, data):

        instances = data['instnaces']
        duration_per_instance = data['duration'] / len(instances)

        return Phase(
            [Instance(media=x, duration=duration_per_instance) for x in instances]
        )

    def __init__(self, instances=[]):
        super(Phase, self).__init__(instances)
        self._id = Phase.get_id()


    def run_child(self):
        pass

    @property
    def id(self):
        return self._id

    def __str__(self):
        return "Phase - {0}".format(self.id)

    def do_shuffle(self):
        random.shuffle(self.childs)

    def do_extend(self, factor=1, shuffle=False):
        if shuffle:
            l = self.childs[:]
            for i in range(0, factor):
                random.shuffle(l)
                self.childs += l
        else:
            self.childs *= factor


class Instance(object):

    __id = 0

    @classmethod
    def get_id(cls):
        """
        :Returns:
            id of the next instance
        """
        cls.__id += 1;
        return cls.__id

    def __init__(self, media, duration):
        """
        Args:
            id (int): serial number for this instance
            media (str): path to media (video / image)
            duration (float): the duration of this instance
        Returns:
        """
        self._id = Instance.get_id()
        self._media = os.path.join(
            config.Config().get_path_exp('media_path'),
            media,
        )
        self._duration = duration

    @property
    def id(self):
        return self._id

    @property
    def media(self):
        return self._media

    @property
    def duration(self):
        return self._duration

    def __str__(self):
        return "id = {0}, media = {1}, duration = {2}\n".format(
            self.id,
            self.media,
            self.duration
        )


def test():
    pass

if __name__ == '__main__':
    test()
