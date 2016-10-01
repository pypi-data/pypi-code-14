import logging
import os
from commands import getstatusoutput

__author__ = 'Michael'

TEST_PY2 = True
TEST_PY3 = True

TEST_IGNORE = {
    __file__,
    "getch_test.py"
}


def listdir():
    return [
        fname for fname in os.listdir(".")
        if fname.endswith(".py") and fname not in TEST_IGNORE
        ]


def test(py_ver, fname):
    stat, out = getstatusoutput("python{} {}".format(py_ver, fname))
    if stat:
        logging.error("Script {} failed with Python {}".format(fname, py_ver))


if __name__ == '__main__':
    for fname in listdir():
        if TEST_PY2:
            test(2, fname)
        if TEST_PY3:
            test(3, fname)
