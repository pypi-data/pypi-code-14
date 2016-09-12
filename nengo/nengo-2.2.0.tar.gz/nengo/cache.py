"""Caching capabilities for a faster build process."""

import errno
import hashlib
import inspect
import logging
import os
import shutil
import struct
from uuid import uuid1
import warnings

import numpy as np

from nengo.exceptions import FingerprintError, TimeoutError
from nengo.neurons import (AdaptiveLIF, AdaptiveLIFRate, Direct, Izhikevich,
                           LIF, LIFRate, RectifiedLinear, Sigmoid)
from nengo.rc import rc
from nengo.solvers import (Lstsq, LstsqL1, Nnls, NnlsL2,
                           NnlsL2nz, LstsqNoise, LstsqMultNoise, LstsqL2,
                           LstsqL2nz, LstsqDrop)
from nengo.utils import nco
from nengo.utils.cache import byte_align, bytes2human, human2bytes
from nengo.utils.compat import (
    int_types, is_string, pickle, replace, PY2, string_types)
from nengo.utils.least_squares_solvers import (
    Cholesky, ConjgradScipy, LSMRScipy, Conjgrad,
    BlockConjgrad, SVD, RandomizedSVD)
from nengo.utils.lock import FileLock

logger = logging.getLogger(__name__)


def get_fragment_size(path):
    try:
        return os.statvfs(path).f_frsize
    except AttributeError:  # no statvfs on Windows
        return 4096  # correct value in 99% of cases


def safe_stat(path):
    """Does os.stat, but fails gracefully in case of an OSError."""
    try:
        return os.stat(path)
    except OSError as err:
        logger.warning("OSError during safe_stat: %s", err)
    return None


def safe_remove(path):
    """Does os.remove, but fails gracefully in case of an OSError."""
    try:
        os.remove(path)
    except OSError as err:
        logger.warning("OSError during safe_remove: %s", err)


def safe_makedirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as err:
            logger.warning("OSError during safe_makedirs: %s", err)


def check_dtype(ndarray):
    return ndarray.dtype.isbuiltin == 1 and not ndarray.dtype.hasobject


def check_seq(tpl):
    return all(Fingerprint.supports(x) for x in tpl)


def check_attrs(obj):
    attrs = [getattr(obj, x) for x in dir(obj) if not x.startswith('_')]
    return all(Fingerprint.supports(x) for x in attrs if not callable(x))


class Fingerprint(object):
    """Fingerprint of an object instance.

    A finger print is equal for two instances if and only if they are of the
    same type and have the same attributes.

    The fingerprint will be used as identification for caching.

    Parameters
    ----------
    obj : object
        Object to fingerprint.

    Attributes
    ----------
    fingerprint : hash
        A unique fingerprint for the object instance.

    Notes
    -----
    Not all objects can be fingerprinted. In particular, custom classes are
    tricky to fingerprint as their implementation can change without changing
    its fingerprint, as the type and attributes may be the same.

    In order to ensure that only safe object are fingerprinted, this class
    maintains class attribute ``WHITELIST`` that contains all types that can
    be safely fingerprinted.

    If you want your custom class to be fingerprinted, call the
    `.whitelist` class method and pass in your class.
    """

    __slots__ = ('fingerprint',)

    SOLVERS = (
        Lstsq,
        LstsqDrop,
        LstsqL1,
        LstsqL2,
        LstsqL2nz,
        LstsqNoise,
        LstsqMultNoise,
        Nnls,
        NnlsL2,
        NnlsL2nz,
    )
    LSTSQ_METHODS = (
        BlockConjgrad,
        Cholesky,
        Conjgrad,
        ConjgradScipy,
        LSMRScipy,
        RandomizedSVD,
        SVD,
    )
    NEURON_TYPES = (
        AdaptiveLIF,
        AdaptiveLIFRate,
        Direct,
        Izhikevich,
        LIF,
        LIFRate,
        RectifiedLinear,
        Sigmoid
    )

    WHITELIST = set(
        (bool, float, complex, bytes, list, tuple, np.ndarray) +
        int_types + string_types +
        SOLVERS + LSTSQ_METHODS + NEURON_TYPES
    )
    CHECKS = dict([
        (np.ndarray, check_dtype),
        (tuple, check_seq),
        (list, check_seq)
    ] + [
        (x, check_attrs) for x in SOLVERS + LSTSQ_METHODS + NEURON_TYPES
    ])

    def __init__(self, obj):
        if not self.supports(obj):
            raise FingerprintError("Object of type %r cannot be fingerprinted."
                                   % type(obj).__name__)

        self.fingerprint = hashlib.sha1()
        try:
            self.fingerprint.update(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL))
        except Exception as err:
            raise FingerprintError(str(err))

    def __str__(self):
        return self.fingerprint.hexdigest()

    @classmethod
    def supports(cls, obj):
        typ = type(obj)
        in_whitelist = typ in cls.WHITELIST
        succeeded_check = typ not in cls.CHECKS or cls.CHECKS[typ](obj)
        return in_whitelist and succeeded_check

    @classmethod
    def whitelist(cls, typ, fn=None):
        cls.WHITELIST.add(typ)
        if fn is not None:
            cls.CHECKS[typ] = fn


