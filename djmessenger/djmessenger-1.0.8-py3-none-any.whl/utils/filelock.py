# Copyright (c) 2009, Evan Fosmark
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.
'''Cross platform mechanism to acquire and release a file lock. The module
uses additional lock file to mark if the file is currently used.

Example:
from filelock import FileLock
with FileLock('path_to_my_file'):
     # My operations with this files comes here
'''
import time
import os
import errno
import logging
import traceback
import sys

logger = logging.getLogger(__name__)


class FileLockException(Exception):
    '''Thrown if cannot acquire a file lock.
    '''
    pass


class FileLock(object):
    """ Implementation of cross platform file lock mechanism.
    """

    def __init__(self, filePath, delay=.05, timeout=60, strict=False):
        """ Creates file lock instance.

        @param filePath: File wanted to be locked
        @param delay: Specifies the sleeping time in seconds between each
            attempt of lock acquisition
        @param timeout: Specifies the maximum time in seconds for waiting to
            lock the file
        @param strict: Specifies the behavior if timeout has been exceeded.
            False(default) - Ignore timeout, and presume the file lock is created
            True - Throw exception because file lock hasn't been created
        """
        self.lockFile = filePath + ".upgradeLock"
        self.isLocked = False
        self.timeout = timeout
        self.delay = delay
        self.strict = strict

    def acquire(self):
        """ Acquires a file lock. If file lock has been already created, then
             waits until the file lock is released. If the file lock is not released
             and timeout elapsed then either throw Exception or ignore locking a file
             based on the value of strict parameter.
        """
        if self.isLocked:
            logger.debug('The lock has already been acquired. Skip new acquisition')
            return

        startTime = time.time()
        logger.debug('Acquiring lock %s', self.lockFile)
        while True:
            fd = None
            try:
                fd = os.open(self.lockFile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                self.isLocked = True
                break
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # Someone is using the file. This is fine, let retry.
                    pass
                elif e.errno == errno.EACCES:
                    # We got permission error. This file might have been used
                    # by another process with higher permission. Let leave the
                    # owner to release the file, so let keep retrying
                    logger.warn('Got permission error: %s', e)
                else:
                    logger.exception('Got OS error: %s', e)
                    raise

                # Retry logic
                if (time.time() - startTime) >= self.timeout:
                    # Timeout exceeded
                    if self.strict:
                        raise FileLockException("Cannot acquire a file lock %s. Timeout exceeded." % self.lockFile)
                    else:
                        logger.warning("Cannot acquire a file lock %s: %s", self.lockFile, e)
                        break

                time.sleep(self.delay)
            finally:
                # ensure we won't leave open handle
                if fd:
                    os.close(fd)

    def release(self):
        """ Releases file lock created by acquire method.
        """
        if self.isLocked:
            logger.debug('Releasing lock %s', self.lockFile)
            startTime = time.time()
            while True:
                try:
                    os.remove(self.lockFile)
                    self.isLocked = False
                    break
                except Exception as e:  # pylint: disable=W0703
                    # log the actual reason for failure and retry
                    logger.warning("Cannot release the file lock: %s. %s", e, traceback.extract_stack())
                    # Retry logic
                    if (time.time() - startTime) >= self.timeout:
                        # Timeout exceeded
                        logger.warning("Timeout releasing the file lock %s.", self.lockFile)
                        break

                    time.sleep(self.delay)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, _type, _value, _traceback):
        self.release()

    def __del__(self):
        self.release()


