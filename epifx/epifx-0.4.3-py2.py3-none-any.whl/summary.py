from __future__ import absolute_import, division, print_function
# Note: unicode_literals produces NumPy errors, since dtype field names cannot
#       be unicode (https://github.com/numpy/numpy/issues/2407).
# from __future__ import unicode_literals

import datetime
import inspect
import numpy as np

import pypfilt
import pypfilt.stats as stats
import pypfilt.summary
from pypfilt.summary import dtype_date, Table, Monitor
import pypfilt.text

from . import obs


class PrOutbreak(Table):
    """
    Record the daily outbreak probability, defined as the sum of the weights
    of all particles in which an outbreak has been seeded.

    :param name: the name of the table in the output file.
    """

    def __init__(self, name='pr_epi'):
        Table.__init__(self, name)

    def dtype(self, params, obs_list):
        self.__model = params['model']
        return [dtype_date(), ('pr', np.float64)]

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        return n_days

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        for date, ix, hist_ix in dates:
            mask = self.__model.is_seeded(hist[hist_ix])
            seeded_weights = weights[ix, :] * mask
            date_bs = pypfilt.text.to_bytes(date)
            insert_fn((date_bs, np.sum(seeded_weights)))


class PeakMonitor(Monitor):
    """Record epidemic peak forecasts, for use with other statistics."""

    peak_size = None
    """
    A dictionary that maps observation systems to the size of each particle's
    peak with respect to that system: ``peak_size[(unit, period)]``.

    Note that this is **only** valid for tables to inspect in the
    ``finished()`` method, and **not** in the ``add_rows()`` method.
    """

    peak_date = None
    """
    A dictionary that maps observation systems to the date of each particle's
    peak with respect to that system: ``peak_date[(unit, period)]``.

    Note that this is **only** valid for tables to inspect in the
    ``finished()`` method, and **not** in the ``add_rows()`` method.
    """

    peak_time = None
    """
    A dictionary that maps observation systems to the time of each particle's
    peak with respect to that system, measured in (fractional) days from the
    start of the forecasting period: ``peak_time[(unit, period)]``.

    Note that this is **only** valid for tables to inspect in the
    ``finished()`` method, and **not** in the ``add_rows()`` method.
    """

    peak_weight = None
    """
    A dictionary that maps observation systems to the weight of each
    particle at the time that its peak occurs:
    ``peak_weight[(unit, period)]``.

    Note that this is **only** valid for tables to inspect in the
    ``finished()`` method, and **not** in the ``add_rows()`` method.
    """

    expected_obs = None
    """
    The expected observation for each particle for the duration of the
    **current simulation window**.

    Note that this is **only** valid for tables to inspect in each call to
    ``add_rows()``, and **not** in a call to ``finished()``.
    """

    def __init__(self):
        self.__run = None

    def prepare(self, params, obs_list):
        self.__params = params
        self.__obs_types = sorted(set((o['unit'], o['period'])
                                      for o in obs_list))
        self.peak_obs = {u_p: (0, None) for u_p in self.__obs_types}
        for o in obs_list:
            key = (o['unit'], o['period'])
            if o['value'] > self.peak_obs[key][0]:
                self.peak_obs[key] = (o['value'], o['date'])

    def begin_sim(self, start_date, end_date, n_days, n_sys, forecasting):
        if self.__run is None or self.__run != (start_date, end_date):
            # For each particle, record the weight and peak time.
            num_px = self.__params['size']
            self.__run = (start_date, end_date)
            self.peak_size = {k: np.zeros(num_px) for k in self.__obs_types}
            self.peak_time = {k: np.zeros(num_px) for k in self.__obs_types}
            self.peak_date = {k: np.empty(num_px, dtype='|S20')
                              for k in self.__obs_types}
            self.peak_weight = {k: np.zeros(num_px) for k in self.__obs_types}
        elif self.__run is not None and self.__run == (start_date, end_date):
            pass
        else:
            self.__run = None
            self.peak_size = None
            self.peak_time = None
            self.peak_date = None
            self.peak_weight = None

    def days_to(self, date):
        """
        Convert a date to the (fractional) number of days from the start of
        the forecasting period.
        """
        delta = date - self.__run[0]
        return delta.days + delta.seconds / 86400.0

    def monitor(self, hist, weights, fs_date, dates, obs_types):
        """Record the peak for each particle during a forecasting run."""
        # Ensure an empty data structure exists, at least.
        self.expected_obs = {}
        for (u, p) in obs_types:
            self.expected_obs[u, p] = np.array([])

        # Do nothing more if there are no dates to summarise.
        num_dates = len(dates)
        if num_dates == 0:
            return

        # Calculate the infection probabilities at every date, for every
        # observation period.
        pr_inf = {}
        pr_inf_fn = self.__params['model'].pr_inf
        periods = set([p for (_, p) in obs_types])

        for p in periods:
            # Calculate the probability of infection over the observation
            # period, and record the current and previous state vectors at
            # each date.
            pr_inf[p] = np.zeros((num_dates, hist.shape[1]))
            curr = np.zeros((num_dates, hist.shape[1], hist.shape[2]))
            prev = np.zeros((num_dates, hist.shape[1], hist.shape[2]))

            for date, ix, hist_ix in dates:
                curr[ix] = hist[hist_ix]
                n_back = self.__params['steps_per_day'] * p
                prev[ix] = pypfilt.earlier_states(hist, hist_ix, n_back)
                pr_inf[p][ix] = pr_inf_fn(prev[ix], curr[ix])

            # Record the expected observations.
            valid_types = [(u, pd) for (u, pd) in obs_types if p == pd]
            for (u, p) in valid_types:
                values = obs.expect(self.__params, u, p, pr_inf[p], prev, curr)
                self.expected_obs[u, p] = values
                max_ixs = np.argmax(values, axis=0)
                px_ixs = np.arange(values.shape[1])
                mask = values[max_ixs, px_ixs] > self.peak_size[u, p]
                max_ixs = max_ixs[mask]
                px_ixs = px_ixs[mask]
                # Record the particle weights and the peak size and time.
                self.peak_weight[u, p][mask] = weights[max_ixs, px_ixs]
                self.peak_size[u, p][mask] = values[max_ixs, px_ixs]
                self.peak_date[u, p][mask] = [dates[ix][0] for ix in max_ixs]
                self.peak_time[u, p][mask] = [self.days_to(dates[ix][0])
                                              for ix in max_ixs]


