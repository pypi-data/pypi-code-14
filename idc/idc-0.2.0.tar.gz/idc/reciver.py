from OSC import OSCServer
import functools
import time
import logging

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
        """

        self.address = address
        self.dst_file_path = dst_file_path
        self.callbacks = callbacks
        self.addr_for_backup = addr_for_backup
        self.server = OSCServer(address)
        self.add_callbacks()
        self.motion = ['']

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
        self.motion[0] = data

    def set_file_callback(self, stream):

        def write_msg(path, tags, args, source):
            """
            :type msg: list
            :type stream: file
            :param msg:
            :param stream:
            :return:
            """
            motion_pointer = self.motion
            args.append(motion_pointer[0])
            args.insert(0, path)
            stream.write(
                ','.join(map(str, args))
            )
            stream.write('\n')

        for address in self.addr_for_backup:
            self.server.addMsgHandler(
                address,
                write_msg
            )

    def start(self):
        stream = open(self.dst_file_path, mode='wt')
        self.set_file_callback(stream)

        LOGGER.debug('Muse server is open on {}:{}'.format(
            self.address[0],
            self.address[1],
        ))
        # Blocking
        self.server.serve_forever()

        # if self.stop is called, close the backup file
        stream.close()

    def stop(self):
        self.server.close()
        LOGGER.debug('Muse server is closed')


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
