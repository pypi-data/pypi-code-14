import random

from adaptivepy.monitor.primitives import Monitor


def create_fixed_monitor(value):
    m = Monitor()
    m.value = lambda: value
    m.possible_values = lambda: {value}
    return m


def create_random_monitor(possible_values):
    """
    :type possible_values: set
    :rtype: Monitor
    """
    m = Monitor()
    possible_values_copy = possible_values.copy()
    m.value = lambda: random.sample(possible_values_copy, 1)[0]
    m.possible_values = lambda: possible_values_copy
    return m
