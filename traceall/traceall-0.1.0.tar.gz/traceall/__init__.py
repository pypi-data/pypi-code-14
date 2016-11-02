__title__ = 'traceall'
__copyright__ = 'Copyright (c) 2016 Shady Rafehi'
__author__ = 'Shady Rafehi'
__license__ = 'MIT'
__version__ = '0.1.0'

import sys
import json
from collections import defaultdict


class WriteWrap(object):

    def __init__(self, f):
        self.f = f
        self._last_write = None

    @property
    def last_write(self):
        s = self._last_write
        self._last_write = None
        return s

    def __getattr__(self, item):
        return getattr(self.f, item)

    def write(self, contents, *args, **kwargs):
        if self._last_write:
            self._last_write += contents
        else:
            self._last_write = contents
        self.f.write(contents, *args, **kwargs)


class trace(object):

    def __enter__(self):
        self.write_wrap = sys.stdout = WriteWrap(sys.stdout)
        sys.settrace(self.trace)
        return self

    def __init__(self, output, skip_files=None, skip_names=None):
        self.write_wrap = None
        self.index_local = 0
        self.index_name = 0
        self.output = output
        self.entries = []
        self.name_index = defaultdict(self.next_index_name)
        self.local_index = defaultdict(self.next_index_local)
        self.files = {}
        self.skip_files = skip_files or []
        self.skip_names = skip_names or []

    def next_index_name(self):
        self.index_name += 1
        return self.index_name - 1

    def next_index_local(self):
        self.index_local += 1
        return self.index_local - 1

    def __exit__(self, *_):
        try:
            sys.settrace(None)
            last_write = self.write_wrap.last_write
            if last_write and self.entries:
                self.entries.append(dict(self.entries[-1]))
                self.entries[-1]['out'] = last_write
            sys.stdout = self.write_wrap.f

            with open(self.output, 'w') as f:
                json.dump({
                    'index': {
                        'name': [x[0] for x in sorted(self.name_index.iteritems(), key=lambda x: x[1])],
                        'locals': [list(x[0]) for x in sorted(self.local_index.iteritems(), key=lambda x: x[1])],
                    },
                    'files': self.files,
                    'entries': self.entries
                }, f, default=str, indent=2, ensure_ascii=False)
        except:
            import traceback
            print traceback.format_exc()
        return

    def trace(self, frame, event, extra):
        filename = frame.f_code.co_filename
        name = frame.f_code.co_name
        if filename == __file__:
            return
        if not any(x in filename for x in self.skip_files) and not any(x == name for x in self.skip_names):
            new_locals = []
            for key, item in frame.f_locals.iteritems():
                if key.startswith('__') and key.endswith('__'):
                    continue

                type_ = type(item).__name__
                if type_ == 'module':
                    continue

                key_index = self.name_index[key]
                type_index = self.name_index[type_]

                try:
                    item_index = self.name_index[str(item)]
                except:
                    item_index = self.name_index['<unknown>']

                new_locals.append(self.local_index[(key_index, type_index, item_index)])

            if self.name_index[filename] not in self.files:
                try:
                    self.files[self.name_index[filename]] = open(filename).read()
                except:
                    return

            if event == 'return' and extra is not None:
                try:
                    return_index = self.name_index[str(extra)]
                except:
                    return_index = self.name_index['<unknown>']
            else:
                return_index = None

            entry = {
                'cxt': {
                    'fl': self.name_index[filename],
                    'ln': frame.f_lineno,
                    'fn': self.name_index[name],
                    'ev': self.name_index[event],
                    'rt': return_index
                },
                'loc': new_locals,
                'out': self.write_wrap.last_write
            }

            if entry['out'] is None:
                del entry['out']

            if not entry['loc']:
                del entry['loc']

            if entry['cxt']['rt'] is None:
                del entry['cxt']['rt']

            self.entries.append(entry)
        return self.trace
