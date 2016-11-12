#!/usr/bin/python3

import listdownloader
import argparse
from itertools import islice

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, dest="filepath", default="",
                        help="Text file that contains links to download, line by line", required=True)
    parser.add_argument("-d", "--destination", type=str, dest="dest", default="",
                        help="Destination path to download the files", required=True)
    parser.add_argument("-t", "--threads", type=int, dest="threads", default=0,
                        help="Number of threads/processes to be used")
    parser.add_argument("-l", "--lines", type=int, dest="numlines", default=0,
                        help="Number of lines to be read as a chunk. 0=Read the whole file.")
    args = parser.parse_args()

    if args.numlines <= 0: # load the whole file
        with open(args.filepath) as f:
            file_lines = f.readlines()
            listdownloader.download_files(file_lines, args.dest, args.threads)

    else: # load parts of the file
        with open(args.filepath, 'r') as infile:
            while True:
                file_lines = list(islice(infile, args.numlines))
                if len(file_lines) > 0:
                    print(file_lines)
                    listdownloader.download_files(file_lines, args.dest, args.threads)
                else:
                    break
