import csv
import glob
import pickle

'''
#---------------------------
# MODULE CONTENTS
#---------------------------
Functions to/for:
Import/export data

'''

#------------------------------
# IMPORT CENTROIDS FROM CSVs
#------------------------------


def import_centroids(input_dir):
    print "--------------------------------"
    print input_dir
    print "--------------------------------"

    centroid_arrays = []
    for matlab_export in glob.glob( input_dir ):
        in_file = open(matlab_export, "rU")
        with in_file as f:
            reader = csv.reader(f, delimiter=',')
            try:
                x, y = zip(*reader)
            except ValueError:
                x, y = (10000000,),(10000000,)

        i = 0
        array = []
        while i < len(x):
            array.append( ( float(x[i]), float(y[i]) ) )
            i += 1
        centroid_arrays.append(array)
    return centroid_arrays

#------------------------------
# WRITE STATISTICS TO CSV
#------------------------------

def write_prop_colliders(prop_colliders, output_dir):

    out_file = (output_dir + 'prop_colliders.csv')
    with open(out_file, 'wb') as f:
        selectric = csv.writer(f, delimiter = ',', quoting=csv.QUOTE_NONE, quotechar='')
        selectric.writerow( [prop_colliders] )

def write_motility_stats(output_dir, output_name, gf, rwf, merged_list):
    output_file_path = str(output_dir + output_name)

    motility_header = [ 'Well/XY', 'cell_id', 'total_distance', 'net_distance', 'linearity', 'spearmanrsq','progressivity',
    'max_speed', 'min_speed', 'avg_speed', 'MSD_slope', 'hurst_RS', 'nongauss', 'disp_var', 'disp_skew', 'rw_linearity', 'rw_netdist', 'rw_kurtosis01',
    'rw_kurtosis02', 'rw_kurtosis03', 'rw_kurtosis04', 'rw_kurtosis05', 'rw_kurtosis06', 'rw_kurtosis07',
    'rw_kurtosis08', 'rw_kurtosis09', 'rw_kurtosis10', 'avg_moving_speed01', 'avg_moving_speed02',
    'avg_moving_speed03', 'avg_moving_speed04', 'avg_moving_speed05', 'avg_moving_speed06',
    'avg_moving_speed07', 'avg_moving_speed08', 'avg_moving_speed09', 'avg_moving_speed10',
    'time_moving01', 'time_moving02', 'time_moving03', 'time_moving04', 'time_moving05',
    'time_moving06', 'time_moving07', 'time_moving08', 'time_moving09', 'time_moving10']

    theta_stats_list = []
    for i in gf.tau_range:
        for j in gf.interval_range:
            theta_stats_list.append( 'mean_theta_' + str(i) + '_' + str(j) )
            theta_stats_list.append( 'min_theta_' + str(i) + '_' + str(j) )
            theta_stats_list.append( 'max_theta_' + str(i) + '_' + str(j) )

    turn_stats_list = []
    for i in gf.tau_range:
        for j in gf.interval_range:
            turn_stats_list.append( 'p_rturn_' + str(i) + '_' + str(j) )

    autocorr_stats_list = []
    for i in range(1, rwf.autocorr_max_tau):
        autocorr_stats_list.append('autocorr_' + str(i))

    #partial_acorr_stats_list = []
    #for i in range(1, rwf.autocorr_max_tau):
    #    partial_acorr_stats_list.append('partial_acorr_' + str(i))

    #for i in moving_kurt_list:
    #    motility_header.append(i)
    for i in autocorr_stats_list:
        motility_header.append(i)
    #for i in partial_acorr_stats_list:
    #    motility_header.append(i)
    for i in turn_stats_list:
        motility_header.append(i)
    for i in theta_stats_list:
        motility_header.append(i)


    with open(output_file_path, 'wb') as out_file:
        selectric = csv.writer(out_file, delimiter = ',', quoting=csv.QUOTE_NONE, quotechar='')
        selectric.writerow( motility_header )
        i = 0
        while i < len(merged_list):
            selectric.writerow( merged_list[i] )
            i += 1

    print 'Wrote ', output_dir, output_name


#------------------------------
# PICKLES FOR AREA ANALYSIS
#------------------------------

# Pickle cell_ids to be used by area_changes.py
# Uses sobel check from above to name output file

def pickle_cell_ids( cell_ids, sobel, output_dir ):
    if sobel == True:
        pickle_output = (output_dir + 'centroid_paths_sobel.pickle')
    else:
        pickle_output = (output_dir + 'centroid_paths.pickle')

    pickle.dump( cell_ids, file(pickle_output, 'w') )
    print "Pickeled cell_ids for ", output_dir

def pickle_removed_ids( removed_ids, sobel, output_dir ):
    if sobel == True:
        pickle_output = (output_dir + 'removed_ids_sobel.pickle')
    else:
        pickle_output = (output_dir + 'removed_ids.pickle')

    pickle.dump( removed_ids, file(pickle_output, 'w') )
    print "Pickled removed_ids for ", output_dir
