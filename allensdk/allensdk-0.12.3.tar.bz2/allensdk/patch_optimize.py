import allensdk.internal.model.biophysical.optimize as opt
import allensdk.internal.model.biophysical.fit_stage_1 as fit_stage_1
import allensdk.internal.model.biophysical.fit_stage_2 as fit_stage_2
from allensdk.internal.api.queries.optimize_config_reader import OptimizeConfigReader
from allensdk.internal.api.queries.biophysical_module_reader import BiophysicalModuleReader
from mock import Mock

opt.DEFAULT_NGEN = 5
opt.DEFAULT_MU = 12
fit_stage_1.DEFAULT_NUM_PROCESSES = 24
fit_stage_2.DEFAULT_NUM_PROCESSES = 24
OptimizeConfigReader.lims_working_directory = \
    lambda self: '/local1/tmp'
BiophysicalModuleReader.sweep_numbers = Mock(return_value=[5])
