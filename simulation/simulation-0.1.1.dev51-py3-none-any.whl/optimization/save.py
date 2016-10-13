import argparse
import re
import tempfile
import time

import simulation.optimization.cost_function
import simulation.optimization.job
import simulation.model.constants

import measurements.all.pw.data

import util.batch.universal.system
import util.logging
logger = util.logging.logger



def save(cost_functions, model_names=None, eval_f=True, eval_df=False):
    for cost_function in simulation.optimization.cost_function.iterator(cost_functions, model_names=model_names):
        if eval_f and not cost_function.f_available():
            logger.info('Saving cost function f value in {}'.format(cost_function.model.parameter_set_dir))
            cost_function.f()
        if eval_df and not cost_function.df_available():
            logger.info('Saving cost function df value in {}'.format(cost_function.model.parameter_set_dir))
            cost_function.df()



def save_for_all_measurements(max_box_distances_to_water=None, min_measurements_correlations=float('inf'), cost_function_classes=None, model_names=None, eval_f=True, eval_df=False):
    cost_functions = cost_functions_for_all_measurements(max_box_distances_to_water=max_box_distances_to_water, min_measurements_correlations=float('inf'), cost_function_classes=None)
    save(cost_functions, model_names=model_names, eval_f=eval_f, eval_df=eval_df)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculating cost function values.')
    parser.add_argument('-m', '--max_box_distances_to_water', type=int, default=None, nargin='+', help='The maximal distances to water boxes to accept measurements.')
    parser.add_argument('-c', '--min_measurements_correlations', type=int, default=float('inf'), help='The minimal number of measurements used to calculate correlations.')
    parser.add_argument('-n', '--node_kind', default='clexpress', help='Node kind to use for the jobs.')
    parser.add_argument('--DF', action='store_true', help='Eval (also) DF.')
    parser.add_argument('-d', '--debug_level', choices=util.logging.LEVELS, default='INFO', help='Print debug infos low to passed level.')
    args = parser.parse_args()
    
    with util.logging.Logger(level=args.debug_level):
        save_for_all_measurements(max_box_distances_to_water=args.max_box_distances_to_water, min_measurements_correlations=args.min_measurements_correlations, eval_f=True, eval_df=args.DF)
