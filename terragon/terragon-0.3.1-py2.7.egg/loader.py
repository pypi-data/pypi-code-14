import sys as sys
import time as time

import pickle
from six import string_types as string_types

from .terragon import loads_from_base64, loads_spark_from_base64, load_pom_from_base64

"""
the load_object function is used by the python kernel in ScienceOps to load_object
base64 encoded serialized objects into memory
"""
def load_object(name, base64_pickle, sc=None):

    pickle_error, terragon_error, spark_error, pom_error = "", "", "", ""
    strategies = []
    # "regular" pickle strategy
    try:
        strategies.append("pickle")
        if isinstance(base64_pickle, string_types):
            base64_pickle = base64_pickle.encode()
        return pickle.loads(base64_pickle)
    except Exception as e:
        pickle_error = e

    # terragon strategy
    try:
        strategies.append("terragon")
        return loads_from_base64(base64_pickle)
    except Exception as e:
        terragon_error = e

    # spark strategy
    if sc:
        try:
            strategies.append("spark")
            return loads_spark_from_base64(sc, base64_pickle)
        except Exception as e:
            spark_error = e

    # pomegranate strategy
    import pomegranate
    try:
        strategies.append("pomegranate")
        return load_pom_from_base64(base64_pickle)
    except Exception as e:
        pom_error = e

    sys.stderr.write("Attempted to load object %s using the following methods:\n")
    for strategy in strategies:
        sys.stderr.write("- %s\n" % strategy)
    sys.stderr.write("See stack traces below for more details:\n")

    if "pickle" in strategies:
        sys.stderr.write("pickle: %s\n" % pickle_error)
    if "terragon" in strategies:
        sys.stderr.write("terragon: %s\n" % terragon_error)
    if "spark" in strategies:
        sys.stderr.write("spark: %s\n" % spark_error)
    if "pomegranate" in strategies:
        sys.stderr.write("pomegranate: %s\n" % pom_error)
