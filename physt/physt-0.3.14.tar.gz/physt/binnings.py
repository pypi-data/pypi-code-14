from __future__ import absolute_import
"""Different binning algorithms/schemas for the histograms."""

import numpy as np
from .bin_utils import (
    make_bin_array, is_consecutive, to_numpy_bins, is_rising, is_bin_subset, to_numpy_bins_with_mask)


# TODO: Locking and edit operations (like numpy read-only)


class BinningBase(object):
    """Abstract base class for binning.

    Inheriting
    ----------
    - define at least one of the following properties: bins, numpy_bins (cached intercomputation exists)
    - if you modify the bins, be sure to put _bins and _numpy_bins into proper state (in some cases, None is sufficient)
    - checking of proper bins should be done in __init__
    - if you want to support adaptive histogram, override _force_bin_existence
    """
    def __init__(self, bins=None, numpy_bins=None, includes_right_edge=False, integrity_check=True, adaptive=False):
        # TODO: Incorporate integrity_check parameter
        self._consecutive = None
        if bins is not None:
            if numpy_bins is not None:
                raise RuntimeError("Cannot specify numpy_bins and bins at the same time.")
            bins = make_bin_array(bins)
            if not is_rising(bins):
                raise RuntimeError("Bins must be in rising order.")
            # TODO: Test for consecutiveness?
        elif numpy_bins is not None:
            numpy_bins = to_numpy_bins(numpy_bins)
            if not np.all(numpy_bins[1:] > numpy_bins[:-1]):
                raise RuntimeError("Bins must be in rising order.")
            self._consecutive = True
        self._bins = bins
        self._numpy_bins = numpy_bins
        self._includes_right_edge = includes_right_edge
        if adaptive and not self.adaptive_allowed:
            raise RuntimeError("Adaptivity not allowed for {0}".format(self.__class__.__name__))
        if adaptive and includes_right_edge:
            raise RuntimeError("Adaptivity does not work together with right-edge inclusion.")
        self._adaptive = adaptive

    adaptive_allowed = False
    inconsecutive_allowed = False
    # TODO: adding allowed?

    @property
    def includes_right_edge(self):
        return self._includes_right_edge

    def is_regular(self, rtol=1.e-5, atol=1.e-8):
        """Whether all bins have the same width.

        Parameters
        ----------
        rtol, atol : float
            numpy tolerance parameters

        Returns
        -------
        bool
        """
        return np.allclose(np.diff(self.bins[1] - self.bins[0]), 0.0, rtol=rtol, atol=atol)

    def is_consecutive(self, rtol=1.e-5, atol=1.e-8):
        """Whether all bins are in a growing order.

        Parameters
        ----------
        rtol, atol : float
            numpy tolerance parameters

        Returns
        -------
        bool
        """
        if self.inconsecutive_allowed:
            if self._consecutive is None:
                if self._numpy_bins is not None:
                    self._consecutive = True
                self._consecutive = is_consecutive(self.bins, rtol, atol)
            return self._consecutive
        else:
            return True

    def is_adaptive(self):
        """Whether the binning can be adapted to include values not currently spanned.

        Returns
        -------
        bool
        """
        return self._adaptive

    def force_bin_existence(self, values):
        """Change schema so that there is a bin for value

        Parameters
        ----------
        values: np.ndarray
            All values we want bins for.

        Returns
        -------
        bin_map: Iterable[tuple] or None or int
            None => There was no change in bins
            int => The bins are only shifted (allows mass assignment)
            Otherwise => the iterable contains tuples (old bin index, new bin index)
                new bin index can occur multiple times, which corresponds to bin merging
        """
        # TODO: Rename to something less evil
        if not self.is_adaptive():
            raise RuntimeError("Histogram is not adaptive")
        else:
            return self._force_bin_existence(values)

    def _force_bin_existence(self, values):
        # TODO: in-place
        raise NotImplementedError()

    def adapt(self, other):
        """Adapt this binning so that it contains all bins of another binning.

        Parameters
        ----------
        other: BinningBase

        Returns
        -------

        """
        # TODO: in-place arg
        if np.array_equal(self.bins, other.bins):
            return None, None
        elif not self.is_adaptive():
            raise RuntimeError("Cannot adapt non-adaptive binning.")
        else:
            return self._adapt(other)

    def set_adaptive(self, value=True):
        if value and not self.adaptive_allowed:
            raise RuntimeError("Cannot change binning to adaptive.")
        self._adaptive = value

    def _adapt(self, other):
        raise RuntimeError("Cannot adapt binning.")

    @property
    def bins(self):
        if self._bins is None:
            self._bins = make_bin_array(self.numpy_bins)
        return self._bins

    @property
    def bin_count(self):
        return self.bins.shape[0]

    @property
    def numpy_bins(self):
        if self._numpy_bins is None:
            self._numpy_bins = to_numpy_bins(self.bins)
        return self._numpy_bins

    @property
    def numpy_bins_with_mask(self):
        bwm = to_numpy_bins_with_mask(self.bins)
        if not self.includes_right_edge:
            bwm[0].append(np.inf)
        return bwm

    @property
    def first_edge(self):
        if self._numpy_bins is None:
            return self._numpy_bins[0]
        else:
            return self.bins[0][0]

    @property
    def last_edge(self):
        if self._numpy_bins is None:
            return self._numpy_bins[-1]
        else:
            return self.bins[-1][1]

    def as_static(self, copy=True):
        """Convert binning to a static form.

        Parameters
        ----------
        copy: bool
            Ensure that we receive another object

        Returns
        -------
        StaticBinning
            A new static binning with a copy of bins.
        """
        return StaticBinning(bins=self.bins.copy(), includes_right_edge=self.includes_right_edge)

    def as_fixed_width(self, copy=True):
        """Convert binning to recipe with fixed width.

        Parameters
        ----------
        copy: bool
            Ensure that we receive another object

        Returns
        -------
        FixedWidthBinning
        """
        if self.bin_count == 0:
            raise RuntimeError("Cannot guess binning width with zero bins")
        elif self.bin_count == 1 or self.is_consecutive() and self.is_regular():
            return FixedWidthBinning(min=self.bins[0][0], bin_count=self.bin_count, bin_width=self.bins[1] - self.bins[0])
        else:
            raise RuntimeError("Cannot create fixed-width binning from differing bin widths.")

    def copy(self):
        """
        Returns
        -------
        BinningBase
        """
        raise NotImplementedError()

    def apply_bin_map(self, bin_map):
        """

        Parameters
        ----------
        bin_map: Iterator(tuple)
            The bins must be in ascending order

        Returns
        -------
        BinningBase
        """
        length = max(item[1] for item in bin_map) + 1
        bins = np.empty((length, 2), dtype=float)
        bins[:] = np.nan
        for old, new in bin_map:
            if np.isnan(bins[new, 0]):
                bins[new, :] = self.bins[old, :]
            else:
                if bins[new, 1] != self.bins[old, 0]:
                    raise RuntimeError("Merging non-consecutive bins")
                bins[new, 1] = self.bins[old, 1]
        if np.any(np.isnan(bins)):
            raise RuntimeError("New binning is not complete.")
        includes_right_edge = (self.includes_right_edge and bins[-1, 1] == self.bins[-1, 1])
        binning = StaticBinning(bins, includes_right_edge=includes_right_edge)
        return binning


