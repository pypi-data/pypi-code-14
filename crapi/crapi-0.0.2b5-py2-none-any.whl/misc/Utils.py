# Copyright (C) 2014/15 - Iraklis Diakos (hdiakos@outlook.com)
# Pilavidis Kriton (kriton_pilavidis@outlook.com)
# All Rights Reserved.
# You may use, distribute and modify this code under the
# terms of the ASF 2.0 license.
#

"""Part of the misc module."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import generators
# Python native libraries.
import os
import sys
import threading
import time

"""ReentrantRWLock.py - Read-Write lock thread lock implementation

See the class documentation for more info.

Copyright (C) 2007, Heiko Wundram.
Released under the BSD-license.

NOTE: Contains modification in method signature and condition in blocking
but core logic remains still the same.
Original source code URL:
http://code.activestate.com/recipes/502283-read-write-lock-class-rlock-like/
"""


class ReentrantRWLock(object):
    """Read-Write lock class. A read-write lock differs from a standard
    threading.RLock() by allowing multiple threads to simultaneously hold a
    read lock, while allowing only a single thread to hold a write lock at the
    same point of time.

    When a read lock is requested while a write lock is held, the reader
    is blocked; when a write lock is requested while another write lock is
    held or there are read locks, the writer is blocked.

    Writers are always preferred by this implementation: if there are blocked
    threads waiting for a write lock, current readers may request more read
    locks (which they eventually should free, as they starve the waiting
    writers otherwise), but a new thread requesting a read lock will not
    be granted one, and block. This might mean starvation for readers if
    two writer threads interweave their calls to acquireWrite() without
    leaving a window only for readers.

    In case a current reader requests a write lock, this can and will be
    satisfied without giving up the read locks first, but, only one thread
    may perform this kind of lock upgrade, as a deadlock would otherwise
    occur. After the write lock has been granted, the thread will hold a
    full write lock, and not be downgraded after the upgrading call to
    acquireWrite() has been match by a corresponding release().
    """

    def __init__(self):
        """Initialize this read-write lock."""

        # Condition variable, used to signal waiters of a change in object
        # state.
        self.__condition = threading.Condition(threading.Lock())

        # Initialize with no writers.
        self.__writer = None
        self.__upgradewritercount = 0
        self.__pendingwriters = []

        # Initialize with no readers.
        self.__readers = {}

    def acquireRead(self, blocking=True, timeout=0):
        """Acquire a read lock for the current thread, waiting at most
        timeout seconds or doing a non-blocking check in case timeout is <= 0.

        In case blocking is True, the call to acquireRead blocks until the
        lock request can be serviced.

        In case the timeout expires before the lock could be serviced, a
        RuntimeError is thrown."""

        if not blocking:
            endtime = time.time() + timeout
        me = threading.currentThread()
        self.__condition.acquire()
        try:
            if self.__writer is me:
                # If we are the writer, grant a new read lock, always.
                self.__writercount += 1
                return
            while True:
                if self.__writer is None:
                    # Only test anything if there is no current writer.
                    if self.__upgradewritercount or self.__pendingwriters:
                        if me in self.__readers:
                            # Only grant a read lock if we already have one
                            # in case writers are waiting for their turn.
                            # This means that writers can't easily get starved
                            # (but see below, readers can).
                            self.__readers[me] += 1
                            return
                        # No, we aren't a reader (yet), wait for our turn.
                    else:
                        # Grant a new read lock, always, in case there are
                        # no pending writers (and no writer).
                        self.__readers[me] = self.__readers.get(me, 0) + 1
                        return
                if not blocking:
                    remaining = endtime - time.time()
                    if remaining <= 0:
                        # Timeout has expired, signal caller of this.
                        raise RuntimeError("Acquiring read lock timed out!")
                    self.__condition.wait(remaining)
                else:
                    self.__condition.wait()
        finally:
            self.__condition.release()

    def acquireWrite(self, blocking=True, timeout=0):
        """Acquire a write lock for the current thread, waiting at most
        timeout seconds or doing a non-blocking check in case timeout is <= 0.

        In case the write lock cannot be serviced due to the deadlock
        condition mentioned above, a ValueError is raised.

        In case blocking is True, the call to acquireWrite blocks until the
        lock request can be serviced.

        In case the timeout expires before the lock could be serviced, a
        RuntimeError is thrown."""

        if not blocking:
            endtime = time.time() + timeout
        me, upgradewriter = threading.currentThread(), False
        self.__condition.acquire()
        try:
            if self.__writer is me:
                # If we are the writer, grant a new write lock, always.
                self.__writercount += 1
                return
            elif me in self.__readers:
                # If we are a reader, no need to add us to pendingwriters,
                # we get the upgradewriter slot.
                if self.__upgradewritercount:
                    # If we are a reader and want to upgrade, and someone
                    # else also wants to upgrade, there is no way we can do
                    # this except if one of us releases all his read locks.
                    # Signal this to user.
                    raise ValueError(
                        "Inevitable deadlock, write lock denied!"
                        )
                upgradewriter = True
                self.__upgradewritercount = self.__readers.pop(me)
            else:
                # We aren't a reader, so add us to the pending writers queue
                # for synchronization with the readers.
                self.__pendingwriters.append(me)
            while True:
                if not self.__readers and self.__writer is None:
                    # Only test anything if there are no readers and writers.
                    if self.__upgradewritercount:
                        if upgradewriter:
                            # There is a writer to upgrade, and it's us. Take
                            # the write lock.
                            self.__writer = me
                            self.__writercount = self.__upgradewritercount + 1
                            self.__upgradewritercount = 0
                            return
                        # There is a writer to upgrade, but it's not us.
                        # Always leave the upgrade writer the advance slot,
                        # because he presumes he'll get a write lock directly
                        # from a previously held read lock.
                    elif self.__pendingwriters[0] is me:
                        # If there are no readers and writers, it's always
                        # fine for us to take the writer slot, removing us
                        # from the pending writers queue.
                        # This might mean starvation for readers, though.
                        self.__writer = me
                        self.__writercount = 1
                        self.__pendingwriters = self.__pendingwriters[1:]
                        return
                if not blocking:
                    remaining = endtime - time.time()
                    if remaining <= 0:
                        # Timeout has expired, signal caller of this.
                        if upgradewriter:
                            # Put us back on the reader queue. No need to
                            # signal anyone of this change, because no other
                            # writer could've taken our spot before we got
                            # here (because of remaining readers), as the test
                            # for proper conditions is at the start of the
                            # loop, not at the end.
                            self.__readers[me] = self.__upgradewritercount
                            self.__upgradewritercount = 0
                        else:
                            # We were a simple pending writer, just remove us
                            # from the FIFO list.
                            self.__pendingwriters.remove(me)
                        raise RuntimeError("Acquiring write lock timed out!")
                    self.__condition.wait(remaining)
                else:
                    self.__condition.wait()
        finally:
            self.__condition.release()

    def release(self):
        """Release the currently held lock.

        In case the current thread holds no lock, a ValueError is thrown."""

        me = threading.currentThread()
        self.__condition.acquire()
        try:
            if self.__writer is me:
                # We are the writer, take one nesting depth away.
                self.__writercount -= 1
                if not self.__writercount:
                    # No more write locks; take our writer position away and
                    # notify waiters of the new circumstances.
                    self.__writer = None
                    self.__condition.notifyAll()
            elif me in self.__readers:
                # We are a reader currently, take one nesting depth away.
                self.__readers[me] -= 1
                if not self.__readers[me]:
                    # No more read locks, take our reader position away.
                    del self.__readers[me]
                    if not self.__readers:
                        # No more readers, notify waiters of the new
                        # circumstances.
                        self.__condition.notifyAll()
            else:
                raise ValueError("Trying to release unheld lock")
        finally:
            self.__condition.release()


class Environment(object):

    """A class that contains useful utility methods."""

    @staticmethod
    def getSourceFilePath(name, extensionless=False):

        try:
            src_file = sys.modules[
                name
            ].__file__
        except AttributeError:
            # Executable modules have no __file__ attribute defined.
            src_file = sys.executable

        if extensionless:
            return os.path.splitext(
                os.path.abspath(src_file)
            )[0]
        else:
            return src_file

    @staticmethod
    def getSourceFileDir(name):
        return os.sep.join(
            Environment.getSourceFilePath(name).split(os.sep)[:-1]
        )

    @staticmethod
    def getPyVirtualEnv(folder, name):
        venv = os.path.expanduser('~') + os.sep + folder + os.sep + name
        py_bin = 'python'
        if sys.platform.startswith('win'):
            py_bin += '.exe'
        return venv + os.sep + 'Scripts' + os.sep + py_bin