class SecureOpen(object):
    """ Implementation of cross platform secure file writer logic. Use this
    class for write file operations only. The class is responsible to securely
    persist the file content into a file. In case we are running on Windows we
    may fail because the file could be opened by another process. If this is
    the case, then we have to:
        1) move preliminary known file path to temporary location
        2) delete preliminary known file path
        3) Write the file content to preliminary known file path.
    """
    def __init__(self, filePath, openFileFunction=open, strict=False,
                 *openFileArgs, **openFileKwArgs):
        """ Creates secure file handle.

        @param filePath: File wanted to be opened
        @type filePath: str

        @param openFileFunction: Function which will be used to open the file.
            Default is os.open
        @param openFileFunction: function

        @param strict: Specifies the behavior if file content cannot be
            persisted.
                False(default) - Warn and ignore the exceptions
                True - Throw exception because file content cannot be persisted
        """
        self.filePath = filePath
        self.newFilePath = "%s.new" % (filePath)
        self.oldFilePath = "%s.old" % (filePath)
        self.newFileDescriptior = None
        self.strict = strict
        self.openFileFunnction = openFileFunction
        self.openFileArgs = openFileArgs
        self.openFileKwArgs = openFileKwArgs

    def open(self):
        """Opens the file. Actually it will open self.newFile and will write
        the content there. We do that to decrease the chance two processes to
        use the same file at the same time.
        """
        if self.newFileDescriptior is not None:
            error = 'File %s is already opened' % self.newFilePath
            logger.error(error)
            raise ValueError(error)

        self.newFileDescriptior = self.openFileFunnction(self.newFilePath,
                                                         *self.openFileArgs,
                                                         **self.openFileKwArgs)
        return self.newFileDescriptior

    @staticmethod
    def moveFile(srcFile, dstFile):
        '''Moves the source file to destination file. If destination file
        exists then the file will be overwritten.

        @param srcFile: Path to the source file which has to be renamed
        @type srcFile: str

        @param dstFile: Destination file path
        @type dstFile: str

        @raise IOError: If move operation failed to be performed.
        '''
        import platform
        if platform.system().lower() == 'windows':
            # os.rename fails on Windows if the destination file exists. In
            # order to not be required to first remove the file and then use
            # os.rename, we go on lower(MoveFileExW(MOVEFILE_REPLACE_EXISTING))
            # level and use WindowsAPI to actually rename the file with a single
            # OS operation and replace the destination file in case it exists
            import ctypes
            _MoveFileEx = ctypes.windll.kernel32.MoveFileExW
            _GetLastError = ctypes.windll.kernel32.GetLastError

            if not isinstance(srcFile, unicode):
                srcFile = unicode(srcFile, sys.getfilesystemencoding())
            if not isinstance(dstFile, unicode):
                dstFile = unicode(dstFile, sys.getfilesystemencoding())

            _MOVEFILE_REPLACE_EXISTING = 0x1
            _MOVEFILE_WRITE_THROUGH = 0x8
            result = _MoveFileEx(srcFile, dstFile,
                                 _MOVEFILE_REPLACE_EXISTING | _MOVEFILE_WRITE_THROUGH)
            if not result:
                eno = _GetLastError()
                raise IOError('Cannot rename file %s to %s. Errorno %s' %
                              (srcFile, dstFile, eno))
        else:
            os.rename(srcFile, dstFile)

    @staticmethod
    def renameFile(srcFile, dstFile, helperFile):
        '''Tries to rename the source file to destination file. If the rename
        operation failed(perhaps because the destination file is currently in
        use), then try to:
        1/ Rename destination file to helper file in order to release the
          destination file
        2/ Retry to rename the source file to destination file.

        @param srcFile: Path to the source file which has to be renamed
        @type srcFile: str

        @param dstFile: Destination file path
        @type dstFile: str

        @param helperFile: File used for intermediate rename transaction
        @type helperFile: str

        @raise IOError: If rename operation failed to be performed.
        '''
        try:
            SecureOpen.moveFile(srcFile, dstFile)
        except IOError:
            try:
                SecureOpen.moveFile(dstFile, helperFile)
            except IOError as e:
                # This is fine, perhaps the destination file is already gone
                logger.info("%s", e)
            SecureOpen.moveFile(srcFile, dstFile)

    def close(self):
        """ Releases the self.newFileDescriptor and move the file content to
        preliminary set file location.
        """
        if self.newFileDescriptior is None:
            return

        self.newFileDescriptior.close()
        self.newFileDescriptior = None

        # Rename the temporary file path to the wanted destination path.
        try:
            SecureOpen.renameFile(self.newFilePath, self.filePath,
                                  self.oldFilePath)
        except Exception as e:  # pylint: disable=W0703
            logger.exception('Failed to create a file %s. Cause: %s', self.filePath, str(e))
            if self.strict:
                raise

    def __getattr__(self, name):
        # Forward the rest of the calls to newFileDescriptor
        return getattr(self.newFileDescriptior, name)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, _type, _value, _traceback):
        self.close()

    def __del__(self):
        self.close()
