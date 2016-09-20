from ConfigParser import SafeConfigParser
from alignment import Alignments
import motif_sites as ms
import numpy as np
import os
from collections import Counter
from features import Features
from performance_stats import PerformanceStats
import numpy as np
import pickle
import sys

########
# TO DO: REFACTOR CODE
########

def main():
    """Run the classification phase of DeFCoM.

    Args:
        sys.argv[1] = A python configuration file. For configuration file 
            details see https://docs.python.org/2/library/configparser.html.
    """
    #Load parameters from config file
    config_file = sys.argv[1]
    parser = SafeConfigParser(os.environ)
    parser.read(config_file)
    candidate_sites_file = parser.get('data', 'candidate_sites_file')
    bam_file = parser.get('data', 'candidate_bam_file')
    f_offset = parser.getint('options', 'f_offset')
    r_offset = parser.getint('options', 'r_offset')
    flank_size = parser.getint('options', 'flank_size')
    combine_strands = parser.getboolean('options', 'combine_strands')
    bias_correction = parser.getboolean('options', 'bias_correction')
    model_data_file = parser.get('options', 'model_data_file')
    results_file = parser.get('options', 'results_file')
    
    #Create data objects
    bam_data = Alignments(bam_file)
    candidate_data = ms.MotifSites(candidate_sites_file)
    model_data = pickle.load(open(model_data_file, 'rb'))
    svm = model_data["svm"]
    feature_scaler = model_data["feature_scaler"]

    #Prepare data
    candidate_sites = candidate_data.get_all_sites()
    cut_profiles = Features.convert_to_cuts(candidate_sites, bam_data, 
        flank_size, combine_strands, f_offset, r_offset, bias_correction)
    candidate_sites = candidate_data.get_all_sites()
    pwm_scores = Features.get_pwm_scores(candidate_sites)
    #Apply square root transformation
    cut_profiles = np.sqrt(cut_profiles)
    #Apply feature extraction
    partition_fn = np.vectorize(lambda x:x**2 + 5)
    split_pts = Features.get_splits(cut_profiles[0].size, partition_fn)
    center = cut_profiles[0].size/2  #For regional feature center size
    left = center - 15  #For regional feature center size
    right = center + 15  #For regional feature center size
    candidate_features = []
    for i in xrange(cut_profiles.shape[0]):
        row = cut_profiles[i]
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
            regional_slopes, regional_means, global_mean, [pwm_scores[i]]))
        candidate_features.append(row_features)
    #Scale features
    candidate_features = feature_scaler.transform(candidate_features)
    #Predict and output to file
    scores = svm.decision_function(candidate_features)
    fout = open(results_file, 'w')
    i = 0
    candidate_sites = candidate_data.get_all_sites()
    for site in candidate_sites:
        updated_row = list(site) + [str(scores[i])]
        fout.write("\t".join(updated_row) + "\n")
        i += 1
    fout.close()

if __name__ == '__main__':
    sys.exit(main())
