
import csv
import logging
import os
import os.path as op
import shutil

import numpy as np
import scipy.io as sio

from phy.io.array import (_get_data_lim,
                          _concatenate_virtual_arrays,
                          )

logger = logging.getLogger(__name__)


def read_array(path):
    arr_name, ext = op.splitext(path)
    if ext == '.mat':
        return sio.loadmat(path)[arr_name]
    elif ext == '.npy':
        return np.load(path, mmap_mode='r')


def write_array(name, arr):
    np.save(name, arr)


def load_metadata(filename, cluster_ids):
    """Load cluster metadata from a CSV file."""
    dic = {cluster_id: None for cluster_id in cluster_ids}
    if not op.exists(filename):
        return dic
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        # Skip the header.
        for row in reader:
            break
        for row in reader:
            cluster, value = row
            cluster = int(cluster)
            dic[cluster] = value
    return dic


def save_metadata(filename, field_name, metadata):
    """Save metadata in a CSV file."""
    import sys
    if sys.version_info[0] < 3:
        file = open(filename, 'wb')
    else:
        file = open(filename, 'w', newline='')
    with file as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['cluster_id', field_name])
        writer.writerows([(cluster, metadata[cluster])
                          for cluster in sorted(metadata)])


def _dat_n_samples(filename, dtype=None, n_channels=None, offset=None):
    assert dtype is not None
    item_size = np.dtype(dtype).itemsize
    offset = offset if offset else 0
    n_samples = (op.getsize(filename) - offset) // (item_size * n_channels)
    assert n_samples >= 0
    return n_samples


def _dat_to_traces(dat_path, n_channels=None, dtype=None, offset=None):
    assert dtype is not None
    assert n_channels is not None
    n_samples = _dat_n_samples(dat_path,
                               n_channels=n_channels,
                               dtype=dtype,
                               offset=offset,
                               )
    return np.memmap(dat_path, dtype=dtype, shape=(n_samples, n_channels),
                     offset=offset)


def load_raw_data(path=None, n_channels_dat=None, dtype=None, offset=None):
    if not path:
        return
    if not op.exists(path):
        logger.warning("Error while loading data: File `%s` not found.",
                       path)
        return None
    assert op.exists(path)
    logger.debug("Loading traces at `%s`.", path)
    return _dat_to_traces(path,
                          n_channels=n_channels_dat,
                          dtype=dtype or np.int16,
                          offset=offset,
                          )


def get_closest_channels(channel_positions, n=None):
    """Return a (n_channels, n) array with the closest channels to
    each channel.
    """
    x = channel_positions[:, 0]
    y = channel_positions[:, 1]
    dx = x[:, np.newaxis] - x[np.newaxis, :]
    dy = y[:, np.newaxis] - y[np.newaxis, :]
    d = dx ** 2 + dy ** 2
    out = np.argsort(d, axis=1)
    if n:
        out = out[:, :n]
    return out


def get_masks(templates, closest_channels):
    # TODO: precompute channels to each channel
    n_templates, n_samples_templates, n_channels = templates.shape
    # Template max.
    amp = templates.max(axis=1)  # (n_templates, n_channels)
    # Template min.
    mi = templates.min(axis=1)  # (n_templates, n_channels)
    # Template amplitudes across all channels.
    amp -= mi  # (n_templates, n_channels)
    # The best channel for each template.
    best = np.argmax(amp, axis=1)  # (n_templates,)
    # Create the masks array.
    masks = np.zeros((n_templates, n_channels))
    assert closest_channels.shape[0] == n_channels
    n = closest_channels.shape[1]
    # For each template, the closest channels.
    ch = closest_channels[best, :]  # (n_templates, n)
    x = np.arange(n_templates)
    x = np.tile(x[:, np.newaxis], (1, n))
    masks[x, ch] = 1
    return masks


class FeatureProviderV1(object):
    def __init__(self, features=None, features_ind=None,
                 features_spike_ids=None,
                 template_features=None,
                 template_features_ind=None,
                 ):
        pass


class TemplateProviderV1(object):
    def __init__(self, templates=None, templates_unw=None,
                 wm=None, wmi=None,):
        pass


