import os
import shutil
import cPickle
import numpy as np
from rlstm.pipeline import RLSTMNode, RLSTMPipeline
from rlstm.common_util import (is_serializable, is_numpy_array, get_timestamp)

class Marmalade(object):
    ''' Like a Pickle or JSON but only for RLSTMNode and
        RLSTMPipeline objects
    '''

    def serialize(self, object, output_file):
        if isinstance(object, RLSTMPipeline):
            with open(output_file, 'w') as fp:
                self.serialize_pipe(object, fp)
        elif isinstance(object, RLSTMNode):
            with open(output_file, 'w') as fp:
                self.serialize_node(object, fp)
        else:
            with open(output_file, 'w') as fp:
                cPickle.dump(object, fp)

    def serialize_pipe(self, pipe, fp=None):
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
            node_json = node.serialize()
            output["node_{}".format(index)] = node_json
            node = node.next
            index += 1

        if fp:
            json.dump(output, fp,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))
            return
        return output

    def unserialize_pipe(self, fp):
        ''' deserializes a pipe and returns a RLSTMPipeline object '''
        input_json = json.load(fp)
        pipeline = RLSTMPipeline(input_json['dataset'],
                                 input_json['log_file'],
                                 input_json['weights_file'])
        num_nodes = input_json['num_nodes']
        pipline.num_nodes = num_nodes

        for node_i in in num_nodes:
            node = input_json['node_{}'.format(node_i)]
            node_params = _unserialize_node_params(node['params'])
            pipeline.add_node(node['name'],
                              node['type'],
                              model_params=node_params)

        return pipeline

    def serialize_node(self, node, fp=None):
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

        base_folder = '.'
        if output_file:
            base_folder = os.path.basename(output_file)
        intermediate_folder = os.path.join(base_folder, get_timestamp(True))

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
            if is_serializable(node.params[param]):
                params_json[param] = node.params[param]
            elif is_numpy_array(node.params[param]):
                param_id = '_marmalade_{name}_{id}_{param}.npy'.format(
                    name=node.name, id=node.index, param=param)
                param_path = os.path.join(intermediate_folder, param_id)
                np.dump(param_path, node.params[param])
                params_json[param] = param_path
            else:
                param_id = '_marmalade_{name}_{id}_{param}.pkl'.format(
                    name=node.name, id=node.index, param=param)
                param_path = os.path.join(intermediate_folder, param_id)
                cPickle.dump(node.params[param], open(param_path, 'w'))
                params_json[param] = param_path

        node_json['params'] = params_json
        if fp:
            json.dump(node_json, fp,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))
            return
        return node_json

    def unserialize_node(self, fp):
        ''' deserializes a node and returns a RLSTMNode object '''
        input_json = json.load(fp)
        node_params = _unserialize_node_params(input_json['params'])
        node = RLSTMNode(input_json['name'],
                         input_json['type'],
                         input_json['index'],
                         None,
                         None,
                         model_params=node_params)

    def _unserialize_node_params(self, params):
        ''' Load the numpy a cpickle files as needed '''
        for param in params:
            if is_numpy_array(params[param]):
                params[param] = np.load(params[param])
            else:
                with open(params[param]) as pfp:
                    params[param] = cPickle.load(pfp)
        return params
