#!/usr/bin/env python
# encoding: utf-8
# Sushil Bhattacharjee <sushil.bhattacharjee@idiap.ch>
# Tue 31 Aug 13:34:23 CEST 2015

"""
This script trains a classifier (linear logistic regression, or linear discriminant analysis) 
on IQM-features, to separate genuine vs. spoof attacks
"""

import os, sys
import argparse
import numpy as np
# from matplotlib import pyplot as P

#from sklearn import svm

import bob.io.base
import bob.learn.linear
import antispoofing.utils.db as bobdb
#import bob.learn.em
import bob.learn.libsvm


'''
'''
def trainLDA(posDS, negDS, pInv):
    """ Takes the two training-sets (representing positive-class and negative-class),
        and returns a trained LDA based 2-class classifier.
        
        Args:
        posDS (2D numpy array): Nxd array contains N d-dimensional samples of the POSITIVE class
        negDS (2D numpy array): Nxd array contains N d-dimensional samples of the NEGATIVE class
        pInv (bool): whether to use pseudo-inverse or not, when training LDA-classifier. 
                     True: yes, use pseudo-inverse; False: no, do not use pseudo-inverse.
        
        Returns:
        bob.machine.LinearMachine: a trained LDA (2-class) classifier.
        
    """
    from antispoofing.utils.ml.norm import zeromean_unitvar_norm
    from antispoofing.utils.ml.norm import calc_mean_std
        
    mean, std = calc_mean_std(posDS, negDS, nonStdZero=True)
    
    posDS = zeromean_unitvar_norm(posDS, mean, std)
    negDS = zeromean_unitvar_norm(negDS, mean, std)
    ldaTrainer = bob.learn.linear.FisherLDATrainer(pInv)
    # print('calling ldaTrainer.train')
    classifier, _ = ldaTrainer.train([negDS, posDS])
    classifier.resize(classifier.shape[0], 1)
    # so we get real and attacks on the "right" side of the axis
    posScores = classifier(posDS)[:,0]
    negScores = classifier(negDS)[:,0]
    #adjust the 'direction' of projection, so as to have, in general, higher scores for positive samples than for negative samples.
    # print 'setting score-sign for lda'
    flipSign = 1
    if np.median(negScores) > np.median(posScores): flipSign = -1
    classifier.weights = flipSign*classifier.weights
    # save the normalization parameters
    classifier.input_subtract = mean
    classifier.input_divide = std
    # print "trainLDA:", type(classifier)
    return classifier

'''
'''
def ldaScores(trainedLdaMachine, dataSet):
    scores = trainedLdaMachine(dataSet)[:,0]
    return scores

 
'''
'''
def trainSVM(posTS, negTS, minFeats, maxFeats, gamma=None):
    svmTrainer = bob.learn.libsvm.Trainer()
    svmTrainer.kernel_type = 'RBF'
    svmTrainer.probability = True
    if gamma is not None:
        svmTrainer.gamma = gamma
     
    #scale input features in training-set before calling trainer
#     trSet = np.vstack((posTS, negTS))
#     trMin = np.amin(trSet, axis=1)
#     trMax = np.amax(trSet, axis=1)
    diffFeats = maxFeats - minFeats
    posTS = (2*((posTS-minFeats)/diffFeats)) - 1
    negTS = (2*((negTS-minFeats)/diffFeats)) - 1
     
    trainingSet = [posTS, negTS]
    svMachine = svmTrainer.train(trainingSet)
     
    return svMachine


