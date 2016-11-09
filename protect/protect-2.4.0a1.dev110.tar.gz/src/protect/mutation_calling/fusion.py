#!/usr/bin/env python2.7
# Copyright 2016 Arjun Arkal Rao
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function
import os
import csv
from math import ceil
from bd2k.util.expando import Expando
from protect.common import get_files_from_filestore, docker_call, export_results, untargz


def run_fusion_caller(job, star_bam, univ_options, fusion_options):
    """
    This module will run a fusion caller on DNA bams.  This module will be
    implemented in the future.

    This module corresponds to node 10 on the tree
    """
    job.fileStore.logToMaster('Running FUSION on %s' % univ_options['patient'])
    job.fileStore.logToMaster('Fusions are currently unsupported.... Skipping.')
    fusion_file = job.fileStore.getLocalTempFile()
    output_file = job.fileStore.writeGlobalFile(fusion_file)
    return output_file


def ericscript_disk(rna_fastqs):
    return int(2 * ceil(sum([f.size for f in rna_fastqs]) + 524288) + 9019431322)


def run_ericscript(job, fastqs, univ_options, ericscript_options):
    """
    Runs EricScript on tumor Rna-seq reads

    ARGUMENTS
    1. fastqs: Tuple for paired RNA-seq reads
        fastqs
            |- ('tumor_rna.1.fq': <JSid>, 'tumor_rna.2.fq1': <JSid>)
    2. univ_options: Dict of universal arguments used by almost all tools
         univ_options
                +- 'java_Xmx': <java memory usage>
    3. ericscript_options: Dict of parameters specific to EricScript
         ericscript_options
              |- 'database.tar.gz': <JSid for the EricScript database tarball>
              +- 'n': <number of threads to allocate>

    RETURN VALUES
    1. EricScript filtered fusion calls <JSid>
    """
    job.fileStore.logToMaster('Running EricScript on %s' % univ_options['patient'])
    work_dir = job.fileStore.getLocalTempDir()
    input_files = {'rna_1.fq': fastqs[0],
                   'rna_2.fq': fastqs[1],
                   'tool_index.tar.gz': ericscript_options['tool_index']}

    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)
    input_files['tool_index'] = untargz(input_files['tool_index.tar.gz'], work_dir)
    input_files['tool_index'] = os.path.basename(input_files['tool_index'])

    cores = ericscript_options['n']
    parameters = ['-db', input_files['tool_index'],
                  '-o', '/data/output',
                  '-name', 'fusions',
                  '-p', str(cores),
                  'rna_1.fq', 'rna_2.fq']

    docker_call(tool='ericscript:0.5.5--065b274e9eb4bfb4fbe26a100e9c64ce7c1b735d',
                tool_parameters=parameters, work_dir=work_dir, dockerhub='jpfeil')

    output_path = os.path.join(work_dir, 'output/fusions.results.filtered.tsv')
    filtered_fusions = job.fileStore.writeGlobalFile(output_path)
    export_results(job, output_path, univ_options, subfolder='mutations/ericscript')
    return job.addChildJobFn(reformat_ericscript_output, filtered_fusions, univ_options).rv()


def parse_ericscript(infile):
    """
    Parses EricScript format and returns an Expando object with basic features
    """
    reader = csv.reader(infile, delimiter='\t')
    header = reader.next()
    header = {key: index for index, key in enumerate(header)}

    eric_features = ['GeneName1', 'EnsemblGene1', 'strand1', 'chr1',
                     'GeneName2', 'EnsemblGene2', 'strand2', 'chr2',
                     'Breakpoint1', 'Breakpoint2',
                     'spanningreads', 'crossingreads', 'JunctionSequence']

    for line in reader:
        yield Expando(dict((feature, line[header[feature]]) for feature in eric_features))


def reformat_ericscript_output(job, fusion_file, univ_options):
    """
    Writes EricScript results in Transgene BEDPE format
    """
    job.fileStore.logToMaster('Reformatting EricScript output for %s' % univ_options['patient'])

    # Import EricScript results
    input_files = {'results.tsv': fusion_file}
    work_dir = job.fileStore.getLocalTempDir()
    input_files = get_files_from_filestore(job, input_files, work_dir, docker=False)

    # Header for BEDPE file
    header = ['# chr1', 'start1', 'end1',
              'chr2', 'start2', 'end2',
              'name', 'score',
              'strand1', 'strand2',
              'junctionSeq1', 'junctionSeq2',
              'hugo1', 'hugo2']

    output_path = os.path.join(work_dir, 'ericscript_results.bedpe')
    with open(input_files['results.tsv'], 'r') as in_f, open(output_path, 'w') as out_f:
        writer = csv.writer(out_f, delimiter='\t')
        writer.writerow(header)
        for record in parse_ericscript(in_f):
            # If EricScript could not find the breakpoint, then set the value to unknown
            if record.Breakpoint1 == 'Unable to predict breakpoint position':
                record.Breakpoint1 = '.'

            if record.Breakpoint2 == 'Unable to predict breakpoint position':
                record.Breakpoint2 = '.'

            # With EricScript the lowercase letters are from the donor sequence and the uppercase
            # letters are from the acceptor sequence.
            five_prime_seq = ''.join([base.upper() for base in record.JunctionSequence if base.islower()])
            three_prime_seq = ''.join([base for base in record.JunctionSequence if base.isupper()])

            writer.writerow([record.chr1,
                             '.',   # Donor start position is not necessary
                             record.Breakpoint1,
                             record.chr2,
                             record.Breakpoint2,
                             '.',   # Acceptor end position is not necessary
                             '-'.join([record.EnsemblGene1, record.EnsemblGene2]),
                             '0',
                             record.strand1,
                             record.strand2,
                             five_prime_seq,
                             three_prime_seq,
                             record.GeneName1,
                             record.GeneName2])

    return job.fileStore.writeGlobalFile(output_path)
