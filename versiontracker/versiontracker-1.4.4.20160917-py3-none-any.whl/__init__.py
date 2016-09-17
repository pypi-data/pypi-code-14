"""Get version information of software products.

See :ref:`library-usage`.
"""

from importlib import import_module
import json
from logging import getLogger
from multiprocessing import cpu_count
from os import path
from queue import Empty, Queue
import re
from threading import Thread

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from versiontracker.baseseekers import _DATE_TRASH_RE, parse_date

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

_DATA = {}
_INPUT_QUEUE = Queue()
_LOGGER = getLogger(__name__)
_NUM_WORKER_THREADS = cpu_count()
_OUTPUT_QUEUE = Queue()
_SEEKER_CLASSES = {}
# Format patterns that are used by two or more entries:
_FORMAT_PATTERNS = {
    # Most software
    'n.n': r'\d+(?:\.\d+)+',
    # c-ares, luafilesystem
    'n_n': r'(\d+)(?:_(\d+))?(?:_(\d+))?(?:_(\d+))?',
    # higan, knightsgame
    'n': r'\d+',
    # libcanberra, moodle
    'd mmm y': r'\d+\s+\w{3}\s+\d{4}',
}


def _load_data():
    global _DATA
    if not _DATA:
        file_path = path.join(path.dirname(__file__), "data.json")
        with open(file_path, "r") as fp:
            _DATA = json.load(fp)
    return _DATA


def _seeker_class(name):
    global _SEEKER_CLASSES
    if name not in _SEEKER_CLASSES:
        module = import_module("versiontracker.seekers.{}".format(name))
        _SEEKER_CLASSES[name] = module.Seeker
    return _SEEKER_CLASSES[name]


def _worker():
    while True:
        software_id = _INPUT_QUEUE.get()
        try:
            _OUTPUT_QUEUE.put(version_info(software_id))
        except:
            _LOGGER.exception("Exception raised for '%s'.", software_id)
        _INPUT_QUEUE.task_done()


def supported_software():
    """Returns a list of supported software IDs that you can pass to
    :meth:`version_info()` or :meth:`iter_version_info()`."""
    return sorted(_load_data().keys())


def version_info(software_id):
    """Given a :meth:`supported software ID <supported_software>`, it returns a
    dictionary with version information about it.

    The returned dictionary contains the following keys:

    - `id` is the input software ID.

    - `version` is the latest stable version of the specified software.

    - `date` is the date when the specified version was released.

    - `url` is a URL where you can manually confirm the `version` and
      `date` values.

    To get version information about several software products, see
    :meth:`iter_version_info()`.
    """
    tracking_data = _load_data()[software_id]
    invalid_keys = [key for key in tracking_data
                    if key not in ('seeker', 'formatter')]
    if invalid_keys:
        raise ValueError(
            "Software ID '{}' defines the following invalid keys: {}.".format(
                software_id, ", ".join(invalid_keys)))
    seeker_class = _seeker_class(tracking_data["seeker"]["name"])
    tracking_data["seeker"]["id"] = software_id
    seeker = seeker_class(tracking_data['seeker'])
    data = seeker.data()
    if 'formatter' in tracking_data:
        formatter = tracking_data['formatter']
        patterns = {}
        if isinstance(formatter, str):
            patterns['version'] = formatter
        else:
            patterns['version'], patterns['date'] = formatter
        for field in list(patterns.keys()):
            if patterns[field] in _FORMAT_PATTERNS:
                patterns[field] = \
                    _FORMAT_PATTERNS[patterns[field]]
        if 'date' in patterns:
            match = re.search(patterns['date'], data['date'])
            if not match:
                raise ValueError(
                    "Pattern '{}' does not match date string '{}'".format(
                        patterns['date'], data['date']))
            groups = match.groups()
            groupdict = match.groupdict()
            if groupdict:
                data['date'] = "{y}-{m}-{d}".format(**groupdict)
            elif groups:
                data['date'] = groups[0]
            else:
                data['date'] = match.group(0)
        data['date'] = parse_date(data['date'])
        if patterns['version'] == 'date':
            data['version'] = data['date'].strftime("%Y%m%d")
        else:
            match = re.search(patterns['version'], data['version'])
            if not match:
                raise ValueError(
                    "Pattern '{}' does not match version string '{}'".format(
                        patterns['version'], data['version']))
            groups = match.groups()
            if groups:
                data['version'] = ".".join(tuple(group for group in groups
                                                 if group is not None))
            else:
                data['version'] = match.group(0)
    else:
        data['date'] = parse_date(data['date'])
    return data


def iter_version_info(software_ids=()):
    """Given an iterable containing :meth:`supported software IDs
    <supported_software>`, it yields dictionaries with version information
    about them.

    The format of the yielded dictionary is the same as the format of the
    output dictionary of :meth:`version_info()`.

    .. note:: Yield order may not match input order.
    """
    for i in range(_NUM_WORKER_THREADS):
        thread = Thread(target=_worker)
        thread.daemon = True
        thread.start()
    for software_id in software_ids:
        _INPUT_QUEUE.put(software_id)
        try:
            yield _OUTPUT_QUEUE.get(False)
        except Empty:
            pass
    while not _INPUT_QUEUE.empty():
        try:
            yield _OUTPUT_QUEUE.get(True, timeout=1)
        except Empty:
            pass
    _INPUT_QUEUE.join()
    while not _OUTPUT_QUEUE.empty():
        yield _OUTPUT_QUEUE.get()
