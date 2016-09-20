#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Artur Costa-Pazo <acosta@gradiant.org>
# Tue Nov 10 10:41:56 2015 +0100
#
# Copyright  (C) 2016 Gradiant, Vigo, Spain

""" Generates the results of the paper "The Replay-Mobile face presentation-attack database"
"""

import os
import sys
import argparse
import numpy
from antispoofing.utils.db import *
#from . import helpers
#from bob.paper.biosig2016_replaymobile import helpers
import evaluation as ev
import scoresReplayMobile as srm

def main(command_line_parameters=None):
    #Parser implementation
    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    INPUT_DIR = os.path.join(basedir, 'scores')
    OUTPUT_DIR = os.path.join(basedir, 'result')

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input', dest='scores_directory', default=INPUT_DIR, help="Folder with the scores (defaults to '%(default)s')")
    parser.add_argument('-o', '--output', dest='result_directory', default=OUTPUT_DIR, help="Result folder (defaults to '%(default)s')")

    args = parser.parse_args(command_line_parameters)

    result_directory = args.result_directory
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    #######
    # Database especific configuration
    #######
    #Database.create_parser(parser, implements_any_of='video')

#    args = parser.parse_args()
    #db = bob.db.replaymobile.Database()
    print args.scores_directory


    ## Performance Gabor (APCER and NPCER) #####################################################################################################
    ############################################################################################################################################
    sys.stdout.write("Calculate performance (APCER and BPCER)...\n")

  
#    scores_idiap = helpers.ScoresReplayMobile()
    scores_idiap = srm.ScoresReplayMobile()
    scores_idiap.label = 'idiap (IQM)'
    scores_idiap.load(args.scores_directory + "/replaymobile_IqmScores_SVM.hdf5")
    scores_idiap.purgeNaN()
    print scores_idiap

    #scores_gradiant_gabor_svm_linear =  helpers.ScoresReplayMobile()
    #scores_gradiant_gabor_svm_linear.label = 'gabor (linear)'
    #scores_gradiant_gabor_svm_linear.load(args.scores_directory + "/replaymobile_scores_gabor_factor6_SVM_LINEAL.hdf5")
    #scores_gradiant_gabor_svm_linear.purgeNaN()
    #print scores_gradiant_gabor_svm_linear

#    scores_gradiant_gabor_svm_rbf =  helpers.ScoresReplayMobile()
    scores_gradiant_gabor_svm_rbf =  srm.ScoresReplayMobile()
    scores_gradiant_gabor_svm_rbf.label = 'gabor (rbf g=1/4000)'
    scores_gradiant_gabor_svm_rbf.load(args.scores_directory + "/gabor-svm-C_SVC-RBF-g0.00025.hdf5")
    #scores_gradiant_gabor_svm_rbf.purgeNaN()
    print scores_gradiant_gabor_svm_rbf

    #scores_gradiant_gabor_svm_rbf_mean =  helpers.ScoresReplayMobile()
    #scores_gradiant_gabor_svm_rbf_mean.label = 'gabor (rbf g=1/4000) (mean)'
    #scores_gradiant_gabor_svm_rbf_mean.load(args.scores_directory + "gabor-svm-C_SVC-RBF-g0.00025-mean.hdf5")
    #scores_gradiant_gabor_svm_rbf.purgeNaN()
    #print scores_gradiant_gabor_svm_rbf_mean


    systems = []
    systems.append(scores_idiap)  
    systems.append(scores_gradiant_gabor_svm_rbf)  
    #systems.append(scores_gradiant_gabor_svm_rbf_mean)
#    txt_fancy_grid = helpers.evaluate_systems(systems, swap_subset = False)
    txt_fancy_grid = ev.evaluate_systems(systems, swap_subset = False)
    print "\nswap_subset = False"
    print txt_fancy_grid
    t_fancy_grid = open(os.path.join(args.result_directory, 'perf_table_biosig2016.rst'), 'w')
    t_fancy_grid.write(txt_fancy_grid.encode('utf-8'))    

    #txt_fancy_grid = helpers.evaluate_systems(systems, swap_subset = True)
    #print "\nswap_subset = True"
    #print txt_fancy_grid
    #t_fancy_grid = open(os.path.join(args.result_directory, 'swap_perf_table_biosig2016.rst'), 'w')
    #t_fancy_grid.write(txt_fancy_grid.encode('utf-8'))    

    sufix = '_roc_curve.eps'
#    helpers.plot_curves(args.result_directory,'IQM'+sufix, 'IQM - SVM-RBF($\gamma = 1.5$)', scores_idiap, swap_subset = False)
    ev.plot_curves(args.result_directory,'IQM'+sufix, 'IQM - SVM-RBF($\gamma = 1.5$)', scores_idiap, swap_subset = False)
#    helpers.plot_curves(args.result_directory,'Gabor_RBF_gamma000025'+sufix, 'Gabor - SVM-RBF($\gamma = 1/4000$)',scores_gradiant_gabor_svm_rbf, swap_subset = False)
    ev.plot_curves(args.result_directory,'Gabor_RBF_gamma000025'+sufix, 'Gabor - SVM-RBF($\gamma = 1/4000$)',scores_gradiant_gabor_svm_rbf, swap_subset = False)
    #helpers.plot_curves(args.result_directory,'Gabor_RBF_gamma000025_mean'+sufix,'Gabor - SVM-RBF($\gamma = 1/4000$) (mean)', scores_gradiant_gabor_svm_rbf_mean, swap_subset = False)

    #helpers.plot_curves(args.result_directory,'swap_IQM'+sufix, 'IQM - SVM-RBF($\gamma = 1.5$)', scores_idiap, swap_subset = True)
    #helpers.plot_curves(args.result_directory,'swap_Gabor_RBF_gamma000025'+sufix, 'Gabor - SVM-RBF($\gamma = 1/4000$)',scores_gradiant_gabor_svm_rbf, swap_subset = True)
    #helpers.plot_curves(args.result_directory,'swap_Gabor_RBF_gamma000025_mean'+sufix,'Gabor - SVM-RBF($\gamma = 1/4000$) (mean)', scores_gradiant_gabor_svm_rbf_mean, swap_subset = True)



'''
'''
if __name__ == '__main__':
        main(sys.argv[1:])

