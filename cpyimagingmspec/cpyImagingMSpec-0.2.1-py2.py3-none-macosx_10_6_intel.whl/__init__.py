# -*- encoding: utf-8 -*-
import cffi
import numpy as np
import pandas as pd
import numbers

from .utils import shared_lib, full_filename

ffi = cffi.FFI()
ffi.cdef(open(full_filename("ims.h")).read())
_ims = ffi.dlopen(full_filename(shared_lib("ims_cffi")))

_has_numpy = True
_dtypes = {'f': np.float32, 'd': np.float64}
_full_types = {'f': 'float', 'd': 'double'}

def _as_buffer(array, numtype):
    return np.asarray(array, dtype=_dtypes[numtype])

class _cffi_buffer(object):
    def __init__(self, n, numtype):
        if isinstance(n, numbers.Number):
            self.buf = np.zeros(n, dtype=_dtypes[numtype])
        else:
            self.buf = _as_buffer(n, numtype)

        self.ptr = ffi.cast(_full_types[numtype] + '*',
                            self.buf.__array_interface__['data'][0])

    def python_data(self):
        return self.buf

def _raise_ims_exception():
    raise Exception(ffi.string(_ims.ims_strerror()))

def _raise_ims_exception_if_null(arg):
    if arg == ffi.NULL:
        _raise_ims_exception()

class ImzbReader(object):
    """
    Class for reading .imzb format.

    WARNING: the format is not standardized and might change in the future without any backward compatibility considerations; use it at your own risk!

    .imzb format is optimized for very fast m/z-image queries.

    ImzML files can be converted to it using 'ims convert' tool that
    must be compiled from source: https://github.com/alexandrovteam/ims-cpp
    """
    def __init__(self, filename):
        """
        Open .imzb file for reading
        """
        self._filename = filename
        r = _ims.imzb_reader_new(filename.encode('utf-8'))
        _raise_ims_exception_if_null(r)
        self._reader = ffi.gc(r, _ims.imzb_reader_free)

    @property
    def height(self):
        """
        Image height
        """
        return _ims.imzb_reader_height(self._reader)

    @property
    def width(self):
        """
        Image width
        """
        return _ims.imzb_reader_width(self._reader)

    @property
    def min_mz(self):
        """
        Minimal m/z value
        """
        return _ims.imzb_reader_min_mz(self._reader)

    @property
    def max_mz(self):
        """
        Maximal m/z value
        """
        return _ims.imzb_reader_max_mz(self._reader)

    def get_mz_image(self, mz, ppm):
        """
        Read m/z-image formed from peaks within mz × (1 ± 10 :sup:`-6` × ppm) window.

        Pixels that were not scanned have intensity set to -1.
        """
        data = _cffi_buffer(self.height * self.width, 'f')
        read_func = _ims.imzb_reader_image
        ret = read_func(self._reader, ffi.cast("double", mz), ffi.cast("double", ppm),
                        data.ptr)
        if ret < 0:
            _raise_ims_exception()
        return data.buf.reshape((self.height, self.width))

    def peaks(self, min_mz, max_mz):
        """
        Returns peaks between min_mz and min_mz formatted as a Pandas dataframe
        with columns mz, intensity, x, y, z.
        """
        peaks_ptr = ffi.new("Peak**", ffi.NULL)
        n = _ims.imzb_reader_slice(self._reader,
                                   ffi.cast("double", min_mz), ffi.cast("double", max_mz),
                                   peaks_ptr)
        alignment = ffi.alignof('Peak')
        if alignment == 8:
            dtype = [('x', 'u4'), ('y', 'u4'), ('z', 'u4'), ('_', 'u4'),
                     ('mz', 'f8'), ('intensity', 'f4'), ('__', 'f4')]
        else:
            dtype = [('x', 'u4'), ('y', 'u4'), ('z', 'u4'),
                     ('mz', 'f8'), ('intensity', 'f4')]
        arr = np.frombuffer(ffi.buffer(peaks_ptr[0], n * ffi.sizeof('Peak')), dtype, n)
        df = pd.DataFrame(arr)
        if alignment == 8:
            del df['_'], df['__']
        _ims.free(peaks_ptr[0])
        return df

    def dbscan(self, minPts=None, eps=0.001, min_mz=None, max_mz=None):
        """
        Runs DBSCAN algorithm on the set of all m/z values encountered in the file.
        Meaningful only for centroided data.
        If minPts is not provided, it is set as 2% of the number of spectra.
        The range can be set through min_mz and max_mz parameters.

        Returns m/z bins formatted as a Pandas dataframe with the following columns:
        * left, right - bin boundaries;
        * count - number of peaks in the bin;
        * mean - average m/z;
        * sd - standard deviation of m/z;
        * intensity - total intensity.
        """
        bins_ptr = ffi.new("MzBin**", ffi.NULL)
        if minPts is None:
            minPts = int(self.width * self.height * 0.02)  # FIXME don't assume rectangular
        if (min_mz is None) and (max_mz is None):
            n = _ims.imzb_reader_dbscan(self._reader,
                                        ffi.cast("int", minPts), ffi.cast("double", eps),
                                        bins_ptr)
        elif (min_mz is None) and (max_mz is not None):
            min_mz = self.min_mz
        elif (min_mz is not None) and (max_mz is None):
            max_mz = self.max_mz + 1

        if min_mz is not None:
            n = _ims.imzb_reader_dbscan2(self._reader,
                                         ffi.cast("int", minPts), ffi.cast("double", eps),
                                         ffi.cast("double", min_mz), ffi.cast("double", max_mz),
                                         bins_ptr)
        assert ffi.sizeof('MzBin') == 7 * 8
        dtype = [('left', 'f8'), ('right', 'f8'), ('count', 'u8'), ('_', 'u8'),
                 ('sum', 'f8'), ('sumsq', 'f8'), ('intensity', 'f8')]
        arr = np.frombuffer(ffi.buffer(bins_ptr[0], n * ffi.sizeof('MzBin')), dtype, n)
        df = pd.DataFrame(arr)
        df['mean'] = df['sum'] / df['count']
        df['sd'] = (df['sumsq'] / df['count'] - df['mean'] ** 2) ** 0.5
        del df['_'], df['sum'], df['sumsq']
        _ims.free(bins_ptr[0])
        return df

