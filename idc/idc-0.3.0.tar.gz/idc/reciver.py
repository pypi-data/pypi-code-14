from OSC import OSCServer
import functools
import time
import logging
import Queue
import threading

LOGGER = logging.getLogger(__name__)


class Muse:

    def __init__(self, address, dst_file_path, callbacks={}, addr_for_backup=[]):
        """
            address - (ip, port)

            :type address: tuple
            address and port to listen to
            :type dst_file_path: str
            path to the file in which the data will be stored
            :type addr_for_backup: list
            osc msg that their content should be save to disk
            :type callbacks: dict
            mapping from osc addresses to functions
            :type has_changed: bool
            Flag which indicates if the motion has changed
        """

        self.address = address
        self.dst_file_path = dst_file_path
        self.callbacks = callbacks
        self.addr_for_backup = addr_for_backup
        self.server = OSCServer(address)
        self.add_callbacks()
        self.motion = ['']
        self.q = Queue.PriorityQueue()
        self.writer_thread = None
        self.start_time = time.time()

        self.callback_counter = 0

    def write(self, stop_flag):
        """
        writer thread logic
        :param stop_flag:
        :return:
        """

        with open(self.dst_file_path, mode='wt') as stream:
            while stop_flag:
                item = self.q.get()
                if item.data == 'EOF':
                    break
                stream.write(
                    ','.join(map(str, item.data))
                )
                stream.write('\n')
                self.q.task_done()

        print 'Writer end'

    def add_callbacks(self):
        for address, callback in self.callbacks.items():
            self.server.addMsgHandler(address, callback)

        # Add default handler
        self.server.addMsgHandler(
            'default',
            lambda *args: None
        )

    # not using decorator because I wish to pass this function
    # as an argument
    def set_motion(self, data):
        time_offset = self._get_time_offset()
        l = [
            'TRG',
            time_offset,
            data,
            '',
            '',
            '',
        ]
        self.q.put(
            Item(data=l, arrival_time=time_offset, priority=0)
        )

    def set_file_callback(self):

        def write_msg_to_q(path, tags, args, source):
            """
            :type msg: list
            :type stream: file
            :param msg:
            :param stream:
            :return:
            """
            # fix the size of the data
            args_len = len(args)
            if args_len < 4:
                diff = 4 - args_len
                for i in range(0, diff):
                    args.append = ''

            # add the event's time
            time_offset = self._get_time_offset()
            args.insert(0, time_offset)

            # add the data source
            args.insert(0, path)
            self.q.put(
                Item(data=args, arrival_time=time_offset, priority=0)
            )

            self.callback_counter += 1

        for address in self.addr_for_backup:
            self.server.addMsgHandler(
                address,
                write_msg_to_q
            )

    def _get_time_offset(self):
        return round(
                time.time() - self.start_time,
                3
            )

    def start(self):
        self.set_file_callback()
        stop_flag = ['EOF']
        self.writer_thread = threading.Thread(
            target=self.write,
            name='Writer',
            kwargs={'stop_flag': stop_flag}
        )
        self.writer_thread.setDaemon(True)
        self.writer_thread.start()

        LOGGER.debug('Muse server is open on {}:{}'.format(
            self.address[0],
            self.address[1],
        ))
        # Blocking
        self.server.serve_forever()
        self.q.put(
            Item(
                data=stop_flag.pop(),
                arrival_time=0,
            )
        )

    def stop(self):
        self.server.close()
        LOGGER.debug('Muse server is closed')
        print 'callback-counter - {}'.format(self.callback_counter)


class Item:
    def __init__(self, data, arrival_time, priority=0):
        self._priority = priority
        self._arrival_time = arrival_time
        self._data = data

    @property
    def arrival_time(self):
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, new):
        self._arrival_time = new

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, new):
        self._priority = new

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new):
        self._data = new

    def __cmp__(self, other):
        if not isinstance(other, Item):
            raise TypeError('{} is not an Item'.format(other))

        if self.priority > other.priority:
            return 1
        elif self.priority < other.priority:
            return -1
        else:
            if self.arrival_time > other.arrival_time:
                return 1
            else:
                return -1

def dummy(path, tags, args, source):
    pass

def main():
    muse = Muse(
        address=("192.168.122.146", 5000),
        dst_file_path='output.csv',
        callbacks={'/muse/acc': dummy},
        addr_for_backup=['/muse/eeg'],
    )

    muse.start()

if __name__ == '__main__':
    main()
