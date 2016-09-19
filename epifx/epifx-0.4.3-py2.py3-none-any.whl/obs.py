"""Observation models: expected values and log likelihoods."""

from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import codecs
import datetime
import numpy as np
import pypfilt.summary
import pypfilt.text
import scipy.stats

from scipy.special import betaln, gammaln


def from_model(params, when, unit, period, pr_inf):
    """Determine the expected observation for a given infection probability.

    :param params: The observation model parameters.
    :param when: The end of the observation period.
    :type when: datetime.datetime
    :param unit: The observation units (see classes in :py:module`data`).
    :type unit: str
    :param period: The duration of the observation period (in days).
    :type period: int
    :param pr_inf: The probability of an individual becoming infected during
        the observation period.
    :type pr_inf: float
    """
    return {'date': when,
            'value': expect(params, unit, period, pr_inf),
            'unit': unit,
            'period': period,
            'source': "synthetic-observation"}


def expect(params, unit, period, pr_inf, prev, curr):
    """Determine the expected value for a given infection probability.

    :param params: The observation model parameters.
    :param unit: The observation units (see classes in :py:module`data`).
    :type unit: str
    :param period: The duration of the observation period (in days).
    :type period: int
    :param pr_inf: The probability of an individual becoming infected during
        the observation period.
    :type pr_inf: float
    :param prev: The state vectors at the start of the observation period.
    :type prev: numpy.ndarray
    :param curr: The state vectors at the end of the observation period.
    :type curr: numpy.ndarray
    """
    if unit in params['obs']:
        op = params['obs'][unit]
        return op['expect_fn'](params, op, period, pr_inf, prev, curr)
    else:
        raise ValueError("Unknown observation type '{}'".format(unit))


def log_llhd(params, obs, curr, hist, weights):
    """Calculate the log-likelihood of obtaining one or more observations from
    each particle.

    :param params: The observation model parameters.
    :param obs: The list of observations for the current time-step.
    :param curr: The particle state vectors.
    :type curr: numpy.ndarray
    :param hist: The particle state histories, indexed by observation period.
    :type hist: dict(int, list(float))
    """
    log_llhd = np.zeros(curr.shape[:-1])
    pr_inf = params['model'].pr_inf

    hook_key = 'record_log_llhd_fns'
    hook_fns = params['epifx'][hook_key]

    for o in obs:
        # Extract the observation period and the infection probability.
        days = o['period']
        unit = o['unit']
        p_inf = np.maximum(pr_inf(hist[days], curr), 0)
        cpt_indiv = np.array([1 - p_inf, p_inf])

        if unit in params['obs']:
            op = params['obs'][unit]
            lgllhd = op['log_llhd_fn'](params, op, o, cpt_indiv, curr, hist)
            for hook_fn in hook_fns:
                hook_fn(o, lgllhd, weights)
            log_llhd += lgllhd
        else:
            raise ValueError("Unknown observation type '{}'".format(unit))

    return log_llhd


def datetime_conv(text, fmt='%Y-%m-%d', encoding='utf-8'):
    """
    Convert date strings to datetime.datetime instances. This is a
    convenience function intended for use with, e.g., ``numpy.loadtxt``.

    :param text: A string (bytes or Unicode) containing a date or date-time.
    :param fmt: A format string that defines the textual representation.
        See the Python ``strptime`` documentation for details.
    :param encoding: The byte string encoding (default is UTF-8).
    """
    # Note: text will always be read in as a byte string.
    text = pypfilt.text.to_unicode(text, encoding)
    return datetime.datetime.strptime(text, fmt)