class CacheIndex(object):
    def __init__(self, filename):
        self.filename = filename
        self._lock = FileLock(self.filename + '.lock')
        self._index = None
        self._updates = {}
        self._deletes = set()
        self._removed_files = set()

    def __getitem__(self, key):
        if key in self._updates:
            return self._updates[key]
        else:
            return self._index[key]

    def __setitem__(self, key, value):
        self._updates[key] = value

    def __delitem__(self, key):
        self._deletes.add(key)

    def remove_file_entry(self, filename):
        self._removed_files.add(filename)

    def __enter__(self):
        with self._lock:
            self._index = self._load_index()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sync()

    def _load_index(self):
        assert self._lock.acquired
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except IOError as err:
            if err.errno == errno.ENOENT:
                return {}
            else:
                raise

    def sync(self):
        try:
            with self._lock:
                self._index = self._load_index()
                self._index.update(self._updates)

                for key in self._deletes:
                    del self._index[key]

                with open(self.filename + '.part', 'wb') as f:
                    pickle.dump(
                        {k: v for k, v in self._index.items()
                         if v[0] not in self._removed_files},
                        f, pickle.HIGHEST_PROTOCOL)
                replace(self.filename + '.part', self.filename)
        except TimeoutError:
            warnings.warn(
                "Decoder cache index could not acquire lock. "
                "Cache index was not synced.")

        self._updates.clear()
        self._deletes.clear()


