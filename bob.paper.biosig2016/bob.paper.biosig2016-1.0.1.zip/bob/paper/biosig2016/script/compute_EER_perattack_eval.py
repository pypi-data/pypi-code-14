#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <Pavel.Korshunov@idiap.ch>
# Hannah Muckenhirn <hannah.muckenhirn@idiap.ch>
# Thu  21 Jan 13:56:21 CEST 2016
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Preprocessing audio files from AVspoof 2015 database
Installation of Bob toolbox is required
"""

import bob.measure

import sys
import os
import argparse

import os.path

import numpy
from bob.db.asvspoof.query import Database

# setup logging
import bob.core
logger = bob.core.log.setup("bob.paper.biosig2016")


def read_attack_scores(objects, attack_file):
    positives = []
    names = []
    scores = []
    for (client_id, probe_id, filename, score) in bob.measure.load.four_column(attack_file):
        names.append(filename)
        scores.append(score)

    for obj in objects:
        if obj.is_real():
            raise ValueError('The object of the database should be an attack but it is real!')
        sample_name = str(obj.make_path())
        try:
          idx = names.index(sample_name)
          positives.append(scores[idx])
        except ValueError:
          pass

    return numpy.array(positives, numpy.float64)


def main(command_line_parameters=None):

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    OUTPUT_DIR = os.path.join(basedir, 'plots')

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
    parser.add_argument('-d', '--real-file', required=True, help="The score file with real accesses scores of the evaluation set.")
    parser.add_argument('-t', '--attack-file', type=str, required=True, help="The score file with attacks scores of the evaluation set.")
    parser.add_argument('-o', '--out-directory', dest="directory", default=OUTPUT_DIR,
                        help="This path will be prepended to every file output by this procedure (defaults to '%(default)s')")

    # add verbose option
    bob.core.log.add_command_line_option(parser)
    args = parser.parse_args()
    # set verbosity level
    bob.core.log.set_verbosity_level(logger, args.verbose)

    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    # Querying the database
    db = Database()
    scores_attack_set = []
    attack_names = ('S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10')
    for attack in attack_names:
        print ('Processing attack %s' % attack)
        attackObjects = db.objects(purposes='attack', support=attack, groups='eval', protocol='CM')
        scores_attack = read_attack_scores(attackObjects, args.attack_file)
        scores_attack_set.append(scores_attack)

    eers = []
    resfile = open(os.path.join(args.directory, 'eval_results.txt'), "w")

    print("Loading %s real score file of the evaluation set" % (args.real_file))
    scores_zimp, scores_real = bob.measure.load.split_four_column(args.real_file)
    for attack, scores_attack in zip(attack_names, scores_attack_set):
        eer_threshold = bob.measure.eer_threshold(scores_attack, scores_real)
        far, frr = bob.measure.farfrr(scores_attack, scores_real, eer_threshold)
        eer = (far + frr) / 2 * 100
        eers.append(eer)
        print("Evaluation set, attack: %s, stats: FAR = %2.6f \t FRR = %2.6f \t EER = %2.6f%% \t EER threshold = %2.6f" %
              (attack, far, frr, eer, eer_threshold))
        resfile.write("%s & %2.6f & %2.6f \\\\ \\hline \n" %
                      (attack, eer_threshold, eer))
    eers = numpy.asarray(eers)
    print ('Average EER of all attacks: %f%%' % numpy.mean(eers))
    resfile.write("Average over known & & %2.6f \\\\ \\hline \n" % (numpy.mean(eers[0:5])))
    resfile.write("Average over unknown & & %2.6f \\\\ \\hline \n" % (numpy.mean(eers[5:10])))
    resfile.write("Average & & %2.6f \\\\ \\hline \n" % (numpy.mean(eers)))
    resfile.close()


if __name__ == '__main__':
    main()