def read_table(filename, columns, date_fmt=None, comment='#'):
    """
    Load data from a space-delimited **ASCII** text file with column headers
    defined in the first *non-comment* line.

    :param filename: The file to read.
    :param columns: The columns to read, represented as a list of
        ``(name, type)`` tuples; ``type`` should either be a built-in NumPy
        `scalar type <http://docs.scipy.org/doc/numpy-1.9.2/reference/arrays.scalars.html#arrays-scalars-built-in>`__,
        or ``datetime.date`` or ``datetime.datetime`` (in which case
        string values will be automatically converted to ``datetime.datetime``
        objects by :func:`~epifx.obs.datetime_conv`).
    :param date_fmt: A format string for parsing date columns; see
        :func:`datetime_conv` for details and the default format string.
    :param comment: Prefix string(s) that identify comment lines; either a
        single Unicode string or a *tuple* of Unicode strings.
    :return: A NumPy structured array.
    :raises ValueError: If the data file contains non-ASCII text (i.e., bytes
        greater than 127), because ``numpy.loadtxt`` cannot process non-ASCII
        data (e.g., see NumPy issues
        `#3184 <https://github.com/numpy/numpy/issues/3184>`__,
        `#4543 <https://github.com/numpy/numpy/issues/4543>`__,
        `#4600 <https://github.com/numpy/numpy/issues/4600>`__,
        `#4939 <https://github.com/numpy/numpy/issues/4939>`__).

    :Example:

    The code below demonstrates how to read observations from a file that
    includes columns for the year, the observation date, the observed value,
    and free-text metadata (up to 20 characters in length).

    ::

       import datetime
       import numpy as np
       import epifx.obs
       columns = [('year', np.int32), ('date', datetime.datetime),
                  ('count', np.int32), ('metadata', 'S20')]
       df = epifx.obs.read_table('my-data-file.ssv', columns,
                                 date_fmt='%Y-%m-%d')
    """
    if comment is None:
        comment = '#'
    skip_lines = 1
    with codecs.open(filename, encoding='ascii') as f:
        cols = f.readline().strip().split()
        while len(cols) == 0 or cols[0].startswith(comment):
            cols = f.readline().strip().split()
            skip_lines += 1

    req_cols = [col[0] for col in columns]
    for req in req_cols:
        if req not in cols:
            raise ValueError("Column '{}' not found in {}".format(
                req, filename))

    col_convs = {}
    col_types = pypfilt.summary.dtype_names_to_str(columns)
    for ix, col in enumerate(col_types):
        # Ensure that all column names are valid ASCII strings.
        try:
            pypfilt.text.to_bytes(col[0], encoding='ascii')
        except UnicodeEncodeError as e:
            raise ValueError("Column '{}' is not valid ASCII".format(col[0]))
        if isinstance(col[1], type) and issubclass(col[1], datetime.date):
            # Dates and datetimes must be converted from strings to objects.
            # Note: the opposite is true when *writing* tables!
            # This has implications for making the time units arbitrary, as
            # the time class will need to define both conversion operations.
            col_types[ix] = (col[0], 'O')
            col_ix = cols.index(col[0])
            if date_fmt is None:
                col_convs[col_ix] = lambda s: datetime_conv(s,
                                                            encoding='ascii')
            else:
                col_convs[col_ix] = lambda s: datetime_conv(s, date_fmt,
                                                            'ascii')
    col_read = [cols.index(name) for name in req_cols]

    with codecs.open(filename, encoding='ascii') as f:
        try:
            return np.loadtxt(f, skiprows=skip_lines, dtype=col_types,
                              converters=col_convs, usecols=col_read)
        except (TypeError, UnicodeDecodeError) as e:
            msg = "File '{}' contains non-ASCII text".format(filename)
            print(e)
            raise ValueError(msg)