class TemplateModel(object):
    def __init__(self, dat_path=None, **kwargs):
        dat_path = dat_path or ''
        dir_path = (op.dirname(op.realpath(op.expanduser(dat_path)))
                    if dat_path else os.getcwd())
        self.dat_path = dat_path
        self.dir_path = dir_path
        self.__dict__.update(kwargs)

        self.dtype = getattr(self, 'dtype', np.int16)
        self.sample_rate = float(self.sample_rate)
        assert self.sample_rate > 0
        self.offset = getattr(self, 'offset', 0)

        self.filter_order = None if getattr(self, 'hp_filtered', False) else 3
        self.n_closest_channels = getattr(self, 'max_n_unmasked_channels', 16)
        self.mask_threshold = getattr(self, 'waveform_mask_threshold', None)

        self._load_data()

    def _load_data(self):
        sr = self.sample_rate

        self.spike_times = self._load_spike_samples() / sr
        ns, = self.n_spikes, = self.spike_times.shape

        self.amplitudes = self._load_amplitudes()
        assert self.amplitudes.shape == (ns,)

        self.spike_templates = self._load_spike_templates()
        assert self.spike_templates.shape == (ns,)

        self.spike_clusters = self._load_spike_clusters()
        assert self.spike_clusters.shape == (ns,)

        self.templates = self._load_templates()
        self.n_templates, self.n_samples_templates, self.n_channels = \
            self.templates.shape
        nc = self.n_channels

        self.channel_mapping = self._load_channel_map()
        assert self.channel_mapping.shape == (nc,)
        assert np.all(self.channel_mapping <= self.n_channels_dat - 1)

        self.channel_positions = self._load_channel_positions()
        assert self.channel_positions.shape == (nc, 2)

        self.wm = self._load_wm()
        assert self.wm.shape == (nc, nc)
        try:
            self.wmi = self._load_wmi()
        except IOError:
            self.wmi = self._compute_wmi(self.wm)
        assert self.wmi.shape == (nc, nc)

        try:
            self.templates_unw = self._load_templates_unw()
        except IOError:
            self.templates_unw = self._compute_templates_unw(self.templates,
                                                             self.wmi)
        assert self.templates_unw.shape == self.templates.shape

        self.similar_templates = self._load_similar_templates()
        assert self.similar_templates.shape == (self.n_templates,
                                                self.n_templates)

        # TODO: load waveforms, masks, template masks, features
        self.traces = self._load_traces(self.channel_mapping)
        self.duration = self.traces.shape[0] / float(self.sample_rate)

        self.template_masks = self._compute_template_masks()

        # TODO:
        # get rid of template_masks: just compute the template amplitude
        # and best channel for each template
        # WaveformLoader(traces).get(spike_ids, channels)
        # template => best channels => waveforms
        # no more masks
        # sparse templates

    def _get_array_path(self, name):
        return op.join(self.dir_path, name + '.npy')

    def _read_array(self, name):
        return read_array(self._get_array_path(name)).squeeze()

    def _write_array(self, name, arr):
        return write_array(self._get_array_path(name), arr)

    def _load_channel_map(self):
        return self._read_array('channel_map').astype(np.int32)

    def _load_channel_positions(self):
        return self._read_array('channel_positions')

    def _load_traces(self, channel_map=None):
        traces = load_raw_data(self.dat_path,
                               n_channels_dat=self.n_channels_dat,
                               dtype=self.dtype,
                               offset=self.offset,
                               )
        if traces is not None:
            # Find the scaling factor for the traces.
            scaling = 1. / _get_data_lim(traces[:10000])
            traces = _concatenate_virtual_arrays([traces],
                                                 channel_map,
                                                 scaling=scaling,
                                                 )
        return traces

    def _load_amplitudes(self):
        return self._read_array('amplitudes')

    def _load_spike_templates(self):
        return self._read_array('spike_templates').astype(np.int32)

    def _load_spike_clusters(self):
        sc_path = self._get_array_path('spike_clusters')
        # Create spike_clusters file if it doesn't exist.
        if not op.exists(sc_path):
            st_path = self._get_array_path('spike_templates')
            shutil.copy(st_path, sc_path)
        logger.debug("Loading spike clusters.")
        return self._read_array('spike_clusters').astype(np.int32)

    def _load_spike_samples(self):
        # WARNING: "spike_times.npy" is in units of samples. Need to
        # divide by the sampling rate to get spike times in seconds.
        return self._read_array('spike_times')

    def _load_similar_templates(self):
        return self._read_array('similar_templates')

    def _load_templates(self):
        logger.debug("Loading templates.")
        templates = self._read_array('templates')
        # templates[np.isnan(templates)] = 0
        return templates

    def _load_templates_unw(self):
        logger.debug("Loading unwhitened templates.")
        templates_unw = self._read_array('templates_unw')
        # templates_unw[np.isnan(templates_unw)] = 0
        return templates_unw

    def _compute_templates_unw(self, templates, wmi):
        logger.debug("Couldn't find unwhitened templates, computing them.")
        logger.debug("Unwhitening the templates %s.", templates.shape)
        templates_unw = np.dot(np.ascontiguousarray(templates),
                               np.ascontiguousarray(wmi))
        # Save the unwhitened templates.
        self._write_array('templates_unw', templates_unw)
        return templates_unw

    def _load_wm(self):
        logger.debug("Loading the whitening matrix.")
        return self._read_array('whitening_mat')

    def _load_wmi(self):
        logger.debug("Loading the inverse of the whitening matrix.")
        return self._read_array('whitening_mat_inv')

    def _compute_wmi(self, wm):
        logger.debug("Inversing the whitening matrix %s.", wm.shape)
        wmi = np.linalg.inv(wm)
        self._write_array('whitening_mat_inv', wmi)
        return wmi

    def _compute_template_masks(self):
        closest_channels = get_closest_channels(self.channel_positions,
                                                self.n_closest_channels,
                                                )
        return get_masks(self.templates, closest_channels)


if __name__ == '__main__':
    tm = TemplateModel('silico_0.dat',
                       n_channels_dat=32,
                       sample_rate=20000,
                       )
    print(tm)
