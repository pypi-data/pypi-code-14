#!/usr/bin/env python

from __future__ import print_function
from colorama import *

init(autoreset=True)


################################################################################
results = {
    "total": 0,
    "bad": 0
}

# report
# NONE -> NONE
# produce pass or fail result
def reportResult():
    total = results["total"]
    bad = results["bad"]
    passed = total - bad
    if (passed <= 1 and total <= 1):
        print(Fore.YELLOW + "Of " + str(total) + " tests run, " + str(bad) +
              " failed, and " + str(passed) + " passed.")
    else:
        print(Fore.GREEN + "Of " + str(total) + " tests, " + str(bad) +
              " failed, " + str(passed) + " passed.")
    print(Style.RESET_ALL)


# checkExpect
# object param object string -> NONE
# produce pass or fail when the input function under test is invoked using
# param and expected value
# param can be of any data type
# expected value can be of any data type
def checkExpect(f, a, expected, name=None):
    results['total'] += 1
    result = f(a)
    if (name is not None):
        print(Fore.WHITE + "> for unit test: " + name)
    else:
        print(Fore.WHITE + "> for unit test: " + "unknown test")

    if (result != expected):
        results['bad'] += 1
        print(Fore.RED + "Expected " + str(expected) + ", but was " + str(result))

    reportResult()