class StaticBinning(BinningBase):
    inconsecutive_allowed = True

    def __init__(self, bins, includes_right_edge=True, **kwargs):
        super(StaticBinning, self).__init__(bins=bins, includes_right_edge=includes_right_edge)

    def as_static(self, copy=True):
        """Convert binning to a static form.

        Returns
        -------
        StaticBinning
            A new static binning with a copy of bins.

        Parameters
        ----------
        copy : bool
            if True, returns itself (already satisfying conditions).
        """
        if copy:
            return StaticBinning(bins=self.bins.copy(), includes_right_edge=self.includes_right_edge)
        else:
            return self

    def copy(self):
        return self.as_static(True)

    def __getitem__(self, item):
        copy = self.copy()
        copy._bins = self._bins[item]
        # TODO: check for the right_edge??
        return copy

    def _adapt(self, other):
        if is_bin_subset(other.bins, self.bins):
            indices = np.searchsorted(other.bins[:,0], self.bins[:,0])
            return None, list(enumerate(indices))


class NumpyBinning(BinningBase):
    """Binning schema working as numpy.histogram.
    """
    def __init__(self, numpy_bins, includes_right_edge=True, **kwargs):
        if not is_rising(numpy_bins):
            raise RuntimeError("Bins not in rising order.")
        super(NumpyBinning, self).__init__(numpy_bins=numpy_bins, includes_right_edge=includes_right_edge, **kwargs)

    @property
    def numpy_bins(self):
        return self._numpy_bins

    def copy(self):
        return NumpyBinning(numpy_bins=self.numpy_bins, includes_right_edge=self.includes_right_edge)


