from ConfigParser import SafeConfigParser
from alignment import Alignments
import motif_sites as ms
import numpy as np
import os
from collections import Counter
from features import Features
from sklearn import preprocessing, grid_search, svm, metrics
from performance_stats import PerformanceStats
from scipy import stats
import numpy as np
import pickle
import sys

########
# TO DO: REFACTOR CODE
########

def main():
    """Run the training phase of DeFCoM.

    Args:
        sys.argv[1] = A python configuration file. For configuration file 
            details see https://docs.python.org/2/library/configparser.html.
    """
    #Load parameters from config file
    config_file = sys.argv[1]
    parser = SafeConfigParser(os.environ)
    parser.read(config_file)
    active_sites_file = parser.get('data', 'active_sites_file')
    inactive_sites_file = parser.get('data', 'inactive_sites_file')
    bam_file = parser.get('data', 'training_bam_file')
    f_offset = parser.getint('options', 'f_offset')
    r_offset = parser.getint('options', 'r_offset')
    flank_size = parser.getint('options', 'flank_size')
    combine_strands = parser.getboolean('options', 'combine_strands')
    bias_correction = parser.getboolean('options', 'bias_correction')
    bootstrap_iterations = parser.getint('options', 'bootstrap_iterations')
    bootstrap_active_set_size = parser.getint('options', 
        'bootstrap_active_set_size')
    bootstrap_inactive_set_size = parser.getint('options', 
        'bootstrap_inactive_set_size')
    training_active_set_size = parser.getint('options', 
        'training_active_set_size')
    training_inactive_set_size = parser.getint('options', 
        'training_inactive_set_size')
    memory = parser.getint('options', 'memory_limit')
    model_data_file = parser.get('options', 'model_data_file')

    print "making data"    
    #Create data objects
    bam_data = Alignments(bam_file)
    active_sites = ms.MotifSites(active_sites_file)
    inactive_sites = ms.MotifSites(inactive_sites_file)

    print "begin bootstrap"
    #Execute parameter estimation via bootstrapping
    gammas = []
    c_rbf = []
    c_linear = []
    rbf_pauc = []
    lin_pauc = []
    active_bootstrap = active_sites.subsample_sites(
        bootstrap_active_set_size, bootstrap_iterations)
    inactive_bootstrap = active_sites.subsample_sites(
        bootstrap_inactive_set_size, bootstrap_iterations)
    for i in range(bootstrap_iterations):
        temp_active = active_bootstrap[i]
        temp_inactive = inactive_bootstrap[i]
        print "to cuts"
        active_cuts = Features.convert_to_cuts(temp_active, bam_data, 
            flank_size, combine_strands, f_offset, r_offset, bias_correction)
        inactive_cuts = Features.convert_to_cuts(temp_inactive, bam_data, 
            flank_size, combine_strands, f_offset, r_offset, bias_correction)
        active_pwm = Features.get_pwm_scores(temp_active)
        inactive_pwm = Features.get_pwm_scores(temp_inactive)
        
        print "sqrt transform"
        #Apply square root transformation
        active_cuts = np.sqrt(active_cuts)
        inactive_cuts = np.sqrt(inactive_cuts)
        #Apply feature extraction
        partition_fn = np.vectorize(lambda x:x**2 + 5)
        split_pts = Features.get_splits(active_cuts[0].size, partition_fn)
        center = active_cuts[0].size/2  #For regional feature center size
        left = center - 15  #For regional feature center size
        right = center + 15  #For regional feature center size
        active_features = []
        inactive_features = []
        print "feature extraction"
        for i in xrange(active_cuts.shape[0]):
            row = active_cuts[i]
            #Get local features
            row_split = np.split(row, split_pts)
            local_slopes = Features.get_slopes(row_split)
            local_means = np.vectorize(np.mean)(row_split)
            #Get regional features
            row_split = np.array([row[(left-30):left], row[left:right],
                row[right:(right+30)]])
            regional_slopes = Features.get_slopes(row_split)
            regional_means = np.mean(row_split, axis=1)
            global_mean = [np.mean(row[(center-75):(center+75)])]
            row_features = np.concatenate((local_slopes, local_means, 
                regional_slopes, regional_means, global_mean, [active_pwm[i]]))
            active_features.append(row_features)
        for i in xrange(inactive_cuts.shape[0]):
            row = inactive_cuts[i]
            #Get local features
            row_split = np.split(row, split_pts)
            local_slopes = Features.get_slopes(row_split)
            local_means = np.vectorize(np.mean)(row_split)
            #Get regional features
            row_split = np.array([row[(left-30):left], row[left:right],
                row[right:(right+30)]])
            regional_slopes = Features.get_slopes(row_split)
            regional_means = np.mean(row_split, axis=1)
            global_mean = [np.mean(row[(center-75):(center+75)])]
            row_features = np.concatenate((local_slopes, local_means, 
                regional_slopes, regional_means, global_mean, 
                [inactive_pwm[i]]))
            inactive_features.append(row_features)
        
        combined_features = np.concatenate((active_features, 
            inactive_features), axis=0)
        feature_scaler = preprocessing.MaxAbsScaler()
        training_set = feature_scaler.fit_transform(combined_features)
        active_labels = [1] * len(active_features)
        inactive_labels = [-1] * len(inactive_features)
        training_labels = active_labels + inactive_labels
        
        print "cross-validation"
        #Perform cross-validation
        gamma_range = np.logspace(-6,3,10)
        c_range = np.logspace(-3,4,8)
        parameters = {'C':c_range, 'gamma':gamma_range}
        pauc_scorer = metrics.make_scorer(PerformanceStats.pAUC, 
            needs_threshold=True, fpr_cutoff=0.05)
        #RBF kernel SVM
        gridCV = grid_search.GridSearchCV(
            svm.SVC(cache_size=memory, kernel="rbf"),
            parameters, n_jobs=3, pre_dispatch=3, cv=5,
            scoring=pauc_scorer, refit=False)
        gridCV.fit(training_set, training_labels)
        c_rbf.append(gridCV.best_params_["C"])
        gammas.append(gridCV.best_params_["gamma"])
        rbf_pauc.append(gridCV.best_score_)
        #Linear SVM
        parameters = {'C':c_range}
        gridCV = grid_search.GridSearchCV(svm.SVC(kernel="linear"), 
            parameters, n_jobs=3, pre_dispatch=3, cv=5,
            scoring=pauc_scorer, refit=False)
        gridCV.fit(training_set, training_labels)
        c_linear.append(gridCV.best_params_["C"])
        lin_pauc.append(gridCV.best_score_)
    
    print "t-test"
    #Use t-test to determine better model
    pval = stats.ttest_ind(lin_pauc, rbf_pauc)[1]
    if pval > 0.01:
        best_c = Counter(c_linear).most_common(1)[0][0]
        final_model = svm.SVC(kernel="linear", C=best_c)
    elif np.mean(lin_pauc) > np.mean(rbf_pauc):
        best_c = Counter(c_linear).most_common(1)[0][0]
        final_model = svm.SVC(kernel="linear", C=best_c)
    else:
        best_c = Counter(c_rbf).most_common(1)[0][0]
        best_gamma = Counter(gammas).most_common(1)[0][0]
        final_model = svm.SVC(kernel="linear", C=best_c, gamma=best_gamma)
    
    print "final model training"
    #Train final model
    active_set = active_sites.subsample_sites(training_active_set_size)[0]
    inactive_set = inactive_sites.subsample_sites(training_inactive_set_size)[0]
    active_cuts = Features.convert_to_cuts(active_set, bam_data, flank_size, 
        combine_strands, f_offset, r_offset, bias_correction)
    inactive_cuts = Features.convert_to_cuts(inactive_set, bam_data,
        flank_size, combine_strands, f_offset, r_offset, bias_correction)
    active_pwm = Features.get_pwm_scores(active_set)
    inactive_pwm = Features.get_pwm_scores(inactive_set)
    #Apply square root transformation
    active_cuts = np.sqrt(active_cuts)
    inactive_cuts = np.sqrt(inactive_cuts)
    print "feature extraction"
    #Apply feature extraction
    partition_fn = np.vectorize(lambda x:x**2 + 5)
    split_pts = Features.get_splits(active_cuts[0].size, partition_fn)
    center = active_cuts[0].size/2  #For regional feature center size
    left = center - 15  #For regional feature center size
    right = center + 15  #For regional feature center size
    active_features = []
    inactive_features = []
    for i in xrange(active_cuts.shape[0]):
        row = active_cuts[i]
        #Get local features
        row_split = np.split(row, split_pts)
        local_slopes = Features.get_slopes(row_split)
        local_means = np.vectorize(np.mean)(row_split)
        #Get regional features
        row_split = np.array([row[(left-30):left], row[left:right],
            row[right:(right+30)]])
        regional_slopes = Features.get_slopes(row_split)
        regional_means = np.mean(row_split, axis=1)
        global_mean = [np.mean(row[(center-75):(center+75)])]
        row_features = np.concatenate((local_slopes, local_means,
            regional_slopes, regional_means, global_mean, [active_pwm[i]]))
        active_features.append(row_features)
    for i in xrange(inactive_cuts.shape[0]):
        row = inactive_cuts[i]
        #Get local features
        row_split = np.split(row, split_pts)
        local_slopes = Features.get_slopes(row_split)
        local_means = np.vectorize(np.mean)(row_split)
        #Get regional features
        row_split = np.array([row[(left-30):left], row[left:right],
            row[right:(right+30)]])
        regional_slopes = Features.get_slopes(row_split)
        regional_means = np.mean(row_split, axis=1)
        global_mean = [np.mean(row[(center-75):(center+75)])]
        row_features = np.concatenate((local_slopes, local_means,
            regional_slopes, regional_means, global_mean, [inactive_pwm[i]]))
        inactive_features.append(row_features)

    combined_features = np.concatenate((active_features,
        inactive_features), axis=0)
    feature_scaler = preprocessing.MaxAbsScaler()
    training_set = feature_scaler.fit_transform(combined_features)
    active_labels = [1] * len(active_features)
    inactive_labels = [-1] * len(inactive_features)
    training_labels = active_labels + inactive_labels
    print "final model fit"
    final_model.fit(training_set, training_labels)
    model_data = {"svm": final_model, "feature_scaler": feature_scaler}
    print "pickling"
    pickle.dump(model_data, open(model_data_file, 'wb'))
    

if __name__ == '__main__':
    sys.exit(main()) 
