from __future__ import absolute_import
import numpy as np
from . import bin_utils, binnings
from .histogram_base import HistogramBase
from .binnings import as_binning

# TODO: Fix I/O with binning


class Histogram1D(HistogramBase):
    """One-dimensional histogram data.

    The bins can be of different widths.

    The bins need not be consecutive. However, some functionality may not be available
    for non-consecutive bins (like keeping information about underflow and overflow).

    Attributes
    ----------
    frequencies: numpy.ndarray
    errors2: numpy.ndarray
    underflow: float
    name: str
    axis_name: str
    keep_missed: bool

    These are the basic attributes that can be used in the constructor (see there)
    Other attributes are dynamic.
    """
    def __init__(self, binning, frequencies=None, errors2=None, **kwargs):
        """Constructor

        Parameters
        ----------
        binning: physt.binnings.BinningBase or array_like
            The binning
        frequencies: Optional[array_like]
            The bin contents.
        keep_missed: Optional[bool]
            Whether to keep track of underflow/overflow when filling with new values.
        underflow: Optional[float]
            Weight of observations that were smaller than the minimum bin.
        overflow: Optional[float]
            Weight of observations that were larger than the maximum bin.
        name: Optional[str]
            Name of the histogram (will be displayed as plot title)
        axis_name: Optional[str]
            Name of the characteristics that is histogrammed (will be displayed on x axis)
        errors2: Optional[array_like]
            Quadratic errors of individual bins. If not set, defaults to frequencies.
        stats: dict
            Dictionary of various statistics ("sum", "sum2")
        """
        from .binnings import BinningBase, static_binning
        self._binnings = [as_binning(binning)]

        if frequencies is None:
            self._frequencies = np.zeros(self.bins.shape[0])
        else:
            frequencies = np.asarray(frequencies)
            if frequencies.shape != (self.bins.shape[0],):
                raise RuntimeError("Values must have same dimension as bins.")
            if np.any(frequencies < 0):
                raise RuntimeError("Cannot have negative frequencies.")
            self._frequencies = frequencies

        self.keep_missed = kwargs.get("keep_missed", True)

        if self.keep_missed:
            self._missed = np.array([
                kwargs.get("underflow", 0),
                kwargs.get("overflow", 0),
                kwargs.get("inner_missed", 0)
            ], dtype=self._frequencies.dtype)
        else:
            self._missed = np.array([np.nan, np.nan, np.nan])
        self.name = kwargs.get("name", None)
        self.axis_name = kwargs.get("axis_name", self.name)
        self._stats = kwargs.get("stats", None)

        if errors2 is None:
            self._errors2 = self._frequencies.copy()
        else:
            self._errors2 = np.asarray(errors2)
        if np.any(self._errors2 < 0):
            raise RuntimeError("Cannot have negative squared errors.")
        if self._errors2.shape != self._frequencies.shape:
            raise RuntimeError("Errors must have same dimension as frequencies.")

    def __getitem__(self, i):
        """Select sub-histogram or get one bin.

        Parameters
        ----------
        i : int or slice or bool masked array or array with indices
            In most cases, this has same semantics as for numpy.ndarray.__getitem__


        Returns
        -------
        Histogram1D or float
            Depending on the parameters, a sub-histogram or content of one bin are returned.
        """
        underflow = np.nan
        overflow = np.nan
        keep_missed=False
        if isinstance(i, int):
            return self.bins[i], self.frequencies[i]
        elif isinstance(i, np.ndarray):
            if i.dtype == bool:
                if i.shape != (self.bin_count,):
                    raise IndexError("Cannot index with masked array of a wrong dimension")
        elif isinstance(i, slice):
            keep_missed=self.keep_missed
            # TODO: Fix this
            if i.step:
                raise IndexError("Cannot change the order of bins")
            if i.step == 1 or i.step is None:
                underflow = self.underflow
                overflow = self.overflow
                if i.start:
                    underflow += self.frequencies[0:i.start].sum()
                if i.stop:
                    overflow += self.frequencies[i.stop:].sum()
        # Masked arrays or item list or ...
        return self.__class__(self._binning.as_static(copy=False)[i], self.frequencies[i], self.errors2[i], overflow=overflow, keep_missed=keep_missed,
                              underflow=underflow, name=self.name, axis_name=self.axis_name, dtype=self.dtype)

    @property
    def _binning(self):
        """Adapter property for HistogramBase interface"""
        return self._binnings[0]

    @_binning.setter
    def _binning(self, value):
        self._binnings = [value]

    @property
    def bins(self):
        """Array of all bin edges.

        Returns
        -------
        numpy.ndarray
            Wide-format [[leftedge1, rightedge1], ... [leftedgeN, rightedgeN]]
        """
        # TODO: Read-only copy
        return self._binning.bins  # TODO: or this should be read-only copy?

    @property
    def numpy_bins(self):
        """Bins in the format of numpy.

        Returns
        -------
        numpy.ndarray
        """
        # TODO: If not consecutive, does not make sense
        return self._binning.numpy_bins

    @property
    def cumulative_frequencies(self):
        """Cumulative frequencies.

        Note: underflow values are not considered

        Returns
        -------
        numpy.ndarray
        """
        return self._frequencies.cumsum()

    @property
    def underflow(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[0]

    @underflow.setter
    def underflow(self, value):
        self._missed[0] = value

    @property
    def overflow(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[1]

    @overflow.setter
    def overflow(self, value):
        self._missed[1] = value

    @property
    def inner_missed(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[2]

    @inner_missed.setter
    def inner_missed(self, value):
        self._missed[2] = value

    def mean(self):
        """Statistical mean of all values entered into histogram.

        This number is precise, because we keep the necessary data
        separate from bin contents.

        Returns
        -------
        float
        """
        if self._stats:    # TODO: should be true always?
            if self.total > 0:
                return self._stats["sum"] / self.total
            else:
                return np.nan
        else:
            return None    # TODO: or error

    def std(self, ddof=0):
        """Standard deviation of all values entered into histogram.

        This number is precise, because we keep the necessary data
        separate from bin contents.

        Parameters
        ----------
        ddof: int
            Not yet used.

        Returns
        -------
        float
        """
        # TODO: Add DOF
        if self._stats:
            return np.sqrt(self.variance(ddof=ddof))
        else:
            return None    # TODO: or error

    def variance(self, ddof=0):
        """Statistical variance of all values entered into histogram.

        This number is precise, because we keep the necessary data
        separate from bin contents.

        Parameters
        ----------
        ddof: int
            Not yet used.

        Returns
        -------
        float
        """
        # TODO: Add DOF
        # http://stats.stackexchange.com/questions/6534/how-do-i-calculate-a-weighted-standard-deviation-in-excel
        if self._stats:
            if self.total > 0:
                return (self._stats["sum2"] - self._stats["sum"] ** 2 / self.total) / self.total
            else:
                return np.nan
        else:
            return None

    # TODO: Add (correct) implementation of SEM
    # def sem(self):
    #     if self._stats:
    #         return 1 / total * np.sqrt(self.variance)
    #     else:
    #         return None

    @property
    def bin_left_edges(self):
        """Left edges of all bins.

        Returns
        -------
        numpy.ndarrad
        """
        return self.bins[...,0]

    @property
    def bin_right_edges(self):
        """Right edges of all bins.

        Returns
        -------
        numpy.ndarray
        """
        return self.bins[...,1]

    @property
    def min_edge(self):
        """Left edge of the first bin.

        Returns
        -------
        float
        """
        return self.bin_left_edges[0]

    @property
    def max_edge(self):
        """Right edge of the last bin.

        Returns
        -------
        float
        """
        return self.bin_right_edges[-1]

    @property
    def bin_centers(self):
        """Centers of all bins.

        Returns
        -------
        numpy.ndarray
        """
        return (self.bin_left_edges + self.bin_right_edges) / 2

    @property
    def bin_widths(self):
        """Widths of all bins.

        Returns
        -------
        numpy.ndarray
        """
        return self.bin_right_edges - self.bin_left_edges

    @property
    def total_width(self):
        """Total width of all bins.

        In inconsecutive histograms, the missing intervals are not counted in.

        Returns
        -------
        float
        """
        return self.bin_widths.sum()

    @property
    def bin_sizes(self):
        return self.bin_widths

    def find_bin(self, value):
        """Index of bin corresponding to a value.

        Parameters
        ----------
        value: float
            Value to be searched for.

        Returns
        -------
        int
            index of bin to which value belongs (-1=underflow, N=overflow, None=not found - inconsecutive)
        """
        ixbin = np.searchsorted(self.bin_left_edges, value, side="right")
        if ixbin == 0:
            return -1
        elif ixbin == self.bin_count:
            if value <= self.bin_right_edges[-1]:
                return ixbin - 1
            else:
                return self.bin_count
        elif value < self.bin_right_edges[ixbin - 1]:
            return ixbin - 1
        elif ixbin == self.bin_count:
            return self.bin_count
        else:
            return None

    def fill(self, value, weight=1):
        """Update histogram with a new value.

        Parameters
        ----------
        value: float
            Value to be added.
        weight: float, optional
            Weight assigned to the value.

        Returns
        -------
        int
            index of bin which was incremented (-1=underflow, N=overflow, None=not found)

        Note: If a gap in unconsecutive bins is matched, underflow & overflow are not valid anymore.
        Note: Name was selected because of the eponymous method in ROOT
        """
        self._coerce_dtype(type(weight))
        if self._binning.is_adaptive():
            map = self._binning.force_bin_existence(value)
            self._reshape_data(self._binning.bin_count, map)

        ixbin = self.find_bin(value)
        if ixbin is None:
            self.overflow = np.nan
            self.underflow = np.nan
        elif ixbin == -1 and self.keep_missed:
            self.underflow += weight
        elif ixbin == self.bin_count and self.keep_missed:
            self.overflow += weight
        else:
            self._frequencies[ixbin] += weight
            self._errors2[ixbin] += weight ** 2
            if self._stats:
                self._stats["sum"] += weight * value
                self._stats["sum2"] += weight * value ** 2
        return ixbin

    def fill_n(self, values, weights=None, dropna=True):
        """Update histograms with a set of values.

        Parameters
        ----------
        values: array_like
        weights: Optional[array_like]
        drop_na: Optional[bool]
            If true (default), all nan's are skipped.
        """
        # TODO: Unify with HistogramBase
        values = np.asarray(values)
        if dropna:
            values = values[~np.isnan(values)]
        if self._binning.is_adaptive():
            map = self._binning.force_bin_existence(values)
            self._reshape_data(self._binning.bin_count, map)
        if weights:
            weights = np.asarray(weights)
            self._coerce_dtype(weights.dtype)
        frequencies, errors2, underflow, overflow, stats = calculate_frequencies(values, self._binning,
                                                                                  weights=weights, validate_bins=False)
        self._frequencies += frequencies
        self._errors2 += errors2
        # TODO: check that adaptive does not produce under-/over-flows?
        if self.keep_missed:
            self.underflow += underflow
            self.overflow += overflow
        for key in self._stats:
            self._stats[key] += stats.get(key, 0.0)

    def copy(self, include_frequencies=True):
        """A deep copy of the histogram.

        Parameters
        ----------
        include_frequencies: Optional[bool]
            If True (default), frequencies are copied. Otherwise, an empty histogram template is created.

        Returns
        -------
        Histogram1D
        """
        if include_frequencies:
            frequencies = np.copy(self.frequencies)
            underflow = self.underflow
            overflow = self.overflow
            inner_missed = self.inner_missed
            errors2 = np.copy(self.errors2)
        else:
            frequencies = None
            underflow = 0
            overflow = 0
            inner_missed = 0
            errors2 = None
        return self.__class__(self._binning.copy(), frequencies, underflow=underflow, overflow=overflow, inner_missed=inner_missed,
                              name=self.name, axis_name=self.axis_name, keep_missed=self.keep_missed, stats=self._stats,
                              errors2=errors2)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        # TODO: Change to something in binning itself
        if not np.allclose(other.bins, self.bins):
            return False
        if not np.allclose(other.frequencies, self.frequencies):
            return False
        if not np.allclose(other.errors2, self.errors2):
            return False
        if not other.overflow == self.overflow:
            return False
        if not other.underflow == self.underflow:
            return False
        if not other.inner_missed == self.inner_missed:
            return False
        if not other.name == self.name:
            return False
        if not other.axis_name == self.axis_name:
            return False
        return True

    def to_dataframe(self):
        """Convert to pandas DataFrame.

        This is not a lossless conversion - (under/over)flow info is lost.

        Returns
        -------
        pandas.DataFrame
        """
        import pandas as pd
        df = pd.DataFrame(
            {
                "left": self.bin_left_edges,
                "right": self.bin_right_edges,
                "frequency": self.frequencies,
                "error": self.errors,
            },
            columns=["left", "right", "frequency", "error"])
        return df

    def to_xarray(self):
        """Convert to xarray.Dataset

        This is an identity conversion.

        Returns
        -------
        xarray.Dataset
        """
        import xarray as xr
        data_vars = {
            "frequencies": xr.DataArray(self.frequencies, dims="bin"),
            "errors2": xr.DataArray(self.errors2, dims="bin"),
            "bins": xr.DataArray(self.bins, dims=("bin", "x01"))
        }
        coords = { }
        attrs = {
            "underflow": self.underflow,
            "overflow": self.overflow,
            "inner_missed": self.inner_missed,
            "keep_missed": self.keep_missed
        }
        # TODO: Add stats
        return xr.Dataset(data_vars, coords, attrs)

    @classmethod
    def from_xarray(cls, arr):
        """Convert form xarray.Dataset

        Parameters
        ----------
        arr: xarray.Dataset
            The data in xarray representation
        """
        kwargs = {'frequencies': arr["frequencies"],
                  'bins': arr["bins"],
                  'errors2': arr["errors2"],
                  'overflow': arr.attrs["overflow"],
                  'underflow': arr.attrs["underflow"],
                  'keep_missed': arr.attrs["keep_missed"]}
        # TODO: Add stats
        return cls(**kwargs)

    def to_json(self, path=None):
        """Convert to JSON representation.

        Parameters
        ----------
        path: Optional[str]
            Where to write the JSON.

        Returns
        -------
        str:
            The JSON representation.
        """
        from collections import OrderedDict
        import json
        data = OrderedDict()
        data["bins"] = self.bins.tolist()
        data["frequencies"] = self.frequencies.tolist()
        data["errors2"] = self.errors2.tolist()
        data["keep_missed"] = self.keep_missed
        data["underflow"] = float(self.underflow)
        data["overflow"] = float(self.overflow)
        # TODO: Add stats

        text = json.dumps(data)
        if path:
            with open(path, "w", encoding="ascii") as f:
                f.write(text)
        return text

    @classmethod
    def from_json(cls, text=None, path=None):
        """Read histogram from JSON representation.

        Paramaters
        ----------
        text: Optional[str]
            The JSON string itself.
        path: Optional[str]
            Path of the JSON file.

        Returns
        -------
        Histogram1D
        """
        import json
        if text:
            data = json.loads(text)
        else:
            with open(path, "r") as f:
                data = json.load(f)
        # TODO: Add stats
        return cls(**data)

    def __repr__(self):
        s = "{0}(bins={1}, total={2}".format(
            self.__class__.__name__, self.bins.shape[0], self.total)
        if self.underflow:
            s += ", underflow={0}".format(self.underflow)
        if self.overflow:
            s += ", overflow={0}".format(self.overflow)
        s += ")"
        return s


def calculate_frequencies(data, binning, weights=None, validate_bins=True, already_sorted=False, dtype=None):
    """Get frequencies and bin errors from the data.

    Parameters
    ----------
    data : array_like
        Data items to work on.
    binning : physt.binnings.BinningBase
        A set of bins.
    weights : array_like, optional
        Weights of the items.
    validate_bins : bool, optional
        If True (default), bins are validated to be in ascending order.
    already_sorted : bool, optional
        If True, the data being entered are already sorted, no need to sort them once more.
    dtype: Optional[type]
        Underlying type for the histogram. If weights are specified, default is float. Otherwise long

    Returns
    -------
    frequencies : numpy.ndarray
        Bin contents
    errors2 : numpy.ndarray
        Error squares of the bins
    underflow : float
        Weight of items smaller than the first bin
    overflow : float
        Weight of items larger than the last bin
    stats: dict
        { sum: ..., sum2: ...}

    Note
    ----
    Checks that the bins are in a correct order (not necessarily consecutive)
    """
    # TODO: Maybe change back to bins???

    # Statistics
    sum = 0.0
    sum2 = 0.0

    # Ensure correct binning
    bins = binning.bins # bin_utils.make_bin_array(bins)
    if validate_bins:
        if bins.shape[0] == 0:
            raise RuntimeError("Cannot have histogram with 0 bins.")
        if not bin_utils.is_rising(bins):
            raise RuntimeError("Bins must be rising.")

    if dtype is None:
        dtype = np.int64 if weights is None else np.float

    # Create 1D arrays to work on
    data = np.asarray(data).flatten()
    if weights is not None:
        import numbers
        if issubclass(dtype, numbers.Integral):
            raise RuntimeError("Histograms with weights cannot have integral dtype")
        weights = np.asarray(weights, dtype=dtype).flatten()
        if weights.shape != data.shape:
            raise RuntimeError("Weight must have the same shape as data")
    else:
        weights = np.ones(data.shape, dtype=dtype)

    # Data sorting
    if not already_sorted:
        args = np.argsort(data)
        data = data[args]
        weights = weights[args]

    # Fill frequencies and errors
    frequencies = np.zeros(bins.shape[0], dtype=dtype)
    errors2 = np.zeros(bins.shape[0], dtype=dtype)
    for xbin, bin in enumerate(bins):
        start = np.searchsorted(data, bin[0], side="left")
        if xbin == 0:
            underflow = weights[0:start].sum()
        if xbin == len(bins) - 1:
            stop = np.searchsorted(data, bin[1], side="right")
            overflow = weights[stop:].sum()
        else:
            stop = np.searchsorted(data, bin[1], side="left")
        frequencies[xbin] = weights[start:stop].sum()
        errors2[xbin] = (weights[start:stop] ** 2).sum()
        sum += (data[start:stop] * weights[start:stop]).sum()
        sum2 += ((data[start:stop]) ** 2 * weights[start:stop]).sum()

    # Underflow and overflow don't make sense for unconsecutive binning.
    if not bin_utils.is_consecutive(bins):
        underflow = np.nan
        overflow = np.nan

    stats = { "sum": sum, "sum2" : sum2}

    return frequencies, errors2, underflow, overflow, stats
