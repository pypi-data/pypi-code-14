# -*- coding: utf-8 -*-
from time import time


PROJECTNAME = 'collective.feedaggregator'

# profiling
INMEDIATE_PROFILING = True  # print profiling results after each call

# caching
TTL = str(time() // (60 * 15))  # feed entries are cached for 15 minutes
