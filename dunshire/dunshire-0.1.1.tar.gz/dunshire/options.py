"""
A place to collect the various options that "can be passed to the
underlying engine." Just kidding, they're constants and you can't
change them. But this makes the user interface real simple.
"""


ABS_TOL = 1e-6
"""
The absolute tolerance used in all "are these numbers equal" and "is
this number less than (or equal to) that other number" tests. The CVXOPT
default is ``1e-7``, but loosening that a little reduces the number of
"unknown" solutions that we get during random testing. Whether or not it
improves the solubility of real problems is a question for the
philosophers.
"""

DEBUG_FLOAT_FORMAT = '%.20f'
"""
The float output format to use when something goes wrong. If we need to
reproduce a random test case, for example, then we need all of the digits
of the things involved. If we try to recreate the problem using only,
say, the first seven digits of each number, then the resulting game
might not reproduce the failure.
"""

FLOAT_FORMAT = '%.7f'
"""
The default output format for floating point numbers.
"""
