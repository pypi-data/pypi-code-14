#!/usr/bin/python
# -*- coding: ascii -*-
"""
"""

import os
import sys
import time

def main():
    """
    """
    input_file = sys.argv[1]
    file_d = file(input_file, "r")
    input_lines = file_d.readlines()

    for input_line in input_lines:
        print input_line.strip()
        #time.sleep(3.0)

if __name__ == "__main__":
  """
  """
  sys.exit( main() )