class PeakForecastEnsembles(Table):
    """
    Record the weighted ensemble of peak size and time predictions for each
    forecasting simulation.

    :param peak_monitor: an instance of :class:`.PeakMonitor`.
    :param name: the name of the table in the output file.
    """

    def __init__(self, peak_monitor, name='peak_ensemble'):
        Table.__init__(self, name)
        self.__monitor = peak_monitor

    def monitors(self):
        return [self.__monitor]

    def dtype(self, params, obs_list):
        self.__params = params
        self.__all_obs = obs_list
        self.__obs_types = sorted(set((o['unit'], o['period'])
                                      for o in obs_list))
        # Encode units into bytes, for HDF5 storage.
        self.__obs_units = {o['unit']: pypfilt.text.to_bytes(o['unit'])
                            for o in obs_list}
        ulen = max(len(bs) for unit, bs in self.__obs_units.items())
        unit = ('unit', 'S{}'.format(ulen))
        period = ('period', np.int8)
        fs_date = dtype_date('fs_date')
        weight = ('weight', np.float64)
        date = dtype_date()
        value = ('value', np.float64)
        return [unit, period, fs_date, weight, date, value]

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        if forecasting:
            return self.__params['size'] * n_sys
        else:
            return 0

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        pass

    def finished(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        fs_date_bs = pypfilt.text.to_bytes(fs_date)

        for (u, p) in obs_types:
            # Save the peak time and size ensembles.
            u_bs = self.__obs_units[u]
            for ix in range(self.__params['size']):
                row = (u_bs, p, fs_date_bs,
                       self.__monitor.peak_weight[u, p][ix],
                       self.__monitor.peak_date[u, p][ix],
                       self.__monitor.peak_size[u, p][ix])
                insert_fn(row)


class PeakForecastCIs(Table):
    """
    Record fixed-probability central credible intervals for the peak size and
    time predictions.

    :param peak_monitor: an instance of :class:`.PeakMonitor`.
    :param probs: an array of probabilities that define the size of each
        central credible interval.
        The default value is ``numpy.uint8([0, 50, 90, 95, 99, 100])``.
    :param name: the name of the table in the output file.
    """

    def __init__(self, peak_monitor, probs=None, name='peak_cints'):
        Table.__init__(self, name)
        if probs is None:
            probs = np.uint8([0, 50, 90, 95, 99, 100])
        self.__probs = probs
        self.__monitor = peak_monitor

    def monitors(self):
        return [self.__monitor]

    def dtype(self, params, obs_list):
        self.__params = params
        self.__all_obs = obs_list
        self.__obs_types = sorted(set((o['unit'], o['period'])
                                      for o in obs_list))
        # Encode units into bytes, for HDF5 storage.
        self.__obs_units = {o['unit']: pypfilt.text.to_bytes(o['unit'])
                            for o in obs_list}
        ulen = max(len(bs) for unit, bs in self.__obs_units.items())
        unit = ('unit', 'S{}'.format(ulen))
        period = ('period', np.int8)
        fs_date = dtype_date('fs_date')
        prob = ('prob', np.int8)
        s_min = ('sizemin', np.float64)
        s_max = ('sizemax', np.float64)
        t_min = dtype_date('timemin')
        t_max = dtype_date('timemax')
        return [unit, period, fs_date, prob, s_min, s_max, t_min, t_max]

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        if forecasting:
            # Need a row for each interval, for each observation system.
            return len(self.__probs) * n_sys
        else:
            return 0

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        pass

    def finished(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        fs_date_bs = pypfilt.text.to_bytes(fs_date)

        for (u, p) in obs_types:
            # Calculate the confidence intervals for peak time and size.
            sz_ints = stats.cred_wt(
                self.__monitor.peak_size[u, p],
                self.__monitor.peak_weight[u, p],
                self.__probs)
            tm_ints = stats.cred_wt(
                self.__monitor.peak_time[u, p],
                self.__monitor.peak_weight[u, p],
                self.__probs)

            # Convert from days (from the forecast date) to byte strings.
            def enc(days):
                """Convert peak times from days (as measured from the
                forecast date) to datetime strings."""
                dt = fs_date + datetime.timedelta(days)
                return pypfilt.text.to_bytes(dt)

            u_bs = self.__obs_units[u]
            for pctl in self.__probs:
                row = (u_bs, p, fs_date_bs, pctl, sz_ints[pctl][0],
                       sz_ints[pctl][1], enc(tm_ints[pctl][0]),
                       enc(tm_ints[pctl][1]))
                insert_fn(row)


class PeakSizeAccuracy(Table):
    """
    Record the accuracy of the peak size predictions against multiple accuracy
    tolerances.

    :param peak_monitor: an instance of :class:`.PeakMonitor`.
    :param name: the name of the table in the output file.
    :param toln: The accuracy thresholds for peak size predictions, expressed
        as percentages of the true size.
        The default is ``np.array([10, 20, 25, 33])``.
    """

    def __init__(self, peak_monitor, name='peak_size_acc', toln=None):
        Table.__init__(self, name)
        if toln is None:
            toln = np.array([10, 20, 25, 33])
        self.__toln = toln
        self.__num_toln = len(toln)
        self.__monitor = peak_monitor

    def monitors(self):
        return [self.__monitor]

    def dtype(self, params, obs_list):
        self.__params = params
        self.__all_obs = obs_list
        self.__obs_types = sorted(set((o['unit'], o['period'])
                                      for o in obs_list))
        # Encode units into bytes, for HDF5 storage.
        self.__obs_units = {o['unit']: pypfilt.text.to_bytes(o['unit'])
                            for o in obs_list}
        ulen = max(len(bs) for unit, bs in self.__obs_units.items())
        unit = ('unit', 'S{}'.format(ulen))
        period = ('period', np.int8)
        fs_date = dtype_date('fs_date')
        toln = ('toln', np.float64)
        acc = ('acc', np.float64)
        var = ('var', np.float64)
        savg = ('avg', np.float64)
        return [unit, period, fs_date, toln, acc, var, savg]

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        if forecasting:
            return self.__num_toln * n_sys
        else:
            return 0

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        pass

    def finished(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        obs_peaks = self.__monitor.peak_obs
        fs_date_bs = pypfilt.text.to_bytes(fs_date)

        for (u, p) in obs_types:
            # Summarise the peak size distribution.
            sop_avg, sop_var = stats.avg_var_wt(
                self.__monitor.peak_size[u, p],
                self.__monitor.peak_weight[u, p])
            # Calculate the relative size of each forecast peak.
            sop_rel = self.__monitor.peak_size[u, p] / obs_peaks[(u, p)][0]

            u_bs = self.__obs_units[u]
            for pcnt in self.__toln:
                # Sum the weights of the "accurate" particles.
                sop_min, sop_max = 1 - pcnt / 100.0, 1 + pcnt / 100.0
                sop_mask = np.logical_and(sop_rel >= sop_min,
                                          sop_rel <= sop_max)
                accuracy = np.sum(self.__monitor.peak_weight[u, p][sop_mask])
                row = (u_bs, p, fs_date_bs, pcnt, accuracy, sop_var, sop_avg)
                insert_fn(row)


class PeakTimeAccuracy(Table):
    """
    Record the accuracy of the peak time predictions against multiple accuracy
    tolerances.

    :param peak_monitor: an instance of :class:`.PeakMonitor`.
    :param name: the name of the table in the output file.
    :param toln: The accuracy thresholds for peak time predictions, expressed
        as numbers of days. The default is ``np.array([7, 10, 14])``.
    """

    def __init__(self, peak_monitor, name='peak_time_acc', toln=None):
        Table.__init__(self, name)
        if toln is None:
            toln = np.array([7, 10, 14])
        self.__toln = toln
        self.__num_toln = len(toln)
        self.__monitor = peak_monitor

    def monitors(self):
        return [self.__monitor]

    def dtype(self, params, obs_list):
        self.__params = params
        self.__all_obs = obs_list
        self.__obs_types = sorted(set((o['unit'], o['period'])
                                      for o in obs_list))
        # Encode units into bytes, for HDF5 storage.
        self.__obs_units = {o['unit']: pypfilt.text.to_bytes(o['unit'])
                            for o in obs_list}
        ulen = max(len(bs) for unit, bs in self.__obs_units.items())
        unit = ('unit', 'S{}'.format(ulen))
        period = ('period', np.int8)
        fs_date = dtype_date('fs_date')
        fs_date = dtype_date('fs_date')
        toln = ('toln', np.float64)
        acc = ('acc', np.float64)
        var = ('var', np.float64)
        tavg = dtype_date('avg')
        return [unit, period, fs_date, toln, acc, var, tavg]

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        if forecasting:
            return self.__num_toln * n_sys
        else:
            return 0

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        pass

    def finished(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        obs_peaks = self.__monitor.peak_obs
        fs_date_bs = pypfilt.text.to_bytes(fs_date)

        for (u, p) in obs_types:
            top_true = obs_peaks[(u, p)][1]
            dtp_true = self.__monitor.days_to(top_true)
            # Summarise the peak size distribution.
            dtp_avg, dtp_var = stats.avg_var_wt(
                self.__monitor.peak_time[u, p],
                self.__monitor.peak_weight[u, p])
            # Convert the mean time of peak to a datetime string.
            top_avg = fs_date + datetime.timedelta(dtp_avg)
            top_avg_bs = pypfilt.text.to_bytes(top_avg)

            # Calculate peak time statistics.
            u_bs = self.__obs_units[u]
            for days in self.__toln:
                # Sum the weights of the "accurate" particles.
                # Note: Shaman et al. defined accuracy as +/- one week.
                dtp_diff = dtp_true - self.__monitor.peak_time[u, p]
                dtp_mask = np.fabs(dtp_diff) <= (days + 0.5)
                accuracy = np.sum(self.__monitor.peak_weight[u, p][dtp_mask])
                row = (u_bs, p, fs_date_bs, days, accuracy, dtp_var,
                       top_avg_bs)
                insert_fn(row)


class ExpectedObs(Table):
    """
    Record fixed-probability central credible intervals for the expected
    observations.

    :param peak_monitor: an instance of :class:`.PeakMonitor`.
    :param probs: an array of probabilities that define the size of each
        central credible interval.
        The default value is ``numpy.uint8([0, 50, 90, 95, 99, 100])``.
    :param name: the name of the table in the output file.
    """

    def __init__(self, peak_monitor, probs=None, name='forecasts'):
        Table.__init__(self, name)
        if probs is None:
            probs = np.uint8([0, 50, 90, 95, 99, 100])
        self.__probs = probs
        self.__monitor = peak_monitor

    def monitors(self):
        return [self.__monitor]

    def dtype(self, params, obs_list):
        self.__params = params
        # Encode units into bytes, for HDF5 storage.
        self.__obs_units = {o['unit']: pypfilt.text.to_bytes(o['unit'])
                            for o in obs_list}
        ulen = max(len(bs) for unit, bs in self.__obs_units.items())
        unit = ('unit', 'S{}'.format(ulen))
        period = ('period', np.int8)
        fs_date = dtype_date('fs_date')
        date = dtype_date()
        prob = ('prob', np.int8)
        ymin = ('ymin', np.float64)
        ymax = ('ymax', np.float64)
        return [unit, period, fs_date, date, prob, ymin, ymax]

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        # Need a row for each interval, for each day, for each data source.
        return len(self.__probs) * n_days * n_sys

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        exp_obs = self.__monitor.expected_obs
        fs_date_bs = pypfilt.text.to_bytes(fs_date)

        for (unit, period) in obs_types:
            exp_sys = exp_obs[(unit, period)]

            unit_bs = self.__obs_units[unit]
            for date, ix, _ in dates:
                cinfs = stats.cred_wt(exp_sys[ix, :], weights[ix, :],
                                      self.__probs)
                date_bs = pypfilt.text.to_bytes(date)
                for cix, pctl in enumerate(self.__probs):
                    row = (unit_bs, period, fs_date_bs, date_bs, pctl,
                           cinfs[pctl][0], cinfs[pctl][1])
                    insert_fn(row)


class ObsLikelihood(Table):
    """
    Record the likelihood of each observation according to each particle.
    Note that this table registers its ``record_obs_llhd`` method in the
    parameter dictionary so that it can obtain the observation likelihoods.

    :param name: the name of the table in the output file.
    """

    def __init__(self, name='obs_llhd'):
        Table.__init__(self, name)
        self.__rnd = np.random.RandomState(seed=2073010)
        self.__fs_date = None

    def install_hook(self, params):
        hook_key = 'record_log_llhd_fns'
        hook_fn = self.record_obs_llhd
        if hook_key not in params['epifx']:
            params['epifx'][hook_key] = [hook_fn]
        elif hook_fn not in params['epifx'][hook_key]:
            params['epifx'][hook_key].append(hook_fn)

    def dtype(self, params, obs_list):
        self.__params = params
        self.__all_obs = obs_list
        self.__obs_dates = [o['date'] for o in obs_list]
        # Ensure the hook has been installed.
        self.install_hook(params)
        fs_date = dtype_date('fs_date')
        date = dtype_date()
        value = ('value', np.float64)
        llhd = ('llhd', np.float64)
        std_err = ('std_err', np.float64)
        forecast = ('forecast', np.bool)
        # Identify the observation data source(s).
        ulen = max(len(o['unit']) for o in obs_list)
        slen = max(len(o['source']) for o in obs_list)
        unit = ('unit', 'S{}'.format(ulen))
        source = ('source', 'S{}'.format(slen))
        return [fs_date, unit, source, date, value, llhd, std_err, forecast]

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        self.__data = []
        self.__forecasting = forecasting
        self.__start_date = start_date
        if forecasting:
            # Forecasting from the start of the simulation period.
            self.__fs_date = start_date
        else:
            # Not forecasting, so all observations are included.
            self.__fs_date = end_date
        # Need a row for each observation in the simulation period.
        n_rows = len([o for o in self.__all_obs
                      if o['date'] > start_date and o['date'] <= end_date])
        return n_rows

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        # Must force the log-likelihood calculations when forecasting.
        if self.__forecasting:
            obs_dates = {d[0]: d for d in dates
                         if d[0] in self.__obs_dates
                         and d[0] != self.__start_date}
            obs = [o for o in self.__all_obs if o['date'] in obs_dates]

            for o in obs:
                hist_ix = obs_dates[o['date']][2]
                # This will trigger the record_obs_llhd hook.
                pypfilt.log_llhd_of(self.__params, hist, hist_ix, [o])

    def record_obs_llhd(self, obs, log_llhds, weights):
        if self.__fs_date is None:
            # A forecast may be preceded by an estimation run from the most
            # recent known-good state, and we may only be interested in
            # recording summary statistics for the forecasting simulations.
            return
        # Resample to obtain a random sample from the correct density.
        params = {'resample': {
            'method': 'basic',
            'regularisation': False,
            'rnd': self.__rnd}}
        px = np.array([weights, np.zeros(weights.shape)]).T
        pypfilt.resample(params, px)
        # Retrieve the resampled particle indices.
        sample_ixs = px[:, -1].astype(int)
        # Retrieve the weight (identical for each particle).
        wt = px[0, -2]
        # Convert from log likelihoods to likelihoods.
        probs = np.exp(log_llhds[sample_ixs])
        # Calculate the mean and standard error.
        pr_mean = np.mean(probs)
        pr_serr = np.var(probs) / wt
        # Generate a corresponding row to record later.
        row = (self.__fs_date, obs['unit'], obs['source'], obs['date'],
               obs['value'], pr_mean, pr_serr, self.__forecasting)
        self.__data.append(row)

    def finished(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        for row in self.__data:
            insert_fn(row)
        self.__fs_date = None


def make(params, all_obs, extra_tbls=None, pkgs=None, **kwargs):
    """
    A convenience function that collects all of the summary statistics defined
    in the ``pypfilt.summary`` and ``epifx.summary`` modules.

    :param params: The simulation parameters.
    :param all_obs: A list of all observations.
    :param extra_tbls: A list of extra summary statistic tables to include.
    :param pkgs: A dictionary of python modules whose versions should be
        recorded in the simulation metadata. By default, all of the modules
        recorded by ``pypfilt.summary.metadata`` are included, as is the
        ``epifx`` package itself.
    :param \**kwargs: Extra arguments to pass to ``pypfilt.summary.HDF5``.
    """

    import epifx

    if pkgs is None:
        pkgs = {}
    pkgs['epifx'] = epifx

    peaks = PeakMonitor()
    tbls = [
        pypfilt.summary.ModelCIs(),
        pypfilt.summary.ParamCovar(),
        PrOutbreak(),
        ExpectedObs(peaks),
        ObsLikelihood(),
        PeakSizeAccuracy(peaks),
        PeakTimeAccuracy(peaks),
        PeakForecastCIs(peaks),
        PeakForecastEnsembles(peaks),
    ]
    if extra_tbls:
        tbls.extend(extra_tbls)

    metadata = pypfilt.summary.metadata(params, pkgs=pkgs)
    # Record whether temporal forcing was used, rather than storing a
    # string representation of the forcing function (if any).
    with_forcing = 'forcing' in metadata['param']['epifx']
    metadata['param']['epifx']['forcing'] = with_forcing
    # Remove the log-likelihood functions from the metadata.
    if 'record_log_llhd_fns' in metadata['param']['epifx']:
        del metadata['param']['epifx']['record_log_llhd_fns']

    summary = pypfilt.summary.HDF5(params, all_obs, meta=metadata, **kwargs)
    summary.add_tables(*tbls)
    return summary
