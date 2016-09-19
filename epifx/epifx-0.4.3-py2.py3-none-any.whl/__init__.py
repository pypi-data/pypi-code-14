"""Epidemic forecasts using disease surveillance data."""

from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import datetime
import logging
import numpy as np
import pypfilt

import epifx.model
import epifx.obs
import epifx.summary

__package_name__ = u'epifx'
__author__ = u'Rob Moss'
__email__ = u'rgmoss@unimelb.edu.au'
__copyright__ = u'2014-2016, Rob Moss'
__license__ = u'BSD 3-Clause License'
__version__ = u'0.4.3'


SEIR = epifx.model.SEIR

# Prevent an error message if the application does not configure logging.
log = logging.getLogger(__name__).addHandler(logging.NullHandler())


def default_params(p_exp, px_scale, model=SEIR):
    """The default simulation parameters.

    :param p_exp: The daily probability of seeding an exposure event in a
        naive population.
    :param px_scale: The ratio of particles to seeded exposures.
    :param model: The infection model.
    """
    # Calculate the required number of particles.
    px_count = int(np.ceil(px_scale / p_exp))
    # Enforce a minimal history matrix.
    params = pypfilt.default_params(model, max_days=7, px_count=px_count)
    # The observation model.
    params['log_llhd_fn'] = epifx.obs.log_llhd

    # Model-specific parameters.
    params['epifx'] = {
        # The daily probability of seeding an exposure event.
        'p_exp': p_exp,
        # The ratio of particles to the seeding probability.
        'px_scale': px_scale,
        # The metropolitan Melbourne population.
        'popn_size': 4108541,
        # Allow stochastic variation in model parameters and state variables.
        'stoch': True,
        # Use the default pypfilt PRNG seed, whatever that might be.
        'prng_seed': params['resample']['prng_seed'],
        # Use an independent PRNG instance by default.
        'independent_prng': True,
        # Provide a hook for functions to record log-likelihoods before the
        # particles weights are adjusted and any resampling takes place.
        'record_log_llhd_fns': [],
    }

    # Construct the default PRNG object.
    params['epifx']['rnd'] = np.random.RandomState(
        params['epifx']['prng_seed'])

    # Observation model parameters.
    params['obs'] = {}

    return params


def init_prng(params, seed):
    """Initialise the ``epifx`` PRNG instance (``params['epifx']['rnd']``).

    :param params: The simulation parameters.
    :param seed: The PRNG seed; see the ``numpy.random.RandomState``
        documentation for details.
    """
    params['epifx']['prng_seed'] = seed
    params['epifx']['rnd'] = np.random.RandomState(seed)


def daily_forcing(filename, date_fmt='%Y-%m-%d'):
    """Return a temporal forcing look-up function, which should be stored in
    ``params['epifx']['forcing']`` in order to enable temporal forcing.

    :param filename: A file that contains two columns separated by whitespace,
        the column first being the date and the second being the force of the
        temporal modulation.
        Note that the first line of this file is assumed to contain column
        headings and will be **ignored**.
    :param date_fmt: The format in which dates are stored.
    """

    def _date_col(text, fmt='%Y-%m-%d'):
        """Convert date strings to datetime.date instances."""
        text = pypfilt.text.to_unicode(text)
        return datetime.datetime.strptime(text, fmt).date()

    col_types = [('Date', datetime.date), ('Force', np.float)]
    df = epifx.obs.read_table(filename, col_types)

    def forcing(when):
        """Return the (daily) temporal forcing factor."""
        today = when.date()
        if when.hour == when.minute == 0:
            # The time-step covered the final portion of the previous day.
            today = today - datetime.timedelta(days=1)
        return df['Force'][df['Date'] == today][0]

    return forcing
