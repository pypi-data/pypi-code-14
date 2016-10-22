import sys
import logging
import argparse
import phase_manager
import config
import log_utils
import threading
import time

LOGGER = logging.getLogger(__name__)


def main(args):
    LOGGER.info('idc started')

    mg = phase_manager.PhaseManager.from_yaml('../sessions/sample.yaml')
    mg.add_next_instance_callback(on_next_instance)

    mg_thread = threading.Thread(target=mg.start, name='mg_thread')
    mg_thread.start()
    LOGGER.info('starting session in 5 seconds...')
    time.sleep(5)
    LOGGER.info('session started')
    mg.flag_up()
    mg_thread.join()

    '''
    mg = phase_manager.PhaseManager(
        [
            phase_manager.Phase(
                [
                    phase_manager.Instance("aaa", 1),
                    phase_manager.Instance("bbb", 1),
                    phase_manager.Instance("ccc", 1)
                ]
            )
        ]
    )
'''


def on_next_instance(msg):
    print msg

if __name__ == '__main__':
    log_utils.set_log()
    main(sys.argv[1:])