# '''
# returns scores for neg. and pos. patterns, based on a pre-trained classifier
# '''
# def svmScores(trainedSvm, posDat, negDat, featMin, featMax):
#         scoresDatPos = None
#         scoresDatNeg = None
#         diffFeats = featMax - featMin
#         if posDat is not None:
#             posDat_norm = (2*((posDat-featMin)/diffFeats)) - 1
#             _, scoresDatPos = trainedSvm.predict_class_and_scores(posDat_norm)
#             scoresDatPos= scoresDatPos[:,0]
#         if negDat is not None:
#             negDat_norm = (2*((negDat-featMin)/diffFeats)) - 1
#             _, scoresDatNeg = trainedSvm.predict_class_and_scores(negDat_norm)
#             scoresDatNeg= scoresDatNeg[:,0]
#         
#         return scoresDatPos, scoresDatNeg

'''
returns scores for neg. and pos. patterns, based on a pre-trained classifier
'''
def svmScores(trainedSvm, ds, normMin, normMax):
    scoresDatPos = None
    scoresDatNeg = None
    diffFeats = normMax - normMin
    if ds is not None:
        normDS = (2*((ds - normMin)/diffFeats)) - 1
        _, scoresDS = trainedSvm.predict_class_and_scores(normDS)
        scoresDS= scoresDS[:,0]
     
    return scoresDS


'''
'''
def getClsScores(trainedClassifier, posDat, negDat, featMin, featMax):
    scores_pos = None
    scores_neg = None
    if isinstance(trainedClassifier, bob.learn.linear.Machine):
        if posDat is not None:
            scores_pos = ldaScores(trainedClassifier, posDat)
        if negDat is not None:
            scores_neg = ldaScores(trainedClassifier, negDat)
    else:
        if posDat is not None:
            scores_pos = svmScores(trainedClassifier, posDat, featMin, featMax)
        if negDat is not None:
            scores_neg = svmScores(trainedClassifier, negDat, featMin, featMax)
    
    return scores_pos, scores_neg


'''
loads file-objects from database according to the subparsers specified for the database in 'arguments'
'''
# def loadDbObjects(database):
def loadDbObjects(arguments):
    argParser = ConstructArgumentList()
    #myArgParser = argParser
#     print arguments
    bobdb.Database.create_parser(argParser, implements_any_of='video')
    args = argParser.parse_args(arguments)
    database = args.cls(args)
    
    realTrnFiles, attackTrnFiles = database.get_train_data()
    realDevFiles, attackDevFiles = database.get_devel_data()
    realTstFiles, attackTstFiles = database.get_test_data()
#     print 'loaded devel set: (', len(realDevFiles),', ', len(attackDevFiles),')'
#     print attackDevFiles[0].videofile("")
#     print 'loaded test set: (', len(realTstFiles),', ', len(attackTstFiles),')'
#     print attackTstFiles[0].videofile("")
#     print " "

    return ((realTrnFiles, attackTrnFiles), (realDevFiles, attackDevFiles), (realTstFiles, attackTstFiles))

'''
'''
def loadDataByAttackType(dbname, mode='split', verboseFlag=0):
    """loads dataset from database in separate subsets"""
    
    if not isinstance(mode, str): mode = 'split'
    if mode is None: mode='split'
    
    if mode == 'split':
        if dbname == 'replaymobile':
    
            dbCmdlnOptions = ['replaymobile ', 'replaymobile --protocol print --support fixed ', 'replaymobile --protocol print --support hand ', \
        #                           'replaymobile --protocol mattescreen --support fixed ', 'replaymobile --protocol mattescreen --support hand ', \
                              'replaymobile --protocol mattescreen --sample_types photo', 'replaymobile --protocol mattescreen --sample_types video'
                             ]
        
            attackLabels = ['print-fixed', 'print-hand', 'mattescreen-photo', 'mattescreen-video']
        else:
            assert False, "Split-mode classification is only supported for replaymobile database"
    else:
        if dbname == 'replay':
            dbCmdlnOptions = ['replay --protocol grandtest']
            attackLabels = ['grandtest']
            
        elif dbname == 'replaymobile':
            dbCmdlnOptions = ['replaymobile --protocol grandtest']
            attackLabels = ['grandtest']
        else:
            assert False, "Wrong database specified. Choose either 'replaymobile' or 'replay'"
        
    
    trainingEnsemble = []
    develEnsemble= []
    testEnsemble= []
    for dbo in dbCmdlnOptions:
        if verboseFlag>1: print('database options: %s' % dbo)
        myCommandlineOptions = '' #clOptions0 + clOptions2
        commandlineOptions = myCommandlineOptions + dbo
        #print commandlineOptions
        argumentList = commandlineOptions.split()
        trainingSet, develSet, testSet = loadDbObjects(argumentList)
        trainingEnsemble.append(trainingSet)
        develEnsemble.append(develSet)
        testEnsemble.append(testSet)

    return trainingEnsemble, develEnsemble, testEnsemble, attackLabels


