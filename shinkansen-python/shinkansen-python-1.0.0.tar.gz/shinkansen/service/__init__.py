from __future__ import print_function
import imp
import logging
import logging.config
import multiprocessing
import os
import signal
import sys

import daemon
from daemon import runner
from lockfile import pidlockfile, LockError
import psutil


class ShutdownException(Exception):
    pass


def main(args):
    if args['--daemonize']:
        acquire_pidfile_path = args['--pidfile'] + '.acquirelock'
        pidfile = pidlockfile.PIDLockFile(args['--pidfile'], timeout=0)
        # If the first pidfile is stale, use another pid lockfile to make sure we're not
        # racing someone else. This lockfile should be far less likely to be stale since
        # it is only kept during this check and breaking the stale lock.
        try:
            with pidlockfile.PIDLockFile(acquire_pidfile_path, timeout=0):
                if runner.is_pidfile_stale(pidfile):
                    print('Stale lockfile detected, breaking the stale lock %s' % (args['--pidfile'],))
                    pidfile.break_lock()
        except LockError:
            print('Got an exception while attempting to check for a stale main pidfile.')
            print('There is likely to be a stale acquire pidfile at %s' % (acquire_pidfile_path,))
            raise
        with daemon.DaemonContext(
            pidfile=pidfile,
            working_directory=os.getcwd(),
            stdout=open('log/stdout.log', 'a+'),
            stderr=open('log/stderr.log', 'a+'),
        ):
            run(args['--config'])
    else:
        run(args['--config'])


def http_worker():
    from shinkansen import config
    from shinkansen import http

    http.app.run(port=config.HTTP_PORT, host=config.HTTP_HOST)  # debug=True)


def apply_db_patches():
    from shinkansen.orm import patch
    patch.apply_patches()


def run(configfile):
    if configfile is not None:
        (config_dir, config_file) = os.path.split(configfile)
        (config_name, config_ext) = os.path.splitext(config_file)
        if not config_ext == '.py':
            print('configfile should be a python file (end in .py)')
            sys.exit(1)
        module_args = imp.find_module(config_name, [config_dir])
        imp.load_module('config_local', *module_args)

    signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    signal.signal(signal.SIGUSR2, signal.SIG_IGN)

    from shinkansen import config

    if not os.path.exists(config.SSH_PRIVKEY):
        print('SSH_PRIVKEY file does not exist %s' % (config.SSH_PRIVKEY,))
        sys.exit(1)
    if not os.path.exists(config.LOGGING_INI):
        print('LOGGING_INI file does not exist %s' % (config.LOGGING_INI))
        sys.exit(1)
    logging.config.fileConfig(config.LOGGING_INI)
    log = logging.getLogger(__name__)

    from shinkansen import worker

    for directory in [worker.SOURCE_DIR, worker.DESTINATION_DIR, worker.BACKUP_DIR]:
        if not os.path.exists(directory) and not os.path.lexists(directory):
            os.makedirs(directory)

    # TODO(jpatrin): get this from the LOGGING_INI
    config.CELERYD_LOG_FORMAT = '%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(thread)d-%(threadName)s] [%(name)s] %(message)s'

    if config.QUEUE_SYSTEM == 'multiprocessing':
        from shinkansen import lock
        from shinkansen.orm import memredis

        manager = multiprocessing.Manager()
        memredis.MemRedis.init(manager)
        lock.MemLock.init(manager)

    apply_db_patches()

    from shinkansen.worker.master import MigrationWorkerMaster

    master = MigrationWorkerMaster()
    http_proc = multiprocessing.Process(target=http_worker)
    try:
        log.info('Starting master')
        master.start()

        log.info('Starting HTTP listener')
        http_proc.start()

        def stop_http_worker():
            try:
                proc = psutil.Process(http_proc.pid)
                proc.send_signal(signal.SIGINT)
            except psutil.NoSuchProcess:
                pass

        def handle_sigusr1(signum, frame):
            log.info('Shutting down master gracefully')
            stop_http_worker()
            master.shutdown()
            raise ShutdownException('graceful')

        def handle_sigusr2(signum, frame):
            log.info('Shutting down master quickly')
            stop_http_worker()
            master.shutdown(graceful=False)
            raise ShutdownException('quick')

        signal.signal(signal.SIGUSR1, handle_sigusr1)
        signal.signal(signal.SIGUSR2, handle_sigusr2)
        master.join()
    except ShutdownException:
        while True:
            try:
                master.join()
                break
            except ShutdownException:
                pass
    finally:
        if http_proc.is_alive():
            http_proc.terminate()
            http_proc.join()
        if master.is_alive():
            log.info('Terminating master')
            master.terminate()
            master.join()
    log.info('Ending run()')


if __name__ == '__main__':
    main()
