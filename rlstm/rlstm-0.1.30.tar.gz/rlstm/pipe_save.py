import os
import copy
import shutil
import dill
import json
import cPickle
import numpy as np
from rlstm.pipeline import RLSTMNode, RLSTMPipeline
from rlstm.common_util import (is_json_serializable, is_numpy_array,
                               is_pickle_serializable, get_timestamp)

class Marmalade(object):
    ''' Like a Pickle or JSON but only for RLSTMNode and
        RLSTMPipeline objects
    '''

    @classmethod
    def serialize(cls, object, output_file):
        if isinstance(object, RLSTMPipeline):
            with open(output_file, 'w') as fp:
                cls.serialize_pipe(object, fp)
        elif isinstance(object, RLSTMNode):
            with open(output_file, 'w') as fp:
                cls.serialize_node(object, fp)
        else:
            with open(output_file, 'w') as fp:
                cPickle.dump(object, fp)

    @classmethod
    def serialize_pipe(cls, pipe, fp):
        ''' An entire pipeline can be saved as a large JSON object.
            Calling this function will serialize each node in turn

            The structure will look like the following:

            {
                'dataset': ...,
                'log_file': ...,
                'weights_file': ...,
                'num_nodes': ...,
                'node_0': {...},
                'node_1': {...},
                ...
            }
        '''
        output = {}
        output['dataset'] = pipe.dataset
        output['log_file'] = pipe.log_file
        output['weights_file'] = pipe.weights_file
        output['num_nodes'] = pipe.num_nodes

        index = 0
        node = pipe.head
        while node:
            node_json = cls.serialize_node(node, fp, return_string=True)
            output["node_{}".format(index)] = node_json
            node = node.next
            index += 1

        json.dump(output, fp,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))
        return

    @classmethod
    def unserialize_pipe(cls, fp):
        ''' deserializes a pipe and returns a RLSTMPipeline object '''
        input_json = json.load(fp)
        pipeline = RLSTMPipeline(input_json['dataset'],
                                 input_json['log_file'],
                                 input_json['weights_file'])
        num_nodes = input_json['num_nodes']

        for node_i in range(num_nodes):
            node = input_json['node_{}'.format(node_i)]
            node_params = cls._unserialize_node_params(node['params'])
            pipeline.add_node(node['name'],
                              node['type'],
                              model_params=node_params)

        return pipeline

    @classmethod
    def serialize_node(cls, node, fp, return_string=False):
        ''' Convert node into a json of the following format

            {
                'name': ...,
                'index': ...,
                'type': ...,
                'prev': ...,
                'next': ...,
                ...
                **kwparams,
            }

            - np.arrays will be stored as a path to a numpy serialization
            - Normal types will be stored retringgularly in JSON
            - All other types will be stored as a path to a pickle serialization
        '''

        # safely define/create a folder that all nodes will write to
        output_file = '{}_{}'.format('_marma_node_files', get_timestamp(True))
        intermediate_folder = os.path.join(os.path.dirname(fp.name), output_file)

        if not os.path.isdir(intermediate_folder):
            os.mkdir(intermediate_folder)

        node_json = {}
        node_json['name'] = node.name
        node_json['index'] = node.index
        node_json['type'] = node.type
        # node_json['prev'] = (node.prev.index, node.prev.name)
        # node_json['next'] = (node.next.index, node.next.name)

        params_json = {}
        for param in node.params:
            if is_json_serializable(node.params[param]):
                params_json[param] = node.params[param]
            elif is_numpy_array(node.params[param]):
                param_id = '_marmalade_{name}_{id}_{param}.npy'.format(
                    name=node.name, id=node.index, param=param)
                param_path = os.path.join(intermediate_folder, param_id)
                np.save(param_path, node.params[param])
                params_json[param] = param_path
            elif is_pickle_serializable(node.params[param]):
                param_id = '_marmalade_{name}_{id}_{param}.pkl'.format(
                    name=node.name, id=node.index, param=param)
                param_path = os.path.join(intermediate_folder, param_id)
                with open(param_path, 'w') as pfp:
                    cPickle.dump(node.params[param], pfp)
                params_json[param] = param_path
            else:
                param_id = '_marmalade_{name}_{id}_{param}.dill'.format(
                    name=node.name, id=node.index, param=param)
                param_path = os.path.join(intermediate_folder, param_id)
                with open(param_path, 'w') as pfp:
                    dill.dump(node.params[param], pfp)
                params_json[param] = param_path

        node_json['params'] = params_json
        if not return_string:
            json.dump(node_json, fp,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))
            return
        return node_json

    @classmethod
    def unserialize_node(cls, fp):
        ''' deserializes a node and returns a RLSTMNode object '''
        input_json = json.load(fp)
        node_params = cls._unserialize_node_params(input_json['params'])
        node = RLSTMNode(input_json['name'],
                         input_json['type'],
                         input_json['index'],
                         None,
                         None,
                         model_params=node_params)
        return node

    @classmethod
    def _unserialize_node_params(cls, params):
        ''' Load the numpy and cpickle files as needed '''
        for param in params:
            cur_param = str(params[param])
            if len(cur_param) > 4:
                if cur_param[-4:] == '.npy':
                    cur_param = np.load(cur_param)
                    params[param] = cur_param
                elif cur_param[-4:] == '.pkl':
                    with open(cur_param) as pfp:
                        cur_param = cPickle.load(pfp)
                        params[param] = cur_param
                elif cur_param[-5:] == '.dill':
                    with open(cur_param) as pfp:
                        cur_param = dill.load(pfp)
                        params[param] = cur_param
        return params
