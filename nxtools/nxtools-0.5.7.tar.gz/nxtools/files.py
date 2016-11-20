# The MIT License (MIT)
#
# Copyright (c) 2015 imm studios, z.s.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import tempfile
import stat
import uuid
import time

from .logging import *
from .common import PYTHON_VERSION

__all__ = ["get_files", "get_temp", "get_base_name", "file_to_title", "get_file_siblings", "WatchFolder"]


def get_files(base_path, **kwargs):
    #TODO: Use os.scandir if python version >= 3.5
    recursive = kwargs.get("recursive", False)
    hidden = kwargs.get("hidden", False)
    relative_path = kwargs.get("relative_path", False)
    case_sensitive_exts = kwargs.get("case_sensitive_exts", False)
    if case_sensitive_exts:
        exts = kwargs.get("exts", [])
    else:
        exts = [ext.lower() for ext in kwargs.get("exts", [])]
    strip_path = kwargs.get("strip_path", base_path)
    if os.path.exists(base_path):
        for file_name in os.listdir(base_path):
            if not hidden and file_name.startswith("."):
                continue
            file_path = os.path.join(base_path, file_name)
            try:
                is_reg = stat.S_ISREG(os.stat(file_path)[stat.ST_MODE])
                is_dir = stat.S_ISDIR(os.stat(file_path)[stat.ST_MODE])
            except Exception:
                continue
            if is_reg:
                ext = os.path.splitext(file_name)[1].lstrip(".")
                if not case_sensitive_exts:
                    ext = ext.lower()
                if exts and ext not in exts:
                    continue
                if relative_path:
                    yield file_path.replace(strip_path, "", 1).lstrip(os.path.sep)
                else:
                    yield file_path
            elif is_dir and recursive:
                for file_path in get_files(
                            file_path,
                            recursive=recursive,
                            hidden=hidden,
                            case_sensitive_exts=case_sensitive_exts,
                            exts=exts,
                            relative_path=relative_path,
                            strip_path=strip_path
                        ):
                    yield file_path


def get_temp(extension=False, root=False):
    if not root:
        root = tempfile.gettempdir()
    basename = uuid.uuid1()
    filename = os.path.join(root, str(basename))
    if extension:
        filename = filename + "." + extension
    return filename


def get_base_name(fname):
    return os.path.splitext(os.path.basename(fname))[0]


def file_to_title(fname):
    base = get_base_name(fname)
    base = base.replace("_"," ").replace("-"," - ").strip()
    elms = []
    capd = False
    for i, elm in enumerate(base.split(" ")):
        if not elm: continue
        if not capd and not (elm.isdigit() or elm.upper()==elm):
            elm = elm.capitalize()
            capd = True
        elms.append(elm)
    return " ".join(elms)


def get_file_siblings(path, exts=[]):
    #TODO: Rewrite this
    root = os.path.splitext(path)[0]
    for f in exts:
        tstf = root + "." + f
        if os.path.exists(tstf):
            yield tstf


class WatchFolder():
    def __init__(self, input_dir, **kwargs):
        self.input_dir = input_dir
        self.settings = self.defaults
        self.settings.update(**kwargs)
        self.file_sizes = {}
        self.ignore_files = set()

    @property
    def defaults(self):
        settings = {
            "iter_delay" : 5,
            "recursive" : True,
            "valid_exts" : []
            }
        return settings

    def start(self):
        while True:
            try:
                self.main()
                self.clean_filesizes()
                time.sleep(self.settings["iter_delay"])
            except KeyboardInterrupt:
                print ()
                logging.warning("User interrupt")
                break

    def clean_filesizes(self):
        keys = self.file_sizes.keys()
        for file_path in keys:
            if not os.path.exists(file_path):
                del(self.file_sizes[file_path])

    def main(self):
        for input_path in get_files(self.input_dir, recursive=self.settings["recursive"], exts=self.settings["valid_exts"]):
            if PYTHON_VERSION < 3:
                input_path = input_path.encode("utf8")

            if input_path in self.ignore_files:
                continue
            try:
                f = open(input_path, "rb")
            except:
                logging.debug("File creation in progress. {}".format(os.path.basename(input_path)))
                continue

            f.seek(0, 2)
            file_size = f.tell()
            f.close()

            if file_size == 0:
                continue

            if not (input_path in self.file_sizes.keys() and self.file_sizes[input_path] == file_size):
                self.file_sizes[input_path] = file_size
                logging.debug("New file {} detected (or file has been changed)".format(input_path))
                continue
            self.process(input_path)

    def process(self, input_path):
        pass