class DecoderCache(object):
    """Cache for decoders.

    Hashes the arguments to the decoder solver and stores the result in a file
    which will be reused in later calls with the same arguments.

    Be aware that decoders should not use any global state, but only values
    passed and attributes of the object instance. Otherwise the wrong solver
    results might get loaded from the cache.

    Parameters
    ----------
    readonly : bool
        Indicates that already existing items in the cache will be used, but no
        new items will be written to the disk in case of a cache miss.
    cache_dir : str or None
        Path to the directory in which the cache will be stored. It will be
        created if it does not exists. Will use the value returned by
        :func:`get_default_dir`, if `None`.
    """

    _CACHE_EXT = '.nco'
    _INDEX = 'index'
    _LEGACY = 'legacy.txt'
    _LEGACY_VERSION = 1
    _PICKLE_PROTOCOL = pickle.HIGHEST_PROTOCOL

    def __init__(self, readonly=False, cache_dir=None):
        self.readonly = readonly
        if cache_dir is None:
            cache_dir = self.get_default_dir()
        self.cache_dir = cache_dir
        safe_makedirs(self.cache_dir)
        self._fragment_size = get_fragment_size(self.cache_dir)
        self._index = None
        self._fd = None

    def __enter__(self):
        try:
            self._remove_legacy_files()
            index_path = os.path.join(self.cache_dir, self._INDEX)
            self._index = CacheIndex(index_path)
            try:
                self._index.__enter__()
            except (EOFError, IOError, OSError):
                # Index corrupted, clear cache because we can't recover
                # information necessary to access cache data.
                self.invalidate()
                os.remove(index_path)
                self._index.__enter__()
        except TimeoutError:
            warnings.warn(
                "Decoder cache could not acquire lock and was deactivated.")
            self.readonly = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._close_fd()
        if self._index is not None:
            rval = self._index.__exit__(exc_type, exc_value, traceback)
            self._index = None
            return rval

    @staticmethod
    def get_default_dir():
        """Returns the default location of the cache.

        Returns
        -------
        str
        """
        return rc.get('decoder_cache', 'path')

    def _close_fd(self):
        if self._fd is not None:
            self._fd.close()
            self._fd = None

    def _get_fd(self):
        if self._fd is None:
            self._fd = open(self._key2path(str(uuid1())), 'wb')
        return self._fd

    def _check_legacy_file(self):
        """Checks if the legacy file is up to date."""
        legacy_file = os.path.join(self.cache_dir, self._LEGACY)
        if os.path.exists(legacy_file):
            with open(legacy_file, 'r') as lf:
                text = lf.read()
            try:
                lv, pp = tuple(int(x.strip()) for x in text.split('.'))
            except ValueError:
                # Will be raised with old legacy.txt format
                lv = pp = -1
        else:
            lv = pp = -1
        return lv == self._LEGACY_VERSION and pp == self._PICKLE_PROTOCOL

    def _remove_legacy_files(self):
        """Remove files from now invalid locations in the cache.

        This will not remove any files if a legacy file exists and is
        up to date. Once legacy files are removed, a legacy file will be
        written to avoid a costly ``os.listdir`` after calling this.
        """
        lock_filename = 'legacy.lock'
        with FileLock(os.path.join(self.cache_dir, lock_filename)):
            if self._check_legacy_file():
                return

            for f in os.listdir(self.cache_dir):
                if f == lock_filename:
                    continue
                path = os.path.join(self.cache_dir, f)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

            self._write_legacy_file()

    def _write_legacy_file(self):
        """Writes a legacy file, indicating that legacy files do not exist."""
        legacy_file = os.path.join(self.cache_dir, self._LEGACY)
        with open(legacy_file, 'w') as lf:
            lf.write("%d.%d\n" % (self._LEGACY_VERSION, self._PICKLE_PROTOCOL))

    def get_files(self):
        """Returns all of the files in the cache.

        Returns
        -------
        list of (str, int) tuples
        """
        files = []
        for subdir in os.listdir(self.cache_dir):
            path = os.path.join(self.cache_dir, subdir)
            if os.path.isdir(path):
                files.extend(os.path.join(path, f) for f in os.listdir(path))
        return files

    def get_size(self):
        """Returns the size of the cache with units as a string.

        Returns
        -------
        str
        """
        return bytes2human(self.get_size_in_bytes())

    def get_size_in_bytes(self):
        """Returns the size of the cache in bytes as an int.

        Returns
        -------
        int
        """
        stats = (safe_stat(f) for f in self.get_files())
        return sum(byte_align(st.st_size, self._fragment_size)
                   for st in stats if st is not None)

    def invalidate(self):
        """Invalidates the cache (i.e. removes all cache files)."""
        self._close_fd()
        for path in self.get_files():
            safe_remove(path)

    def shrink(self, limit=None):  # noqa: C901
        """Reduces the size of the cache to meet a limit.

        Parameters
        ----------
        limit : int, optional
            Maximum size of the cache in bytes.
        """
        if self.readonly:
            logger.info("Tried to shrink a readonly cache.")
            return

        if self._index is None:
            warnings.warn("Cannot shrink outside of a `with cache` block.")
            return

        if limit is None:
            limit = rc.get('decoder_cache', 'size')
        if is_string(limit):
            limit = human2bytes(limit)

        self._close_fd()

        fileinfo = []
        excess = -limit
        for path in self.get_files():
            stat = safe_stat(path)
            if stat is not None:
                aligned_size = byte_align(stat.st_size, self._fragment_size)
                excess += aligned_size
                fileinfo.append((stat.st_atime, aligned_size, path))

        # Remove the least recently accessed first
        fileinfo.sort()

        for _, size, path in fileinfo:
            if excess <= 0:
                break

            excess -= size
            self._index.remove_file_entry(path)
            safe_remove(path)

        self._index.sync()

    def wrap_solver(self, solver_fn):  # noqa: C901
        """Takes a decoder solver and wraps it to use caching.

        Parameters
        ----------
        solver : func
            Decoder solver to wrap for caching.

        Returns
        -------
        func
            Wrapped decoder solver.
        """

        def cached_solver(solver, neuron_type, gain, bias, x, targets,
                          rng=None, E=None):
            try:
                args, _, _, defaults = inspect.getargspec(solver)
            except TypeError:
                args, _, _, defaults = inspect.getargspec(solver.__call__)
            args = args[-len(defaults):]
            if rng is None and 'rng' in args:
                rng = defaults[args.index('rng')]
            if E is None and 'E' in args:
                E = defaults[args.index('E')]

            try:
                key = self._get_cache_key(
                    solver, neuron_type, gain, bias, x, targets, rng, E)
            except FingerprintError as e:
                logger.debug("Failed to generate cache key: %s", e)
                return solver_fn(
                    solver, neuron_type, gain, bias, x, targets, rng=rng, E=E)

            try:
                path, start, end = self._index[key]
                if self._fd is not None:
                    self._fd.flush()
                with open(path, 'rb') as f:
                    f.seek(start)
                    solver_info, decoders = nco.read(f)
            except:
                logger.debug("Cache miss [%s].", key)
                if self._index is None:
                    warnings.warn("Cannot use cached solver outside of "
                                  "`with cache` block.")
                decoders, solver_info = solver_fn(
                    solver, neuron_type, gain, bias, x, targets, rng=rng, E=E)
                if not self.readonly and self._index is not None:
                    fd = self._get_fd()
                    start = fd.tell()
                    nco.write(fd, solver_info, decoders)
                    end = fd.tell()
                    self._index[key] = (fd.name, start, end)
            else:
                logger.debug("Cache hit [%s]: Loaded stored decoders.", key)
            return decoders, solver_info

        return cached_solver

    def _get_cache_key(
            self, solver, neuron_type, gain, bias, x, targets, rng, E):
        h = hashlib.sha1()

        if PY2:
            h.update(str(Fingerprint(solver)))
            h.update(str(Fingerprint(neuron_type)))
        else:
            h.update(str(Fingerprint(solver)).encode('utf-8'))
            h.update(str(Fingerprint(neuron_type)).encode('utf-8'))

        h.update(np.ascontiguousarray(gain).data)
        h.update(np.ascontiguousarray(bias).data)
        h.update(np.ascontiguousarray(x).data)
        h.update(np.ascontiguousarray(targets).data)

        # rng format doc:
        # noqa <http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.RandomState.get_state.html#numpy.random.RandomState.get_state>
        state = rng.get_state()
        h.update(state[0].encode())  # string 'MT19937'
        h.update(state[1].data)  # 1-D array of 624 unsigned integer keys
        h.update(struct.pack('q', state[2]))  # integer pos
        h.update(struct.pack('q', state[3]))  # integer has_gauss
        h.update(struct.pack('d', state[4]))  # float cached_gaussian

        if E is not None:
            h.update(np.ascontiguousarray(E).data)
        return h.hexdigest()

    def _key2path(self, key):
        prefix = key[:2]
        suffix = key[2:]
        directory = os.path.join(self.cache_dir, prefix)
        safe_makedirs(directory)
        return os.path.join(directory, suffix + self._CACHE_EXT)


class NoDecoderCache(object):
    """Provides the same interface as :class:`DecoderCache` without caching."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def wrap_solver(self, solver_fn):
        return solver_fn

    def get_size_in_bytes(self):
        return 0

    def get_size(self):
        return '0 B'

    def shrink(self, limit=0):
        pass

    def invalidate(self):
        pass


def get_default_decoder_cache():
    if rc.getboolean('decoder_cache', 'enabled'):
        decoder_cache = DecoderCache(
            rc.getboolean('decoder_cache', 'readonly'))
    else:
        decoder_cache = NoDecoderCache()
    return decoder_cache
