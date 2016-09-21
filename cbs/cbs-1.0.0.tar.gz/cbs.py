#!/usr/bin/env python3
import h5py
import argparse
import subprocess
import numpy as np

from multiprocessing import Process, Pipe


def mpileup(filename):
    p = subprocess.Popen(["samtools", "mpileup", filename], stdout=subprocess.PIPE)
    return (tuple(line.decode("utf-8").split("\t")[0:4]) for line in p.stdout)


def gather(filenames):
    oldchr = None
    pileups = [mpileup(filename) for filename in filenames]
    heads = [next(p) for p in pileups]
    while any(heads):
        min_position = min(enumerate(heads), key=lambda p: (p[1].chr != oldchr, int(p[1].pos)))[0]
        yield heads[min_position]
        oldchr = heads[min_position].chr
        heads[min_position] = next(pileups[min_position])
        if heads[min_position] is None:
            del heads[min_position]
            del pileups[min_position]


def generate_row(min_cov, chrom, pos, typ, count, oldpos, oldchr):
    val = None
    if oldchr and oldchr != chrom:
        val = (oldchr, oldpos+1, 0)
        oldchr = chrom
        oldpos = 0
    if oldpos >= int(pos) - 1:
        oldpos = int(pos)
        oldchr = chrom
    else:
        val = (chrom, oldpos+1, int(pos))
        oldpos = int(pos)
        oldchr = chrom
    return oldchr, oldpos, val


def get_blind_spots(filenames, min_cov, pipe):
    oldpos = 0
    oldchr = None
    gfunc, gargs = (gather, filenames) if len(filenames) != 1 else (mpileup, filenames[0])
    for chrom, pos, typ, count in gfunc(gargs):
        if(int(count) < min_cov):
            continue
        oldchr, oldpos, val = generate_row(min_cov, chrom, pos, typ, count, oldpos, oldchr)
        if val:
            pipe.send(val)
    pipe.send(None)
    pipe.close()


def write_h5(filename, pipe):
    outputfile = h5py.File(filename, "w")
    oldchrom = ""
    dataset = None
    b = pipe.recv()
    while b is not None:
        chrom, first, last = b
        if chrom != oldchrom:
            print(chrom)
            grp = outputfile.create_group(chrom)
            dataset = grp.create_dataset("missing_cov", (0, 2), maxshape=(None, 2), dtype='uint32')
            oldchrom = chrom
        row, col = dataset.shape
        dataset.resize(row+1, 0)
        dataset[row] = np.array([first, last])
        b = pipe.recv()
    pipe.close()


def main():
    parser = argparse.ArgumentParser(description='Coverage tool')
    parser.add_argument('files', nargs="+", help='BAM files')
    parser.add_argument('--min-cov', "-m", help='Minimal coverage', default=0, type=int)
    parser.add_argument('output', help='Outputfile')

    args = parser.parse_args()

    parentpipe, childpipe = Pipe()
    read_process = Process(target=get_blind_spots, args=(args.files, args.min_cov, parentpipe))
    write_process = Process(target=write_h5, args=(args.output, childpipe))
    read_process.start()
    write_process.start()
    read_process.join()
    write_process.join()

if __name__ == "__main__":
    main()