class FixedWidthBinning(BinningBase):
    """Binning schema with predefined bin width."""
    adaptive_allowed = True

    def __init__(self, bin_width, bin_count=0, times_min=None, min=None, includes_right_edge=False, adaptive=False,
                 shift=None, align=True):
        super(FixedWidthBinning, self).__init__(adaptive=adaptive, includes_right_edge=includes_right_edge)
        # TODO: Check edge cases for min/shift/align
        if bin_width <= 0:
            raise RuntimeError("Bin width must be > 0.")
        if bin_count < 0:
            raise RuntimeError("Bin count must be >= 0.")
        if (times_min is not None or shift is not None) and (min is not None):
            raise RuntimeError("Cannot specify both min and (times_min or shift)")
        self._bin_width = float(bin_width)
        self._align = align
        self._bin_count = int(bin_count)
        if min is not None:
            self._times_min = int(np.floor(min / self.bin_width))
            self._shift = min - self._times_min * self.bin_width
        else:
            self._times_min = times_min
            self._shift = shift or 0.0
        self._bins = None
        self._numpy_bins = None

    def is_regular(self, *args, **kwargs):
        return True

    def _force_bin_existence_single(self, value, includes_right_edge=None):
        if includes_right_edge is None:
            includes_right_edge = self.includes_right_edge

        if self._bin_count == 0:
            #print("Beg from zero")
            self._times_min = int(np.floor((value - self._shift) / self.bin_width))
            if not self._align:
                self._shift = value - self._times_min * self.bin_width
            self._bin_count = 1
            self._bins = None
            self._numpy_bins = None
            #print("Bins: ", self.bin_count)
            return ()
        else:
            #print("Beg from non-zero")
            original_count = self.bin_count
            add_left = add_right = 0
            if value < self.numpy_bins[0]:
                add_left = int(np.ceil((self.numpy_bins[0] - value) / self.bin_width))
                self._times_min -= add_left
                self._bin_count += add_left
            elif value >= self.numpy_bins[-1]:
                add_right = (value - self.numpy_bins[-1]) /  self.bin_width
                # print(add_right, includes_right_edge)
                #print(add_right - np.floor(add_right), add_right - np.floor(add_right) == 0)
                add_right = int(np.ceil(add_right))
                # print("Quindi", add_right)
                self._bin_count += add_right
                if self.last_edge == value and not includes_right_edge:
                    add_right += 1
                    self._bin_count += 1
            if add_left or add_right:
                self._bins = None
                self._numpy_bins = None
                return add_left
                # return ((i, i + add_left) for i in range(original_count))
            else:
                return None

    def _force_bin_existence(self, values, includes_right_edge=None):
        if np.isscalar(values):
            return self._force_bin_existence_single(values, includes_right_edge=includes_right_edge)
        else:
            min, max = np.min(values), np.max(values)
            result = self._force_bin_existence_single(min)
            result2 = self._force_bin_existence_single(max, includes_right_edge=includes_right_edge)
            if result is None:
                return result2
            else:
                return result

    @property
    def first_edge(self):
        return self._times_min * self._bin_width + self._shift

    @property
    def last_edge(self):
        return (self._times_min + self._bin_count) * self._bin_width + self._shift

    @property
    def numpy_bins(self):
        if self._numpy_bins is None:
            self._bins = None
            if self._bin_count == 0:
                return np.zeros((0, 2), dtype=float)
            self._numpy_bins = (self._times_min + np.arange(self._bin_count + 1, dtype=int)) * self._bin_width + self._shift
        return self._numpy_bins

    @property
    def bin_count(self):
        return self._bin_count

    def copy(self):
        return FixedWidthBinning(
            bin_width=self._bin_width,
            bin_count=self._bin_count,
            align=self._align,  # Not necessary
            times_min=self._times_min,
            shift=self._shift,
            includes_right_edge=self.includes_right_edge,
            adaptive=self._adaptive)

    @property
    def bin_width(self):
        return self._bin_width

    def _force_new_min_max(self, new_min, new_max):
        bin_map = None
        add_right = add_left = 0
        if new_min < self._times_min:
            add_left = self._times_min - new_min
        if new_max - self._times_min > self._bin_count:
            add_right = new_max - self._times_min - self._bin_count
        if add_left or add_right:
            bin_map = ((i, i + add_left) for i in range(self._bin_count))
            self._set_min_and_count(
                self._times_min - add_left,
                self._bin_count + add_left + add_right)
        return bin_map

    def _set_min_and_count(self, times_min, bin_count):
        self._bin_count = bin_count
        self._times_min = times_min
        self._bins = None
        self._numpy_bins = None

    def _adapt(self, other):
        """

        Parameters
        ----------
        other: BinningBase

        Returns
        -------
        bin_map1: Iterable[tuple] or None
        bin_map2: Iterable[tuple] or None
        """
        other = other.as_fixed_width()
        if self.bin_width != other.bin_width:
            raise RuntimeError("Cannot adapt fixed-width histograms with different widths")
        if self._shift != other._shift:
            raise RuntimeError("Cannot adapt shifted fixed-width histograms: {0} vs {1}".format(self._shift, other._shift))
        # Following operations modify schemas
        other = other.copy()
        if other.bin_count == 0:
            return None, ()
        if self.bin_count == 0:
            self._set_min_and_count(other._times_min, other.bin_count)
            return (), None
        new_min = min(self._times_min, other._times_min)
        new_max = max(self._times_min + self._bin_count, other._times_min + other._bin_count)

        bin_map1 = self._force_new_min_max(new_min, new_max)
        bin_map2 = other._force_new_min_max(new_min, new_max)

        # bin_map1 = self._force_bin_existence([other.first_edge, other.last_edge], includes_right_edge=True)
        # bin_map2 = other._force_bin_existence([self.first_edge, self.last_edge], includes_right_edge=True)
        # if bin_map1:
        # print("#1", bin_map1 and list(bin_map1))
        # print("#2", bin_map2 and list(bin_map2))
        return bin_map1, bin_map2

    def as_fixed_width(self, copy=True):
        if copy:
            return self.copy()
        else:
            return self