def load_features(flist, sourcePath):
    
    d = bob.io.base.load([k.make_path(sourcePath, '.h5') for k in flist])  
    return d

'''
'''
def ConstructArgumentList():
    """Constructs and ArgumentParser object for the expected arguments.
       Returns:
       argparse.ArgumentParser object.
    """

    cwd = os.getcwd()
    features_folder = os.path.join(cwd, 'features')
    scores_folder = os.path.join(cwd, 'scores')
    output_scores_file = os.path.join(scores_folder, 'iqm_scores.hdf5')

    #code for parsing command line args.
    argParser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    argParser.add_argument('-c', '--classifier', default = 'SVM', choices=['LDA', 'SVM'], dest='classifier',
      help='specify which classifier you want to use: LDA or SVM. (Default: %(default)s)')
        
    argParser.add_argument('--svm_gamma', dest='svmGamma', default = 1.5, type=float, metavar='FLOAT',
        help='Gamma parameter for svm-RBF (Default: %(default)s).' )
    
    argParser.add_argument('--lda_pinv', action='store_true', dest='ldaPinv',
      default=False, help='use pseudo-inverse when using LDA (Default: %(default)s)')

    argParser.add_argument('-b', '--basePath', dest='basePath', default = features_folder, #'~/work/git/bob.paper.BioSig2016_ReplayMobile/features',
       help='base path where feature-file-folder exists.')
    
    argParser.add_argument('-f', '--feature_dir', dest='featDir', default = 'ReplayMobile_IQM',
       help='folder where to find feature-files corresponding to the specified database.')
    
    argParser.add_argument('-o', '--output_score_file', dest='scoreFile', default = output_scores_file, #'~/work/git/bob.paper.BioSig2016_ReplayMobile/scores/scores.hdf5',
       help='full path of file where scores will be saved in hdf5 format ')
     
    argParser.add_argument('-g', '--grandtest_only', action='store_true', dest='grandTest', default = False,
       help='to run experiment with only the grandtest protocol of the database.')
    
    # verbose
    argParser.add_argument('-v', '--verbose', dest='verbose', metavar='INT', type=int, choices=[0, 1, 2], default=0,
      help='Prints extra messages during execution; useful for debugging.  (Default: %(default)s)')
    
    return argParser



def trainClassifier(classifierType, trainingSet, datapath, ldaPinv, svmGamma, verboseFlag=0):
    realFiles, attackFiles = trainingSet
#     assert len(attackFiles)>0, 'No attack-data in training-set.'
#     print 'no. of real files:', len(realFiles)
#     posTS = load_features(realFiles, datapath)
#     print 'no. of attack files:', len(attackFiles)
#     negTS = load_features(attackFiles, datapath) 
    
    posTS, negTS = loadFeatureSets(trainingSet, datapath, verboseFlag)
    
    trSet = np.vstack((posTS, negTS))
    trMin = np.amin(trSet, axis=0)
    trMax = np.amax(trSet, axis=0)
