#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright 2016 Curtis Thompson
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
A simple way to share a file over HTTP on the local network without setting up a server.

Usage:
    fling [options] FILE_OR_DIR...

Options:
    --address=<address>         Server address [default: 0.0.0.0]
    --port=<port>               Server port [default: 9999]
    --hash=<strategy>           How the hash is created [default: random]
                                    random: random md5 hash
                                    file:   the file's md5 hash
                                    easy:   human readable low security hash

"""

__version__ = "0.1.1"

import hashlib
import logging
import os
import signal
import socket
import sys

from docopt import docopt
from progress.bar import IncrementalBar

WORDS = ['adam', 'bob', 'carol', 'david', 'edward', 'frank', 'george', 'harry', 'india', 'juliet', 'karen', 'lincoln',
        'martin', 'nora', 'olivia', 'peter', 'queen', 'roger', 'sam', 'tom', 'uncle', 'victor', 'william', 'xerxes',
        'young', 'zebra']

import tornado.gen
import tornado.httputil
import tornado.ioloop
import tornado.iostream
import tornado.web


def format_size(byte_size):
    if byte_size > 1024 * 1024:
        return '%.1fMB' % (byte_size / 1024.0 / 1024)
    elif byte_size > 10 * 1024:
        return '%ikB' % (byte_size / 1024)
    elif byte_size > 1024:
        return '%.1fkB' % (byte_size / 1024.0)
    else:
        return '%ibytes' % byte_size


class ProgressBar(IncrementalBar):

    file = sys.stdout
    message = "%(percent)d%%"
    suffix = "%(done)s %(speed)s %(pretty_eta)s"

    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)

    @property
    def done(self):
        return format_size(self.index)

    @property
    def speed(self):
        # Avoid zero division errors...
        if self.avg == 0.0:
            return "..."
        return format_size(1 / self.avg) + "/s"

    @property
    def pretty_eta(self):
        if self.eta:
            return "eta %s" % self.eta_td
        return ""


def get_server_host():
    return socket.gethostbyname(socket.gethostname())


def file_hash(file_path, algorithm='md5'):
    if algorithm not in hashlib.algorithms:
        raise ValueError("Invalid hashing algorithm {}".format(algorithm))
    hash = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hash.update(chunk)
    return hash.hexdigest()


def random_hash(algorithm='md5'):
    if algorithm not in hashlib.algorithms:
        raise ValueError("Invalid hashing algorithm {}".format(algorithm))
    hash = hashlib.new(algorithm)
    hash.update(os.urandom(128))
    return hash.hexdigest()


def easy_hash(number_of_words=3):
    import random
    return "-".join(random.choice(WORDS) for _ in range(number_of_words))


def collect_files_and_sizes(file_or_dir=None):
    """Create the follwing structure of files and file sizes:
    (<total_size_in_bytes>, (<file_path>, <file_size_in_bytes>), ...))"""
    total_size = 0
    file_list = []
    for filepath in file_or_dir:
        if not os.path.exists(filepath):
            print "File '{}' does not exit".format(filepath)
        if os.path.isdir(filepath):
            for root, dirs, files in os.walk(filepath):
                for fname in files:
                    path = os.path.join(root, fname)
                    size = os.path.getsize(path)
                    file_list.append((path, size))
                    total_size += size
        else:
            size = os.path.getsize(filepath)
            file_list.append((filepath, size))
            total_size += size
    return total_size, file_list


def create_zip_archive(collected_files, archive_path=None):
    """Create a ZIP archive from collected_files that has the following structure:
    (<total_size_in_bytes>, (<file_path>, <file_size_in_bytes>), ...))"""
    from zipfile import ZipFile
    if not archive_path:
        archive_path = '/tmp/{}.zip'.format(random_hash())
    total_size, file_list = collected_files
    zipbar = ProgressBar(max=total_size)
    with ZipFile(archive_path, 'w') as zip_file:
        for path, size in file_list:
            if size:
                zipbar.next(size)
            # Write the path as a *sane* structure in the archive.
            zip_file.write(path, os.path.relpath(path).split('../')[-1])
    zipbar.finish()
    return archive_path


def copy_to_clipboard(str_to_copy):
    copy_cmd = '/usr/bin/pbcopy'
    if os.path.isfile(copy_cmd) and os.access(copy_cmd, os.X_OK):
        os.system('echo "{}" | {}'.format(str_to_copy, copy_cmd))
        print "URL copied to clipboard..."


class Cleanup(object):
    """Track and execute operations that need to perform cleanup."""

    def __init__(self):
        self.cmds = []

    def add_cmd(self, cmd, *args, **kwargs):
        self.cmds.append((cmd, args, kwargs))

    def run(self):
        for cmd, args, kwargs in self.cmds:
            if callable(cmd):
                try:
                    cmd(*args, **kwargs)
                except Exception:
                    logging.exception('Unable to run {}({},{})'.format(cmd, args, kwargs))
            else:
                logging.error("Unable to run {}".format(cmd))
        self.cmds = []


def on_shutdown(cleanup=None):
    """Callback to gracefully shutdown server"""
    if cleanup:
        cleanup.run()
    tornado.ioloop.IOLoop.instance().stop()


class SlingFileHandler(tornado.web.StaticFileHandler):

    def initialize(self, root, hash, default_filename=None, file_path=None):
        super(SlingFileHandler, self).initialize(root, default_filename=default_filename)
        self.hash=hash
        self.file_path=file_path

    @classmethod
    def _get_cached_version(cls, abs_path):
        return None

    @tornado.gen.coroutine
    def get(self, hash, include_body=True):
        if hash == self.hash:
            print "Client connected from: {}...".format(self.request.remote_ip)
            yield super(SlingFileHandler, self).get(self.file_path, include_body=include_body)
        else:
            self.set_status(304)
        tornado.ioloop.IOLoop.current().add_callback(lambda: tornado.ioloop.IOLoop.current().stop())
        return

    @classmethod
    def get_content(cls, abspath, start=None, end=None):
        """Retrieve the content of the requested resource which is located
        at the given absolute path.

        This class method may be overridden by subclasses.  Note that its
        signature is different from other overridable class methods
        (no ``settings`` argument); this is deliberate to ensure that
        ``abspath`` is able to stand on its own as a cache key.

        This method should either return a byte string or an iterator
        of byte strings.  The latter is preferred for large files
        as it helps reduce memory fragmentation.

        .. versionadded:: 3.1
        """
        download_bar = ProgressBar(max=os.stat(abspath).st_size)
        with open(abspath, "rb") as file:
            if start is not None:
                file.seek(start)
            if end is not None:
                remaining = end - (start or 0)
            else:
                remaining = None
            while True:
                chunk_size = 64 * 1024 * 4
                if remaining is not None and remaining < chunk_size:
                    chunk_size = remaining
                chunk = file.read(chunk_size)
                if chunk:
                    if remaining is not None:
                        remaining -= len(chunk)
                    download_bar.next(chunk_size)
                    yield chunk
                else:
                    if remaining is not None:
                        assert remaining == 0
                    download_bar.finish()
                    return


def make_fileshare_app(file_directory, file_hash, file_path):
    return tornado.web.Application([
        (r"/([\w|-]*)/(.*)|.*", SlingFileHandler, dict(root=file_directory, hash=file_hash, file_path=file_path))
    ])


def main():
    arguments = docopt(__doc__, version='Fling {} '.format( __version__))
    cleanup = Cleanup()

    upload_file = None
    zip_files = []

    # Just one normal file
    if len(arguments['FILE_OR_DIR']) == 1 and not os.path.isdir(arguments['FILE_OR_DIR'][0]):
        upload_file = arguments['FILE_OR_DIR'][0]
        upload_name = os.path.basename(upload_file)
    else: # Create a zip archive
        zip_files = arguments['FILE_OR_DIR']
        upload_name = easy_hash()

    upload_hash = random_hash()
    if arguments['--hash']:
        if arguments['--hash'] == 'file':
            if not zip_files:
                upload_hash = file_hash(upload_file)
        elif arguments['--hash'] == 'easy':
            upload_hash = easy_hash()

    if zip_files:
        print "Zipping..."
        archive_path = create_zip_archive(collect_files_and_sizes(zip_files))
        file_directory = os.path.dirname(archive_path)
        if len(zip_files) == 1:
            file_name = os.path.splitext(
                os.path.basename(
                    os.path.abspath(
                        zip_files[0])))[0] + '.zip'
        else:
            file_name = upload_name + '.zip'
        if arguments['--hash'] == 'file':
            upload_hash = file_hash(archive_path)
        file_path = archive_path
    else:
        file_path = os.path.abspath(upload_file)
        file_directory = upload_file
        file_name = upload_name

    app = make_fileshare_app(file_directory, upload_hash, file_path)

    port = arguments['--port']
    address=arguments['--address']
    app.listen(port, address)

    url = 'http://{}:{}/{}/{}'.format(get_server_host(), port, upload_hash, file_name)

    print "URL: {} ".format(url)
    copy_to_clipboard(url)

    signal.signal(signal.SIGINT,
            lambda sig, frame: tornado.ioloop.IOLoop.current().add_callback_from_signal(on_shutdown, cleanup))

    print "Starting file server..."
    tornado.ioloop.IOLoop.current().start()

    print "Server terminating...\n"
    cleanup.run()

if __name__ == "__main__":
    main()