class ExponentialBinning(BinningBase):
    """Binning schema with exponentially distributed bins."""
    adaptive_allowed = False

    # TODO: Implement adaptivity

    def __init__(self, log_min, log_width, bin_count, includes_right_edge=True, adaptive=False):
        super(ExponentialBinning, self).__init__(includes_right_edge=includes_right_edge, adaptive=adaptive)
        self._log_min = log_min
        self._log_width = log_width
        self._bin_count = bin_count

    def is_regular(self, *args, **kwargs):
        return False

    @property
    def numpy_bins(self):
        if self._bin_count == 0:
            return np.ndarray((0,), dtype=float)
        if self._numpy_bins is None:
            log_bins = self._log_min + np.arange(self._bin_count + 1) * self._log_width
            self._numpy_bins = 10 ** log_bins
        return self._numpy_bins

    def copy(self):
        return ExponentialBinning(self._log_min, self._log_width, self._bin_count, self.includes_right_edge)


def numpy_binning(data, bins=10, range=None, *args, **kwargs):
    """Construct binning schema compatible with numpy.histogram

    Parameters
    ----------
    data: array_like, optional
        This is optional if both bins and range are set
    bins: int or array_like
    range: Optional[tuple]
        (min, max)
    includes_right_edge: Optional[bool]
        default: True

    Returns
    -------
    NumpyBinning

    See Also
    --------
    numpy.histogram
    """
    if isinstance(bins, int):
        if range:
            bins = np.linspace(range[0], range[1], bins + 1)
        else:
            start = data.min()
            stop = data.max()
            bins = np.linspace(start, stop, bins + 1)
    elif np.iterable(bins):
        bins = np.asarray(bins)
    else:
        # Some numpy edge case
        _, bins = np.histogram(data, bins, **kwargs)
    return NumpyBinning(bins)