#     print trMin.shape
    
    if classifierType == 'LDA':
        if verboseFlag > 1: print("training LDA")
        clsMachine = trainLDA(posTS, negTS, ldaPinv)
        if verboseFlag > 1: print("LDA trained")
    else:
        if verboseFlag > 1: print("training SVM")
        #svMachine = trainSVM(posTS, negTS, trMin, trMax, args)
        clsMachine = trainSVM(posTS, negTS, trMin, trMax, svmGamma)
        if verboseFlag > 1: print("SVM trained")
#         if isinstance(clsMachine, bob.learn.libsvm.Machine):
        if verboseFlag>1: 
            print('#support vectors: %s' % str(clsMachine.n_support_vectors) )
            print('gamma= %s' % str(clsMachine.gamma) )
    
    if verboseFlag>0: print('trained classifier.')
    
    return clsMachine, trMin, trMax


def loadFeatureSets(dataSet, datapath, verboseFlag=0):
    """ loads the real and attack parts of input dataSet in separate sets.
    Returns:
        posDS: dataset for real presentations
        negDS: dataset for negative presentations
    """
    
    realFiles, attackFiles = dataSet

    posDS = None
    if len(realFiles)>0:
        posDS = load_features(realFiles, datapath)      #suffix 'DS': devel-set
    negDS = None
    if len(attackFiles)>0:
        negDS = load_features(attackFiles, datapath)

    if verboseFlag >1:
        if negDS is not None:
            print('attacks: %s' % str(negDS.shape))
        if posDS is not None:
            print('genuine: %s' % str(posDS.shape))
        print('... feature-set loaded.')
    
    return posDS, negDS


def main(command_line_parameters = None):
    #0. parse arguments
    argParser = ConstructArgumentList()
    
    bobdb.Database.create_parser(argParser, implements_any_of='video')
    args = argParser.parse_args(command_line_parameters)
    #make sure the user specifies a folder where feature-files exist
    if not args.basePath: argParser.error('Specify mandatory parameter --base_path')
    if not args.featDir: argParser.error('Specify mandatory parameter --feature_dir')
    if not args.scoreFile: argParser.error('Specify mandatory parameter --score_file')
    
    database = args.cls(args)
    dbname = args.name
    inPath = os.path.join(args.basePath, args.featDir)
    
    if args.grandTest:
        if args.verbose > 0: print('perform grandtest on: %s' % dbname)
        if args.verbose>0: print('loading training data')
        trainingEnsemble, develEnsemble, testEnsemble, attackLabels = loadDataByAttackType(dbname, mode='grandtest', verboseFlag=args.verbose)
        trainGrandSet = trainingEnsemble[0]
        develGrandSet = develEnsemble[0]
        testGrandSet = testEnsemble[0]
        del develEnsemble[0]
        del testEnsemble[0]
#         print len(trainGrandSet)
        if args.verbose>0: print('training classifier')
        clsMachine, trMin, trMax = trainClassifier(args.classifier, trainGrandSet, inPath, args.ldaPinv, args.svmGamma, args.verbose)
        
        #3. load and compute scores for devel data
        dev_threshold = None      #    initialization
        scores_dev_pos=None
        scores_dev_neg=None
        dev_hter=None
        
        devEnsembleScores = []
        allDevScores_pos = None
        allDevScores_neg = []
        if args.verbose>1: print('loading development set')
        posDS, negDS = loadFeatureSets(develGrandSet, inPath, args.verbose)

        scores_dev_pos, scores_dev_neg =  getClsScores(clsMachine, posDS, negDS, trMin, trMax)
        devEnsembleScores.append((scores_dev_pos, scores_dev_neg))
        if scores_dev_pos is not None:
#             print 'Num. pos. dev. scores:', len(scores_dev_pos)
            if allDevScores_pos is None:            #scores for the real (positive) class need to be appended only once.
                allDevScores_pos = scores_dev_pos
            else:
                allDevScores_pos.extend(scores_dev_pos)
        if scores_dev_neg is not None:
#             print 'extending neg. dev. score-set by', len(scores_dev_neg), 'scores'
            allDevScores_neg.extend(scores_dev_neg)
