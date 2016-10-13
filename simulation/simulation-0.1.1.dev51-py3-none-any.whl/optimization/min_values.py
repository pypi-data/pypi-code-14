import numpy as np

import util.multi_dict

import simulation.model.options
import simulation.optimization.cost_function



f_key = 'f'
parameters_key = 'parameters'
concentrations_key = 'concentrations'



def min_values(cost_functions, model_names=None, filter_function=None):
    if filter_function is None:
        filter_function = lambda model_options: True
    
    results_dict = util.multi_dict.MultiDict()
    
    for cost_function in simulation.optimization.cost_function.iterator(cost_function, model_names=model_names):
        model_options = cost_function.model.model_options
        if filter_function(model_options) and cost_function.f_available():
            ## key
            key = (model_options.model_name, model_options.time_step, cost_function.name)
            ## value dict and min value
            try:
                values_dict = results_dict[key][0]
            except KeyError:
                values_dict = {f_key: float('inf')}
                results_dict[key] = [values_dict]
            min_f = values_dict[f_key]
            ## store if better
            f = cost_function.f()
            if f < min_f:
                values_dict[f_key] = f
                values_dict[parameters_key] = model_options.parameters
                values_dict[concentrations_key] = model_options.initial_concentration_options.concentrations
    
    return results_dict



def all_values_for_min_values(cost_functions, model_names=None, filter_function=None, normalize=False):
    
    def normalized_value(cf_value, min_cf_value):
        if normalize:
            return cf_value / min_cf_value
        else:
            return cf_value
    
    results_dict = min_values(cost_functions, model_names=model_names, filter_function=filter_function)
    
    all_values_dict = util.multi_dict.MultiDict()
    
    for (key, value_list) in results_dict.iterator_keys_and_value_lists():
        (model_name, time_step, cost_function_name) = key
        assert len(value_list) == 1
        values_dict = value_list[0]
        concentrations = tuple(values_dict[concentrations_key])
        parameters = tuple(values_dict[parameters_key])
        min_f = values_dict[f_key]
        
        model_options = simulation.model.options.ModelOptions()
        model_options.model_name = model_name
        model_options.time_step = time_step
        model_options.parameters = parameters
        model_options.initial_concentration_options.concentrations = concentrations
        
        new_key = (model_name, time_step, concentrations, parameters)
        
        for cost_function in cost_functions:
            old_measurements = cost_function.measurements
            cost_function.measurements = old_measurements.subset(model_options.tracers)
            f = cost_function.f()
            all_values_dict[new_key + (cost_function.name,)] = [normalized_value(f, min_f)]
            cost_function.measurements = old_measurements
    
    return all_values_dict



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Getting minimal cost function values.')
    parser.add_argument('-m', '--max_box_distance_to_water', type=int, default=float('inf'), help='The maximal distance to water boxes to accept measurements.')
    parser.add_argument('-c', '--min_measurements_correlations', type=int, default=float('inf'), help='The minimal number of measurements used to calculate correlations.')
    parser.add_argument('-n', '--normalize' action='store_true', help='Normalize cost function values.')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug infos.')
    args = parser.parse_args()
    
    with util.logging.Logger(disp_stdout=args.debug):
        measurements_collection = measurements.all.pw.data.all_measurements(max_box_distance_to_water=args.max_box_distance_to_water, min_measurements_correlations=args.min_measurements_correlations)
        all_values_dict = all_values_for_min_values(measurements_collection, normalize=args.normalize)
        logger.info(str(all_values_dict))