class SampleCounts(object):
    """
    Generic observation model for relating disease incidence to count data
    where the denominator is reported.
    """

    def __init__(self, obs_unit, obs_period, k_obs_ix=None):
        """
        :param obs_unit: A descriptive name for the data.
        :param obs_period: The observation period (in days).
        :param k_obs_ix: The index of the model parameter that defines the
            disease-related increase in observation rate
            (:math:`\kappa_\mathrm{obs}`). By default, the value in the
            parameters dictionary is used.
        """
        self.unit = obs_unit
        self.period = obs_period
        self.k_obs_ix = k_obs_ix

    @staticmethod
    def logpmf(x, prob, size, disp):
        """
        Return the log of the probability mass at :math:`x`.

        :param x: The number of cases (observed numerator :math:`x`).
        :param prob: The expected fraction of all patients that are cases.
        :param size: The number of patients (observed denominator).
        :param disp: The dispersion parameter (:math:`k`).
        """
        return (gammaln(size + 1) - gammaln(x + 1) - gammaln(size - x + 1) -
                betaln(disp * (1 - prob), disp * prob) +
                betaln(size - x + disp * (1 - prob), x + disp * prob))

    @classmethod
    def interval_pmf(cls, x0, x1, prob, size, disp, log=True):
        """
        Return the (log of the) probability mass over the interval
        :math:`(x_0, x1]`.

        :param x0: The (exclusive) minimum number of cases (:math:`x_0`).
        :param x1: The (inclusive) maximum number of cases (:math:`x_1`).
        :param prob: The expected fraction of all patients that are cases.
        :param size: The number of patients (observed denominator).
        :param disp: The dispersion parameter (:math:`k`).
        :param log: Whether to return the log of the probability mass.
        """
        total = np.zeros(np.shape(prob))
        for x in range(x0 + 1, x1 + 1):
            total += np.exp(cls.logpmf(x, prob, size, disp))
        if log:
            # Handle particles with zero mass in this interval.
            total[total == 0.0] = np.finfo(total.dtype).tiny
            return np.log(total)
        return total

    @classmethod
    def logsf(cls, x, prob, size, disp):
        """
        Return the log of the survival function :math:`(1 - \mathrm{CDF}(x))`.

        :param x: The number of cases (observed numerator :math:`x`).
        :param prob: The expected fraction of all patients that are cases.
        :param size: The number of patients (observed denominator).
        :param disp: The dispersion parameter (:math:`k`).
        """
        total = np.ones(np.size(prob))
        for x in range(x + 1):
            total -= np.exp(cls.logpmf(x, prob, size, disp))
        # Handle particles with zero mass in this interval.
        total[total == 0.0] = np.finfo(total.dtype).tiny
        return np.log(total)

    def expect(self, params, op, period, pr_inf, prev, curr):
        """
        Calculate the expected observation value :math:`\mathbb{E}[y_t]` for
        every particle :math:`x_t`.
        """
        if self.k_obs_ix is None:
            k_obs = op['k_obs']
        else:
            # Each particle has its own observation probability.
            k_obs = curr[..., self.k_obs_ix]
        return op['bg_obs'] + pr_inf * k_obs

    def log_llhd(self, params, op, obs, pr_indiv, curr, hist):
        """
        Calculate the log-likelihood :math:`\mathcal{l}(y_t \mid x_t)` for the
        observation :math:`y_t` (``obs``) and every particle :math:`x_t`.

        If it is known (or suspected) that the observed value will increase in
        the future --- when ``obs['incomplete'] == True`` --- then the
        log-likehood :math:`\mathcal{l}(y > y_t \mid x_t)` is calculated
        instead (i.e., the log of the *survival function*).

        If an upper bound to this increase is also known (or estimated) ---
        when ``obs['upper_bound']`` is defined --- then the log-likelihood
        :math:`\mathcal{l}(y_u \ge y > y_t \mid x_t)` is calculated instead.
        """
        period = obs['period']
        pr = self.expect(params, op, period, pr_indiv[1], hist[period], curr)
        disp = op['disp']
        num = obs['numerator']
        denom = obs['denominator']
        if 'incomplete' in obs and obs['incomplete']:
            if 'upper_bound' in obs:
                # Calculate the log-likelihood over the interval from the
                # observed value to this upper bound.
                num_max = obs['upper_bound']
                return self.interval_pmf(num, num_max, pr, denom, disp)
            else:
                # Calculate the log-likelihood of observing a strictly greater
                # value than reported by this incomplete observation.
                return self.logsf(num, pr, denom, disp)
        # Calculate the log-likehood of the observed value.
        return self.logpmf(num, pr, denom, disp)

    def define_params(self, params, bg_obs, k_obs, disp):
        """
        Add observation model parameters to the simulation parameters.

        :param bg_obs: The background signal in the data
            (:math:`bg_\mathrm{obs}`).
        :param k_obs: The increase in observation rate due to infected
            individuals (:math:`\kappa_\mathrm{obs}`).
        :param disp: The dispersion parameter (:math:`k`).
        """
        params['obs'][self.unit] = {
            'expect_fn': self.expect,
            'log_llhd_fn': self.log_llhd,
            'bg_obs': bg_obs,
            'k_obs': k_obs,
            'disp': disp
        }

    def from_file(self, filename, year=None, date_col='to', value_col='cases',
                  denom_col='patients'):
        """
        Load count data from a space-delimited text file with column headers
        defined in the first line.

        Note that returned observation *values* represent the *fraction* of
        patients that were counted as cases, **not** the *absolute number* of
        cases.
        The number of cases and the number of patients are recorded under the
        ``'numerator'`` and ``'denominator'`` keys, respectively.

        :param filename: The file to read.
        :param year: Only returns observations for a specific year.
            The default behaviour is to return all recorded observations.
        :param date_col: The name of the observation date column.
        :param value_col: The name of the observation value column (reported
            as absolute values, **not** fractions).
        :param denom_col: The name of the observation denominator column.
        :return: A list of observations, ordered as per the original file.

        :raises ValueError: If a denominator or value is negative, or if the
            value exceeds the denominator.
        """
        year_col = 'year'
        cols = [(year_col, np.int32), (date_col, datetime.date),
                (value_col, np.int32), (denom_col, np.int32)]
        df = read_table(filename, cols)

        if year is not None:
            df = df[df['year'] == year]

        # Perform some basic validation checks.
        if np.any(df[denom_col] < 0):
            raise ValueError("Observation denominator is negative")
        elif np.any(df[value_col] < 0):
            raise ValueError("Observed value is negative")
        elif np.any(df[value_col] > df[denom_col]):
            raise ValueError("Observed value exceeds denominator")

        # Return observations with non-zero denominators.
        nrows = df.shape[0]
        return [{'date': df[date_col][i],
                 'value': df[value_col][i] / df[denom_col][i],
                 'numerator': df[value_col][i],
                 'denominator': df[denom_col][i],
                 'unit': self.unit,
                 'period': self.period,
                 'source': filename}
                for i in range(nrows) if df[denom_col][i] > 0 and
                df[value_col][i] > 0]