#             print 'Num. neg. dev. scores:', len(allDevScores_neg)
            
        
        #4. load and compute scores for test data
        testEnsembleScores = []
        allTestScores_pos = None
        allTestScores_neg = []   #this is initialized as an empty list, to be able to used extend() later.
        if args.verbose>1: print('loading test set') 
        posTE, negTE = loadFeatureSets(testGrandSet, inPath, args.verbose)

        scores_test_pos, scores_test_neg = getClsScores(clsMachine, posTE, negTE, trMin, trMax)
        testEnsembleScores.append((scores_test_pos, scores_test_neg))
        if scores_test_pos is not None:
            if allTestScores_pos is None:
                allTestScores_pos = scores_test_pos

        if scores_test_neg is not None:
            allTestScores_neg.extend(scores_test_neg)
                
        printPADResults(allDevScores_neg, allDevScores_pos, allTestScores_neg, allTestScores_pos)
        
        #5. save scores in a file
        scoreFilename = args.scoreFile 
        if args.verbose>0: print('saving scores in %s' % scoreFilename)
        SaveScoresAsHdf5File(scoreFilename, attackLabels, devEnsembleScores, testEnsembleScores)
        
        #6. analyze score-file to compute classifier performance measures
#         if dbname == 'replaymobile':
        computePADPerformanceFromFile(scoreFilename)
            
    
    else: #split-mode classification
        #1. load training data
        if args.verbose>0: print('loading training data')
        trainingEnsemble, develEnsemble, testEnsemble, attackLabels = loadDataByAttackType(dbname, mode='split', verboseFlag=args.verbose)
        trainGrandSet = trainingEnsemble[0]
        develGrandSet = develEnsemble[0]
        del develEnsemble[0]
        testGrandSet = testEnsemble[0]
        del testEnsemble[0]
#         print len(trainGrandSet)
        
        #2. train classifier
        if args.verbose>0: print('training classifier')
        clsMachine, trMin, trMax = trainClassifier(args.classifier, trainGrandSet, inPath, args.ldaPinv, args.svmGamma, args.verbose)           
        
        #3. load and compute scores for validation data
        dev_threshold = None      #    initialization
        scores_dev_pos=None
        scores_dev_neg=None
        dev_hter=None
        
        devEnsembleScores = []
        allDevScores_pos = None
        allDevScores_neg = []
        if args.verbose>0: print('num. categories in devel. set: %s' % len(develEnsemble) )
        for attackType in develEnsemble:
            posDS, negDS = loadFeatureSets(attackType, inPath, args.verbose)
    
            scores_dev_pos, scores_dev_neg =  getClsScores(clsMachine, posDS, negDS, trMin, trMax)
            devEnsembleScores.append((scores_dev_pos, scores_dev_neg))
            if scores_dev_pos is not None:
#                 print 'Num. pos. dev. scores:', len(scores_dev_pos)
                if allDevScores_pos is None:            #scores for the real (positive) class need to be appended only once.
                    allDevScores_pos = scores_dev_pos
    #             else:
    #                 allDevScores_pos.extend(scores_dev_pos)
            if scores_dev_neg is not None:
#                 print 'extending neg. dev. score-set by', len(scores_dev_neg), 'scores'
                allDevScores_neg.extend(scores_dev_neg)
#                 print 'Num. neg. dev. scores:', len(allDevScores_neg)
        
        #4. load and compute scores for test data
        testEnsembleScores = []
        allTestScores_pos = None
        allTestScores_neg = []   #this is initialized as an empty list, to be able to used extend() later.
        if args.verbose>0: print('num. categories in test set.: %s' % len(testEnsemble) )
        for attackType in testEnsemble:
            posTE, negTE = loadFeatureSets(attackType, inPath, args.verbose)
    
            scores_test_pos, scores_test_neg = getClsScores(clsMachine, posTE, negTE, trMin, trMax)
            testEnsembleScores.append((scores_test_pos, scores_test_neg))
            if scores_test_pos is not None:
                if allTestScores_pos is None:
                    allTestScores_pos = scores_test_pos
    
            if scores_test_neg is not None:
                allTestScores_neg.extend(scores_test_neg)
                
