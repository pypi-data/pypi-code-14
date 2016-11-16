''' Run a quick example pipeline and see if the
    pipeline can be loaded and saved correctly
    with Marmalade
'''

import os
import shutil
import unittest
import tempfile
import autograd.numpy as np

from rlstm.pipe_save import Marmalade
from rlstm.pipeline import RLSTMPipeline
from rlstm.common_util import is_numpy_array, is_function
import rlstm.datasets

class TestMarmalade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestMarmalade, cls).setUpClass()

        pipeline = RLSTMPipeline(
            os.path.abspath(os.path.dirname(rlstm.datasets.__file__)))
        pipeline.add_node('gru-hmm',
                          'gru-hmm',
                          {'hmm_state_count':5,
                           'gru_state_count':5,
                           'min_iters':1,
                           'max_iters':5,
                           'batch_size':64,
                           'param_scale':0.01,
                           'stop_criterion':1e-3,
                           'early_stop':False,
                           'has_va_set':False})

        pipeline.run_and_eval()
        cls.pipe = pipeline
        cls.node = pipeline.get_node(index=0)

        if not os.path.isdir('_marmalade_tests_folder'):
            os.mkdir('_marmalade_tests_folder')

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir('_marmalade_tests_folder'):
            shutil.rmtree('_marmalade_tests_folder')

    def test_marmalade_pipeline(self):
        node = self.node
        pipe = self.pipe

        with open('pipe.marma', 'w') as fp:
            Marmalade.serialize_pipe(pipe, fp)

        with open('pipe.marma') as fp:
            reload_pipe = Marmalade.unserialize_pipe(fp)
            reload_node = reload_pipe.get_node(index=0)

            self.assertEqual(reload_pipe.num_nodes, pipe.num_nodes)
            self.assertEqual(reload_pipe.log_file, pipe.log_file)
            self.assertEqual(reload_pipe.weights_file, pipe.weights_file)
            self.assertEqual(reload_pipe.dataset, pipe.dataset)
            self.assertEqual(reload_pipe.obs_count, pipe.obs_count)
            self.assertEqual(reload_pipe.out_count, pipe.out_count)

            self.assertEqual(reload_node.name, node.name)
            self.assertEqual(reload_node.index, node.index)
            self.assertEqual(reload_node.prev, node.prev)
            self.assertEqual(reload_node.next, node.next)
            self.assertEqual(reload_node.type, node.type)

            for param in reload_node.params:
                if is_numpy_array(reload_node.params[param]):
                    self.assertEqual(
                        np.sum(~(reload_node.params[param] == node.params[param])), 0)
                elif not is_function(reload_node.params[param]):
                    self.assertEqual(reload_node.params[param], node.params[param])
                else:  # function
                    self.assertEqual(reload_node.params[param].__code__.co_code,
                                     node.params[param].__code__.co_code)

    def test_marmalade_node(self):
        node = self.node

        with open('_marmalade_tests_folder/node.marma', 'w') as fp:
            Marmalade.serialize_node(self.node, fp)

        with open('_marmalade_tests_folder/node.marma') as fp:
            reload_node = Marmalade.unserialize_node(fp)

            self.assertEqual(reload_node.name, node.name)
            self.assertEqual(reload_node.index, node.index)
            self.assertEqual(reload_node.prev, node.prev)
            self.assertEqual(reload_node.next, node.next)
            self.assertEqual(reload_node.type, node.type)

            for param in reload_node.params:
                if is_numpy_array(reload_node.params[param]):
                    self.assertEqual(
                        np.sum(~(reload_node.params[param] == node.params[param])), 0)
                elif not is_function(reload_node.params[param]):
                    self.assertEqual(reload_node.params[param], node.params[param])
                else:  # function
                    self.assertEqual(reload_node.params[param].__code__.co_code,
                                     node.params[param].__code__.co_code)
