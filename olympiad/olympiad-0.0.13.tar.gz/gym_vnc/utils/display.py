# -*- coding: utf-8 -*-

import numpy as np

def display_timestamps_pair_max(time_m_2, flat=True):
    if flat:
        # Ignore empty inputs, which happens when environments are resetting.
        time_m_2 = [[x for x in time_m_2 if len(x)]]

    if len(time_m_2) == 0:
        return '(empty)'

    # We concatenate the (min, max) lags from a variety of runs. Those
    # runs may have different lengths.
    time_m_2 = [np.array(m) for m in time_m_2]

    return [display_timestamps_sigma(m[:, 1]) if len(m) > 0 else None for m in time_m_2]

def display_timestamps_pair_compact(time_m_2):
    """Takes a list of the following form: [(a1, b1), (a2, b2), ...] and
    returns a string a_mean-b_mean, flooring out at 0.
    """
    if len(time_m_2) == 0:
        return '(empty)'

    time_m_2 = np.array(time_m_2)

    low = time_m_2[:, 0].mean()
    high = time_m_2[:, 1].mean()

    low = max(low, 0)

    # Not sure if this'll always be true, and not worth crashing over
    if high < 0:
        logger.warn('Harmless warning: upper-bound on clock skew is negative: (%s, %s). Please let Greg know about this.', low, high)

    return '{}-{}'.format(display_timestamp(low), display_timestamp(high))

def display_timestamps_pair(time_m_2):
    """Takes a list of the following form: [(a1, b1), (a2, b2), ...] and
    returns a string (a_mean+/-a_error, b_mean+/-b_error).
    """
    if len(time_m_2) == 0:
        return '(empty)'

    time_m_2 = np.array(time_m_2)
    return '({}, {})'.format(
        display_timestamps(time_m_2[:, 0]),
        display_timestamps(time_m_2[:, 1]),
    )

def display_timestamps_sigma(time_m):
    if len(time_m) == 0:
        return '(empty)'

    mean = np.mean(time_m)
    std = standard_error(time_m)
    scale, units = pick_time_units(mean)
    return '{:.2f}{}±{:.2f}{}'.format(mean * scale, units, std * scale, units)

def display_timestamps(time_m):
    if len(time_m) == 0:
        return '(empty)'

    mean = np.mean(time_m)
    std = standard_error(time_m)
    return '{}±{}'.format(display_timestamp(mean), display_timestamp(std))

def display_timestamps_n(time_m):
    # concatenate all the n's timesteps together, then display_timestamps on it
    return display_timestamps(np.concatenate(time_m))

def standard_error(ary, axis=0):
    if len(ary) > 1:
        return np.std(ary, axis=axis) / np.sqrt(len(ary) - 1)
    else:
        return np.std(ary, axis=axis)

def display_timestamp(time):
    assert not isinstance(time, np.ndarray), 'Invalid scalar: {}'.format(time)
    scale, units = pick_time_units(time)
    return '{:.2f}{}'.format(time * scale, units)

def pick_time_units(time):
    assert not isinstance(time, np.ndarray), 'Invalid scalar: {}'.format(time)
    if abs(time) < 1:
        return 1000, 'ms'
    else:
        return 1, 's'