#         printPADResults(allDevScores_neg, allDevScores_pos, allTestScores_neg, allTestScores_pos)
        
        #5. save scores in a file
        scoreFilename = args.scoreFile 
        if args.verbose>0: print('saving scores in %s' % scoreFilename)
        SaveScoresAsHdf5File(scoreFilename, attackLabels, devEnsembleScores, testEnsembleScores)
        
        #6. analyze score-file to compute classifier performance measures
        if dbname == 'replaymobile':
            computePADPerformanceFromFile(scoreFilename)
    

'''
'''
def SaveScoresAsHdf5File(scoreFileName, attackLabels, devEnsembleScores, testEnsembleScores):
#         print "Generating score-file for devel and test."
        scoreh5 = bob.io.base.HDF5File(scoreFileName,'w')
        
        #save scores for development set
        h5Dir1 = '/devel'
        scoreh5.create_group(h5Dir1)
#         bob.io.base.HDF5File.cd(scoreh5, h5Dir1)
        
#         print 'num. attack types in dev:', len(devEnsembleScores)
        for i in range(len(devEnsembleScores)):
#             print attackLabels[i]
            bob.io.base.HDF5File.cd(scoreh5, h5Dir1)
            h5Dir2 = attackLabels[i]
            scoreh5.create_group(h5Dir2)
            
            if i==0 and devEnsembleScores[i][0] is not None:
                bob.io.base.HDF5File.cd(scoreh5, h5Dir1)
                scoreh5.set('real', devEnsembleScores[i][0])
            
            if devEnsembleScores[i][1] is not None:
                bob.io.base.HDF5File.cd(scoreh5, h5Dir2)
                scoreh5.set('attack', devEnsembleScores[i][1])
        
        # save scores for test-set
        bob.io.base.HDF5File.cd(scoreh5, '/')
        h5Dir1 = '/test'
        scoreh5.create_group(h5Dir1)
#         bob.io.base.HDF5File.cd(scoreh5, h5Dir1)
#         
#         print " "
#         print 'num. attack types in test:', len(testEnsembleScores)
        for i in range(len(testEnsembleScores)):
            bob.io.base.HDF5File.cd(scoreh5, h5Dir1)
            h5Dir2 = attackLabels[i]
            scoreh5.create_group(h5Dir2)
            
#             print attackLabels[i]
            
            if i==0 and testEnsembleScores[i][0] is not None:
                bob.io.base.HDF5File.cd(scoreh5, h5Dir1)
                scoreh5.set('real', testEnsembleScores[i][0])
                
            if testEnsembleScores[i][1] is not None:
                bob.io.base.HDF5File.cd(scoreh5, h5Dir2)
                scoreh5.set('attack', testEnsembleScores[i][1])
                
        
        del scoreh5


def computePADPerformanceFromFile(hdf5scorefile):
    scoreh5 = bob.io.base.HDF5File(hdf5scorefile,'r')

    test_folder  = '/test'
    devel_folder = '/devel'
 
    bob.io.base.HDF5File.cd(scoreh5, '/')
    if scoreh5.has_group(devel_folder):
        bob.io.base.HDF5File.cd(scoreh5, devel_folder)
        allDevScores_pos = scoreh5.read('real')
#         print 'Num. dev. pos. scores', len(allDevScores_pos)
        develKeys = scoreh5.keys()
        allDevScores_neg = []
        for k in develKeys:
            if 'attack' in k:
                dev_scores_neg = scoreh5.read(k)
#                 print 'extending allDevScores_neg by', len(dev_scores_neg), 'scores'
                allDevScores_neg.extend(dev_scores_neg)
