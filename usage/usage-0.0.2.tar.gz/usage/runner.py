#!/usr/bin/env python
# coding: utf8

import os
import signal
import sys
import time

from xtls.colorful import colorful_print, Color

import eventloop


def _write_pid_file(pid_file, pid):
    import fcntl
    import stat

    try:
        fd = os.open(pid_file, os.O_RDWR | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        colorful_print('write pid file error : %s\nexiting...' % e, Color.RED)
        return -1

    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    assert flags != -1
    flags |= fcntl.FD_CLOEXEC
    r = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
    assert r != -1

    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 0, 0, os.SEEK_SET)
    except IOError:
        r = os.read(fd, 32)
        msg = 'usage already started' + ' at pid %s' % r if r else ''
        colorful_print(msg, Color.YELLOW)
        os.close(fd)
        return -1
    os.ftruncate(fd, 0)
    os.write(fd, str(pid))
    return 0


def daemon_start():
    def handle_exit(signum, _):
        if signum == signal.SIGTERM:
            sys.exit(0)
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    pid = os.fork()
    assert pid != -1

    if pid > 0:
        time.sleep(5)
        sys.exit(0)

    ppid = os.getppid()
    pid = os.getpid()

    if _write_pid_file('/Users/xlzd/.usage/pid', pid) != 0:
        os.kill(ppid, signal.SIGINT)
        sys.exit(1)

    os.setsid()
    signal.signal(signal.SIG_IGN, signal.SIGHUP)

    colorful_print('usage started', Color.GREEN)
    os.kill(ppid, signal.SIGTERM)

    sys.stdin.close()


def start():
    daemon_start()

    loop = eventloop.EventLoop()

    def handler(signum, _):
        print 'received SIGQUIT, doing graceful shutting down..', signum

    signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM), handler)

    def int_handler(signum, _):
        sys.exit(1)

    signal.signal(signal.SIGINT, int_handler)

    loop.run()


def stop():
    import errno
    try:
        with open('/Users/xlzd/.usage/pid') as f:
            pid = f.read()
            if not pid:
                colorful_print('usage is not running', Color.RED)
    except IOError as e:
        if e.errno == errno.ENOENT:
            return colorful_print('usage is not running', Color.RED)
        sys.exit(1)

    pid = int(pid)
    if pid <= 0:
        colorful_print('usage pid is not positive: %d' % pid, Color.RED)
    else:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                return colorful_print('usage pid is not running: %d' % pid, Color.RED)
            colorful_print('error, exiting...', Color.RED)
            sys.exit(1)

    # for i in range(0, 5):
    #     try:
    #         os.kill(pid, 0)
    #     except OSError as e:
    #         print '>>>', i, e
    #         if e.errno == errno.ESRCH:
    #             break
    #     time.sleep(0.1)
    # else:
    #     colorful_print('timed out when stopping pid %d' % pid, Color.RED)
    #     sys.exit(1)

    colorful_print('usage stopped', Color.GREEN)
    os.unlink('/Users/xlzd/.usage/pid')