def human_binning(data=None, bins=None, range=None, **kwargs):
    """Construct fixed-width ninning schema with bins automatically optimized to human-friendly widths.

    Typical widths are: 1.0, 25,0, 0.02, 500, 2.5e-7, ...

    Parameters
    ----------
    bins: Optional[int]
        Number of bins
    range: Optional[tuple]
        (min, max)

    Returns
    -------
    FixedWidthBinning
    """
    subscales = np.array([0.5, 1, 2, 2.5, 5, 10])

    # TODO: remove colliding kwargs
    if data is None and range is None:
        raise RuntimeError("Cannot guess optimum bin width without data.")
    if bins is None:
        bins = ideal_bin_count(data)
    min_ = range[0] if range else data.min()
    max_ = range[1] if range else data.max()
    bw = (max_ - min_) / bins

    power = np.floor(np.log10(bw)).astype(int)
    best_index = np.argmin(np.abs(np.log(subscales * (10 ** power) / bw)))
    bin_width = (10 ** power) * subscales[best_index]
    return fixed_width_binning(bin_width=bin_width, data=data, range=range, **kwargs)


def quantile_binning(data=None, bins=10, qrange=(0.0, 1.0), **kwargs):
    """Binning schema based on quantile ranges.

    This binning finds equally spaced quantiles. This should lead to
    all bins having roughly the same frequencies.

    Note: weights are not (yet) take into account for calculating
    quantiles.

    Parameters
    ----------
    bins: sequence or Optional[int]
        Number of bins
    qrange: Optional[tuple]
        Two floats as minimum and maximum quantile (default: 0.0, 1.0)

    Returns
    -------
    StaticBinning
    """

    if np.isscalar(bins):
        bins = np.linspace(qrange[0] * 100, qrange[1] * 100, bins + 1)
    bins = np.percentile(data, bins)
    return static_binning(bins=make_bin_array(bins), includes_right_edge=True)


def static_binning(data=None, bins=None, **kwargs):
    """Construct static binning with whatever bins."""
    return StaticBinning(bins=make_bin_array(bins), **kwargs)


def integer_binning(data=None, **kwargs):
    """Construct fixed-width binning schema with bins centered around integers.

    Parameters
    ----------
    range: Optional[Tuple[int]]
        min (included) and max integer (excluded) bin

    Returns
    -------
    StaticBinning
    """
    if "range" in kwargs:
        kwargs["range"] = tuple(r - 0.5 for r in kwargs["range"])
    return fixed_width_binning(data=data, bin_width=1, align=True, shift=0.5, **kwargs)


def fixed_width_binning(data=None, bin_width=1, range=None, includes_right_edge=False, **kwargs):
    """Construct fixed-width binning schema.

    Parameters
    ----------
    bin_width: float
    range: Optional[tuple]
        (min, max)
    align: Optional[float]
        Must be multiple of bin_width

    Returns
    -------
    FixedWidthBinning
    """
    result = FixedWidthBinning(bin_width=bin_width, includes_right_edge=includes_right_edge, **kwargs)
    if range:
        result._force_bin_existence(range[0])
        result._force_bin_existence(range[1], includes_right_edge=True)
        if not kwargs.get("adaptive"):
            return result  # Otherwise we want to adapt to data
    if data is not None and data.shape[0]:
        # print("Jo, tady")
        result._force_bin_existence([np.min(data), np.max(data)], includes_right_edge=includes_right_edge)
    return result


def exponential_binning(data=None, bins=None, range=None, **kwargs):
    """Construct exponential binning schema.

    Parameters
    ----------
    bins: Optional[int]
        Number of bins
    range: Optional[tuple]
        (min, max)

    Returns
    -------
    ExponentialBinning

    See also
    --------
    numpy.logspace - note that our range semantics is different
    """
    if bins is None:
        bins = ideal_bin_count(data)

    if range:
        range = (np.log10(range[0]), np.log10(range[1]))
    else:
        range = (np.log10(data.min()), np.log10(data.max()))
    log_width = (range[1] - range[0]) / bins
    return ExponentialBinning(log_min=range[0], log_width=log_width, bin_count=bins, **kwargs)


