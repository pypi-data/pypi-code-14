#!/usr/bin/env python
# coding: utf-8
import csv
import sys
import glob
import struct
import logging
import argparse

from os import path, getcwd, makedirs, remove

from dbfread import DBF


def write_row(writer, row, charset):
    writer.writerow([cell.encode(charset) for cell in row])


def main():
    sys.tracebacklimit = 0

    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default=getcwd(),
                        help="input directory with *.dbf files")
    parser.add_argument("-o", "--output", default=getcwd(),
                        help="output directory for save *.csv files")
    parser.add_argument("-f", "--from-charset", default="cp850",
                        help="charset of *.dbf files (default: cp850)")
    parser.add_argument("-t", "--to-charset", default="utf8",
                        help="charset of *.csv files (default: utf8)")
    args = parser.parse_args()
    input_files = glob.glob('{}/*.dbf'.format(args.input))

    if not input_files:
        log.info("Not found *.dbf files in directory: {}\n".format(args.input))
        exit(0)

    for input_file_path in input_files:
        output_file_path = "{}/{}.csv".format(
            args.output,
            path.splitext(path.basename(input_file_path))[0]
        )
        if args.output != args.input:
            if not path.exists(args.output):
                makedirs(args.output)

        with open(output_file_path, 'wb') as output_file:
            log.info("{} -> {}".format(input_file_path, output_file_path))
            output_writer = csv.writer(output_file)

            try:
                input_reader = DBF(input_file_path, encoding=args.from_charset)

                write_row(output_writer, input_reader.field_names, args.to_charset)
                for record in input_reader:
                    write_row(output_writer, record.values(), args.to_charset)

            except UnicodeDecodeError:
                log.error("Error: Wrong input charset: {}\n".format(
                    args.from_charset))
                remove(output_file_path)
            except UnicodeEncodeError:
                log.error("Error: Can't encode to output charset: {}\n".format(
                    args.to_charset))
                remove(output_file_path)
            except LookupError:
                log.error("Error: Unknown output charset: {}\n".format(
                    args.to_charset))
                remove(output_file_path)
                exit(0)
            except struct.error:
                log.error("Error: Bad input file format: {}\n".format(
                    path.basename(input_file_path))
                )
                remove(output_file_path)
                continue
            else:
                log.info("OK\n")

if __name__ == "__main__":
    main()