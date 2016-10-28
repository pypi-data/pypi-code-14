import pandas as pd
import logging


def helloproject():
    print pd.date_range('20130101', periods=6)
    print "Hello python"


def dounittest():
    logging.warning('Do a simple function for unittest')
    return 100