def measure_of_chaos(im, nlevels):
    """
    Compute a measure for the spatial chaos in given image using the level sets method.

    :param im: 2d array
    :param nlevels: how many levels to use (maximum of 32 in this implementation)
    :type nlevels: int
    """
    assert nlevels > 0
    if nlevels > 32:
        raise RuntimeError("maximum of 32 levels is supported")
    im = _cffi_buffer(im, 'f')
    return _ims.measure_of_chaos_f(im.ptr,
                                   ffi.cast("int", im.buf.shape[1]),
                                   ffi.cast("int", im.buf.shape[0]),
                                   ffi.cast("int", nlevels))

def _compute_metric(metric, images_flat, theor_iso_intensities):
    assert len(images_flat) == len(theor_iso_intensities)
    assert all(np.shape(im) == np.shape(images_flat[0]) for im in images_flat)
    assert all(len(np.shape(im)) == 1 for im in images_flat)
    assert all(intensity >= 0 for intensity in theor_iso_intensities)

    n = len(images_flat)
    images = ffi.new("float*[]", n)
    buffers = [_cffi_buffer(im, 'f') for im in images_flat]
    for i, im in enumerate(images_flat):
        images[i] = buffers[i].ptr
    abundances = _cffi_buffer(theor_iso_intensities, 'd')

    return metric(images,
                  ffi.cast("int", n),
                  ffi.cast("int", len(images_flat[0])),
                  ffi.cast("int", 1),
                  abundances.ptr)

def isotope_pattern_match(images_flat, theor_iso_intensities):
    """
    Measures similarity between total isotope image intensities and the theoretical pattern.

    :param images_flat: list of flattened isotope images
    :param theor_iso_intensities: list of the corresponding theoretical isotope abundances
    :rtype: float
    """
    return _compute_metric(_ims.pattern_match_f, images_flat, theor_iso_intensities)

def isotope_image_correlation(images_flat, weights=None):
    """
    Calculates weighted average of correlations between principal peak image and the rest.

    :param images_flat: list of flattened isotope images
    :param weights: If provided, must be one element shorter than :code:`images_flat` list.
                    Default value of :code:`None` corresponds to equal weights.
    :rtype: float
    """
    if weights is None:
        weights = np.ones(len(images_flat))
    else:
        weights = np.concatenate(([1.0], weights))
    return _compute_metric(_ims.iso_img_correlation_f, images_flat, weights)