class PopnCounts(object):
    """
    Generic observation model for relating disease incidence to count data
    where the denominator is assumed or known to be the population size.
    """

    def __init__(self, obs_unit, obs_period, pr_obs_ix=None):
        """
        :param obs_unit: A descriptive name for the data.
        :param obs_period: The observation period (in days).
        :param pr_obs_ix: The index of the model parameter that defines the
            observation probability (:math:`p_\mathrm{obs}`). By default, the
            value in the parameters dictionary is used.
        """
        self.unit = obs_unit
        self.period = obs_period
        self.pr_obs_ix = pr_obs_ix

    def expect(self, params, op, period, pr_inf, prev, curr):
        """
        Calculate the expected observation value :math:`\mathbb{E}[y_t]` for
        every particle :math:`x_t`.
        """
        n = params['epifx']['popn_size']
        if self.pr_obs_ix is None:
            pr_obs = op['pr_obs']
        else:
            # Each particle has its own observation probability.
            pr_obs = curr[..., self.pr_obs_ix]
        return (1 - pr_inf) * op['bg_obs'] + pr_inf * pr_obs * n

    def log_llhd(self, params, op, obs, pr_indiv, curr, hist):
        """
        Calculate the log-likelihood :math:`\mathcal{l}(y_t \mid x_t)` for the
        observation :math:`y_t` (``obs``) and every particle :math:`x_t`.

        If it is known (or suspected) that the observed value will increase in
        the future --- when ``obs['incomplete'] == True`` --- then the
        log-likehood :math:`\mathcal{l}(y > y_t \mid x_t)` is calculated
        instead (i.e., the log of the *survival function*).

        If an upper bound to this increase is also known (or estimated) ---
        when ``obs['upper_bound']`` is defined --- then the log-likelihood
        :math:`\mathcal{l}(y_u \ge y > y_t \mid x_t)` is calculated instead.
        """
        period = obs['period']
        mu = self.expect(params, op, period, pr_indiv[1], hist[period], curr)
        nb_k = op['disp']
        nb_pr = nb_k / (nb_k + mu)
        nbinom = scipy.stats.nbinom(nb_k, nb_pr)
        if 'incomplete' in obs and obs['incomplete']:
            if 'upper_bound' in obs:
                # Calculate the likelihood over the interval from the observed
                # value to this upper bound, and return its logarithm.
                cdf_u = nbinom.cdf(obs['upper_bound'])
                cdf_l = nbinom.cdf(obs['value'])
                # Handle particles with zero mass in this interval.
                probs = cdf_u - cdf_l
                probs[probs == 0] = np.finfo(probs.dtype).tiny
                return np.log(probs)
            else:
                # Return the likelihood of observing a strictly greater value
                # than the value reported by this incomplete observation.
                return nbinom.logsf(obs['value'])
        return nbinom.logpmf(obs['value'])

    def define_params(self, params, bg_obs, pr_obs, disp):
        """
        Add observation model parameters to the simulation parameters.

        :param bg_obs: The background signal in the data
            (:math:`bg_\mathrm{obs}`).
        :param pr_obs: The probability of observing an infected individual
            (:math:`p_\mathrm{obs}`).
        :param disp: The dispersion parameter (:math:`k`).
        """
        params['obs'][self.unit] = {
            'expect_fn': self.expect,
            'log_llhd_fn': self.log_llhd,
            'bg_obs': bg_obs,
            'pr_obs': pr_obs,
            'disp': disp
        }

    def from_file(self, filename, year=None, date_col='to', value_col='count'):
        """
        Load count data from a space-delimited text file with column headers
        defined in the first line.

        :param filename: The file to read.
        :param year: Only returns observations for a specific year.
            The default behaviour is to return all recorded observations.
        :param date_col: The name of the observation date column.
        :param value_col: The name of the observation value column.
        :return: A list of observations, ordered as per the original file.
        """
        year_col = 'year'
        cols = [(year_col, np.int32), (date_col, datetime.date),
                (value_col, np.int32)]
        df = read_table(filename, cols)

        if year is not None:
            df = df[df['year'] == year]

        nrows = df.shape[0]
        return [{'date': df[date_col][i],
                 'value': df[value_col][i],
                 'unit': self.unit,
                 'period': self.period,
                 'source': filename}
                for i in range(nrows)]
