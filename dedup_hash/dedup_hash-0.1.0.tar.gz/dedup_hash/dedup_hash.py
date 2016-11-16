import argparse
import gzip
import io
from cityhash import CityHash64
from itertools import (
    cycle, izip
)


class UniqueFastqPairs(object):
    def __init__(self, r1_infile, r2_infile, r1_outfile, r2_outfile, write_gzip, buffer_size=32768, compresslevel=6):
        self.seen_hashes = set()
        self.r1_infile = r1_infile
        self.r2_infile = r2_infile
        self.r1_outfile = r1_outfile
        self.r2_outfile = r2_outfile
        self.write_gzip = write_gzip
        self.buffer_size = buffer_size
        self.compresslevel = compresslevel
        self.cur_fastq_str_r1 = ""
        self.cur_fastq_str_r2 = ""
        self.cur_uniq = False
        self.fastq_cycle = cycle([self.header_one_action, self.seq_action, self.header_two_action, self.qual_action])
        self.r1, self.r2 = self.get_input()
        self.r1_out, self.r2_out = self.get_output()
        self.process_files()
        self.close_io()

    def get_input(self):
        if self.is_gzip():
            return io.BufferedReader(gzip.GzipFile(self.r1_infile, 'rb'), buffer_size=self.buffer_size), io.BufferedReader(gzip.GzipFile(self.r2_infile, 'rb'), buffer_size=self.buffer_size)
        return open(self.r1_infile), open(self.r2_infile)

    def get_output(self):
        if self.write_gzip:
            return io.BufferedWriter(gzip.GzipFile(self.r1_outfile, 'wb', compresslevel=self.compresslevel), buffer_size=self.buffer_size), io.BufferedWriter(gzip.GzipFile(self.r2_outfile, 'wb', compresslevel=self.compresslevel), buffer_size=self.buffer_size)
        return open(self.r1_outfile, 'w'), open(self.r2_outfile, 'w')

    def close_io(self):
        self.r1.close()
        self.r2.close()
        self.r1_out.close()
        self.r2_out.close()

    def is_gzip(self):
        gzip_magic_byte = b"\x1f\x8b\x08"
        with open(self.r1_infile) as input:
            return gzip_magic_byte == input.read(len(gzip_magic_byte))

    def process_files(self):
        for fastq_item, r1_line, r2_line in izip(self.fastq_cycle, self.r1, self.r2):
            fastq_item(r1_line, r2_line)

    def seq_action(self, r1_line, r2_line):
        cur_hash = CityHash64(r1_line + r2_line)
        if cur_hash in self.seen_hashes:
            self.cur_uniq = False
        else:
            self.seen_hashes.add(cur_hash)
            self.cur_uniq = True
            self.cur_fastq_str_r1 = "".join((self.cur_fastq_str_r1, r1_line))
            self.cur_fastq_str_r2 = "".join((self.cur_fastq_str_r2, r2_line))

    def header_one_action(self, r1_line, r2_line):
        self.cur_uniq = False
        self.cur_fastq_str_r1 = r1_line
        self.cur_fastq_str_r2 = r2_line

    def header_two_action(self, r1_line, r2_line):
        self.cur_fastq_str_r1 = "".join((self.cur_fastq_str_r1, r1_line))
        self.cur_fastq_str_r2 = "".join((self.cur_fastq_str_r2, r2_line))

    def qual_action(self, r1_line, r2_line):
        if self.cur_uniq:
            self.cur_fastq_str_r1 = "".join((self.cur_fastq_str_r1, r1_line))
            self.cur_fastq_str_r2 = "".join((self.cur_fastq_str_r2, r2_line))
            self.r1_out.write(self.cur_fastq_str_r1)
            self.r2_out.write(self.cur_fastq_str_r2)


def get_args():
    parser = argparse.ArgumentParser(description='Get unique reads from fastq files')
    parser.add_argument('r1_in', help='Read1 input fastq file')
    parser.add_argument('r2_in', help='Read2 input fastq file')
    parser.add_argument('r1_out', help='Read1 output fastq file')
    parser.add_argument('r2_out', help='Read2 output fastq file')
    parser.add_argument('--write_gzip', action='store_true', help="Compress output in gzip format?")
    parser.add_argument('--buffer_size', default=32768, type=int, help="Set buffer size for reading gzip files")
    parser.add_argument('--compresslevel', default=2, type=int, choices=list(range(1, 10)), help="Set compression level (1: fastest, 9: highest compression)")
    return parser.parse_args()


def main():
    args = get_args()
    UniqueFastqPairs(r1_infile=args.r1_in,
                     r2_infile=args.r2_in,
                     r1_outfile=args.r1_out,
                     r2_outfile=args.r2_out,
                     write_gzip=args.write_gzip,
                     buffer_size=args.buffer_size,
                     compresslevel=args.compresslevel)


if __name__ == '__main__':
    main()
