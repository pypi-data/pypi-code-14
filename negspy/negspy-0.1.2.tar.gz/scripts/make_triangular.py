#!/usr/bin/python

import sys
import argparse

from itertools import tee, izip

def main():
    parser = argparse.ArgumentParser(description="""
    
    python make_triangular.py

    Make sure that the coordinates passed in are triangular. Sorts the first two
    columns so that the resulting coordinates are triangular.

""")

    args = parser.parse_args()

    for line in sys.stdin:
        try:
            line_output = []
            line_parts = line.strip().split()

            if int(line_parts[0]) > int(line_parts[1]):
                out_parts = [line_parts[1], line_parts[0]] + line_parts[2:]
            else:
                out_parts = line_parts

            print "\t".join(out_parts)
            
        except KeyError as ke:
            print >>sys.stderr, "KeyError:", ke, line.strip()
    

if __name__ == '__main__':
    main()



