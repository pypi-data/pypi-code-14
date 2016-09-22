'''
Very simple scripts. But handy!
'''
import sys
import numpy


def stdin_numbers():
    '''
    Returns a vector of numbers passed into the script
    as stdin.
    '''
    return [float(x) for x in sys.stdin if len(x) > 1]


def mean():
    '''
    Average
    '''
    print numpy.mean(stdin_numbers())


def stddiv():
    '''
    Standard deviation
    '''
    print numpy.std(stdin_numbers())


def variance():
    '''
    Variance, or std div squared
    '''
    print numpy.var(stdin_numbers())


def median():
    '''
    Median -- the number in the middle
    '''
    print numpy.median(stdin_numbers())


def sumtotal():
    '''
    Grand total. Name was chosen to avoid namespace conflicts
    with other bash utilities
    '''
    print numpy.sum(stdin_numbers())