#                 print 'Num. dev. neg. scores', len(allDevScores_neg)
   
    bob.io.base.HDF5File.cd(scoreh5, '/')
    if scoreh5.has_group(test_folder):
        bob.io.base.HDF5File.cd(scoreh5, test_folder)
        allTestScores_pos = scoreh5.read('real')
#         print 'Num. test pos. scores', len(allTestScores_pos)
        testKeys = scoreh5.keys()
        allTestScores_neg = []
        for k in testKeys:
            if 'attack' in k:
                test_scores_neg = scoreh5.read(k)
#                 print 'extending allTestScores_neg by', len(test_scores_neg), 'scores'
                allTestScores_neg.extend(test_scores_neg)     
#                 print 'Num. test neg. scores', len(allTestScores_neg)  
    
#    printPADResults(allDevScores_neg, allDevScores_pos, allTestScores_neg, allTestScores_pos)   


def printPADResults(allDevScores_neg, allDevScores_pos, allTestScores_neg, allTestScores_pos):
#     print 'Devel. scores:', len(allDevScores_neg), len(allDevScores_pos)
#     print 'Test scores:', len(allTestScores_neg), len(allTestScores_pos)
    dev_threshold = bob.measure.eer_threshold(allDevScores_neg, allDevScores_pos)
#     print 'dev_treshold:', dev_threshold
    if dev_threshold is not None:
        far, frr = bob.measure.farfrr(allDevScores_neg, allDevScores_pos, dev_threshold)
        
        devTrueNeg=0
        for k, v in enumerate(allDevScores_neg):
            if v < dev_threshold:
                devTrueNeg += 1
          
        devTruePos=0
        for k, v in enumerate(allDevScores_pos):
            if v >= dev_threshold:
                devTruePos += 1
        
#         devTrueNeg = bob.measure.correctly_classified_negatives(allDevScores_neg, dev_threshold).sum()
#         devTruePos = bob.measure.correctly_classified_positives(allDevScores_pos, dev_threshold).sum()
        print(" -> Devel set threshold  @ EER: %.5e" % dev_threshold)
        print(" -> Devel set results:")
        print("     * FAR : %.3f%% (%d/%d)" % (100*far, len(allDevScores_neg)-devTrueNeg, len(allDevScores_neg)) )
        print("     * FRR : %.3f%% (%d/%d)" % (100*frr, len(allDevScores_pos)-devTruePos, len(allDevScores_pos)) )
        print("     * EER : %.3f%%" % (50*(far+frr)) )
   
    if dev_threshold is not None:
        test_far, test_frr = bob.measure.farfrr(allTestScores_neg, allTestScores_pos, dev_threshold)
        test_far *= 100
        test_frr *= 100
        test_hter = (0.5*(test_far+test_frr))
        
        testTrueNeg=0
        for k, v in enumerate(allTestScores_neg):
            if v < dev_threshold:
                testTrueNeg += 1
       
        testTruePos=0
        for k, v in enumerate(allTestScores_pos):
            if v >= dev_threshold:
                testTruePos += 1

#         testTrueNeg = bob.measure.correctly_classified_negatives(allTestScores_neg, dev_threshold).sum()
#         testTruePos = bob.measure.correctly_classified_positives(allTestScores_pos, dev_threshold).sum()
#         print('testTrueNeg, testTruePos', testTrueNeg, testTruePos )
        print(" -> devel set threshold @ EER: %.5e" % dev_threshold )
        print(" -> Test set results:" )
        print("     * FAR : %.3f%% (%d/%d)" % (test_far, len(allTestScores_neg)-testTrueNeg, len(allTestScores_neg)) )
        print("     * FRR : %.3f%% (%d/%d)" % (test_frr, len(allTestScores_pos)-testTruePos, len(allTestScores_pos)) )
        print("     * HTER: %.3f%%" % (test_hter) )


'''
'''
if __name__ == '__main__':
    main(sys.argv[1:])