def calculate_bins(array, _=None, *args, **kwargs):
    """Find optimal binning from arguments.

    Parameters
    ----------
    array: arraylike
        Data from which the bins should be decided (sometimes used, sometimes not)
    _: int or str or Callable or arraylike or Iterable
        To-be-guessed parameter that specifies what kind of binning should be done
    check_nan: bool
        Check for the presence of nan's in array? Default: True
    range: tuple
        Limit values to a range. Some of the binning methods also (subsequently)
        use this parameter for the bin shape.

    Returns
    -------
    BinningBase
        A two-dimensional array with pairs of bin edges (not necessarily consecutive).

    """
    if kwargs.pop("check_nan", True):
        if np.any(np.isnan(array)):
            raise RuntimeError("Cannot calculate bins in presence of NaN's.")
    if kwargs.get("range", None):   # TODO: re-consider the usage of this parameter
        array = array[(array >= kwargs["range"][0]) & (array <= kwargs["range"][1])]
    if _ is None:
        bin_count = 10 # kwargs.pop("bins", ideal_bin_count(data=array)) - same as numpy
        binning = numpy_binning(array, bin_count, *args, **kwargs)
    elif isinstance(_, int):
        binning =  numpy_binning(array, _, *args, **kwargs)
    elif isinstance(_, str):
        # What about the ranges???
        if _ in bincount_methods:
            bin_count = ideal_bin_count(array, method=_)
            binning = numpy_binning(array, bin_count, *args, **kwargs)
        elif _ in binning_methods:
            method = binning_methods[_]
            binning = method(array, *args, **kwargs)
        else:
            raise RuntimeError("No binning method {0} available.".format(_))
    elif callable(_):
        binning = _(array, *args, **kwargs)
    elif np.iterable(_):
        binning = static_binning(array, _, *args, **kwargs)
    else:
        raise RuntimeError("Binning {0} not understood.".format(_))
    return binning


def calculate_bins_nd(array, bins=None, *args, **kwargs):
    """Find optimal binning from arguments (n-dimensional variant)

    Usage similar to `calculate_bins`.

    Returns
    -------
    List[BinningBase]
    """
    if kwargs.pop("check_nan", True):
        if np.any(np.isnan(array)):
            raise RuntimeError("Cannot calculate bins in presence of NaN's.")

    if array is not None:
        _, dim = array.shape

    # Prepare bins
    if isinstance(bins, (list, tuple)):
        if len(bins) != dim:
            raise RuntimeError("List of bins not understood.")
    else:
        bins = [bins] * dim

    # Prepare arguments
    args = list(args)
    range_ = kwargs.pop("range", None)
    if range_:
        if len(range_) == 2 and all(np.isscalar(i) for i in range_):
            range_ = dim * [range_]
        elif len(range_) != dim:
            raise RuntimeError("Wrong dimensionality of range")
    for i in range(len(args)):
        if isinstance(args[i], (list, tuple)):
            if len(args[i]) != dim:
                raise RuntimeError("Argument not understood.")
        else:
            args[i] = dim * [args[i]]
    for key in list(kwargs.keys()):
        if isinstance(kwargs[key], (list, tuple)):
            if len(kwargs[key]) != dim:
                raise RuntimeError("Argument not understood.")
        else:
            kwargs[key] = dim * [kwargs[key]]

    if range_:
        kwargs["range"] = range_

    bins = [
        calculate_bins(array[:, i], bins[i],
                       *(arg[i] for arg in args),
                       **{k : kwarg[i] for k, kwarg in kwargs.items()})
        for i in range(dim)
        ]
    return bins


# TODO: Rename
binning_methods = {
    "numpy" : numpy_binning,
    "exponential" : exponential_binning,
    "quantile": quantile_binning,
    "fixed_width": fixed_width_binning,
    "integer": integer_binning,
    "human" : human_binning
}


