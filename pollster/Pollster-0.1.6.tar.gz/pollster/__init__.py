"""
Methods for accessing the HuffPost Pollster API. Documentation for this API
may be found at http://elections.huffingtonpost.com/pollster/api.
"""

__version__ = '0.1.6'

from .pollster import Pollster, Chart, Poll, PollsterException
