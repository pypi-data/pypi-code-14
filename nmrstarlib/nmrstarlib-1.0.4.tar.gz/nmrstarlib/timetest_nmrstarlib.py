#!/usr/bin/env python3

import sys
import os
import time
from . import nmrstarlib

def reading_timetest(dirpath):
    starfiles_dir_path = os.path.abspath(dirpath)
    print("Reading from {}".format(starfiles_dir_path))

    filenames = os.listdir(starfiles_dir_path)
    print("Found {} files".format(len(filenames)))

    ta = time.time()
    print("START:\r\t\t", ta)

    for i, f in enumerate(filenames):
        fta = time.time()
        try:
            sfg = nmrstarlib.read_files([os.path.join(starfiles_dir_path, f)])
            sf = next(sfg)
            ftb = time.time()
            print("OKAY\t" + f + "\t", ftb - fta, "\t", i)
        except KeyboardInterrupt:
            exit()
        except:
            ftb = time.time()
            print("FAIL\t" + f + "\t", ftb - fta, "\t", i)

    tb = time.time()
    print("END:\r\t\t", tb)
    print("Files read in {} seconds".format(tb - ta))

if __name__ == "__main__":
    # python3 -m nmrstarlib.timetest ../AutomatedAnalysisMASSSNMR/bmrbscraper/NMR-STAR3

    script = sys.argv.pop(0)
    starfiles_dir_path = sys.argv.pop(0)

    reading_timetest(starfiles_dir_path)