try:
    from astropy.stats.histogram import histogram as _astropy_histogram   # Just check
    import warnings
    warnings.filterwarnings("ignore", module="astropy\..*")

    def bayesian_blocks_binning(data, range=None, **kwargs):
        """Binning schema based on Bayesian blocks (from astropy).

        Computationally expensive for large data sets.

        Parameters
        ----------
        range: Optional[tuple]

        Returns
        -------
        StaticBinning

        See also
        --------
        astropy.stats.histogram.bayesian_blocks
        astropy.stats.histogram.histogram
        """
        from astropy.stats.histogram import bayesian_blocks
        if range is not None:
            data = data[(data >= range[0]) & (data <= range[1])]
        edges = bayesian_blocks(data)
        return NumpyBinning(edges, **kwargs)

    def knuth_binning(data, range=None, **kwargs):
        """Binning schema based on Knuth's rule (from astropy).

        Computationally expensive for large data sets.

        Parameters
        ----------
        data: arraylike
        range: Optional[tuple]

        Returns
        -------
        StaticBinning

        See also
        --------
        astropy.stats.histogram.knuth_bin_width
        astropy.stats.histogram.histogram
        """
        # TODO: Could we possibly use it with FixedWidthBinning?
        from astropy.stats.histogram import knuth_bin_width
        if range is not None:
            data = data[(data >= range[0]) & (data <= range[1])]
        _, edges = knuth_bin_width(data, True)
        return NumpyBinning(edges, **kwargs)

    def scott_binning(data, range=None, **kwargs):
        """Binning schema based on Scott's rule (from astropy).

        Parameters
        ----------
        data: arraylike
        range: Optional[tuple]

        Returns
        -------
        StaticBinning

        See also
        --------
        astropy.stats.histogram.scott_bin_width
        astropy.stats.histogram.histogram
        """
        from astropy.stats.histogram import scott_bin_width
        if range is not None:
            data = data[(data >= range[0]) & (data <= range[1])]
        _, edges = scott_bin_width(data, True)
        return NumpyBinning(edges, **kwargs)

    def freedman_binning(data, range=None, **kwargs):
        """Binning schema based on Freedman-Diaconis rule (from astropy).

        Parameters
        ----------
        data: arraylike
        range: Optional[tuple]

        Returns
        -------
        StaticBinning

        See also
        --------
        astropy.stats.histogram.freedman_bin_width
        astropy.stats.histogram.histogram
        """
        # TODO: Could we possibly use it with FixedWidthBinning?
        from astropy.stats.histogram import freedman_bin_width
        if range is not None:
            data = data[(data >= range[0]) & (data <= range[1])]
        _, edges = freedman_bin_width(data, True)
        return NumpyBinning(edges, **kwargs)

    binning_methods["blocks"] = bayesian_blocks_binning
    binning_methods["knuth"] = knuth_binning
    binning_methods["scott"] = scott_binning
    binning_methods["freedman"] = freedman_binning
except:
    pass     # astropy is not required


def ideal_bin_count(data, method="default"):
    """A theoretically ideal bin count.

    Parameters
    ----------
    data: array_like or None
        Data to work on. Most methods don't use this.
    method: str
        Name of the method to apply, available values:
          - default
          - sqrt
          - sturges
          - doane
        See https://en.wikipedia.org/wiki/Histogram for the description

    Returns
    -------
    int
        Number of bins, always >= 1
    """
    n = data.size
    if n < 1:
        return 1
    if method == "default":
        if n <= 32:
            return 7
        else:
            return ideal_bin_count(data, "sturges")
    elif method == "sqrt":
        return int(np.ceil(np.sqrt(n)))
    elif method == "sturges":
        return int(np.ceil(np.log2(n)) + 1)
    elif method == "doane":
        if n < 3:
            return 1
        from scipy.stats import skew
        sigma = np.sqrt(6 * (n-2) / (n + 1) * (n + 3))
        return int(np.ceil(1 + np.log2(n) + np.log2(1 + np.abs(skew(data)) / sigma)))
    elif method == "rice":
        return int(np.ceil(2 * np.power(n, 1 / 3)))


bincount_methods = ["default", "sturges", "rice", "sqrt", "doane"]

def as_binning(obj, copy=False):
    """Ensure that an object is a binning

    Parameters
    ---------
    obj : BinningBase or array_like
        Can be a binning, numpy-like bins or full physt bins
    copy : bool
        If true, ensure that the returned object is independent
    """
    if isinstance(obj, BinningBase):
        if copy:
            return obj.copy()
        else:
            return obj
    else:
        bins = make_bin_array(obj)
        return StaticBinning(bins)
