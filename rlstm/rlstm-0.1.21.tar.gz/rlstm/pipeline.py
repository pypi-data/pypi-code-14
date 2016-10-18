'''
pipeline.py

runs all models (or a subset) for a specified dataset.
parameters are customizable. This is a work in progress
and should be modularized such that pieces can be put in
and taken out with ease.

available models:
    - lr
    - hmm by ffbs
    - hmm by sgd
    - gru
    - gru hmm

available cost functions
    - obs-out trade-off

available regularization
    - redun
    - kdropout
    - l1

'''
from __future__ import print_function

import os
import sys
import cPickle
import numpy as np
from datetime import datetime
from rlstm import models_util as util
from rlstm.scores import get_log_sparsity, get_accuracy, get_auc
from rlstm.common_util import flatten_to_2d, merge_two_dicts, pp_json
from copy import copy


def get_relevant_args(func, unused_set=None):
    unused_set = set(unused_set)
    args = set(func.func_code.co_varnames[:func.func_code.co_argcount])
    return list(args - unused_set)


class RLSTMShareWeights(object):
    ''' Define a system to transfer weights from a previous node
        to a latter node at pipeline execution.
    '''

    def __init__(self,
                 parent_name,
                 parent_weights_attr='init_weights',
                 parent_weights_idx=None):
        self.parent_name = parent_name
        self.parent_weights_attr = parent_weights_attr
        self.parent_weights_idx = parent_weights_idx

    def get_parent_weights(self, pipeline):
        weights = pipeline.get_node(self.parent_name).params['trained_weights']
        if not self.parent_weights_idx is None:
            return weights[self.parent_weights_idx.astype(int)]
        return weights


class RLSTMNode(object):

    ''' Doubly linked set for declaring execution pieces.
    return list(args - irrelevant)
    '''
    def __init__(self,
                 model_name,
                 model_class,
                 index,
                 prev,
                 next,
                 model_params=None):

        self.name = model_name
        self.index = index
        self.prev = prev
        self.next = next
        self.type = model_class

        if model_class == 'lr':
            func = util.train_lr
        elif model_class == 'hmm-ffbs':
            func = util.train_hmm_ffbs
        elif model_class == 'hmm-sgd':
            func = util.train_hmm_sgd
        elif model_class == 'gru':
            func = util.train_gru
        else:
            func = util.train_gru_hmm
        self.func = func

        params = self.default_params()
        if model_params:
            for key in model_params:
                params[key] = model_params[key]

        self.params = params
        self.unused_params = ['obs_set',
                              'out_set',
                              'va_obs_set',
                              'va_out_set']

    def default_params(self):
        params = dict()
        params['min_iters'] = 1
        params['max_iters'] = 10000
        params['batch_size'] = 128
        params['param_scale'] = 0.01
        params['obs_lambda'] = 0
        params['l1_lambda'] = 0
        params['patience'] = 25
        params['early_stop'] = False
        params['stop_criterion'] = 1e-3
        params['has_out_set'] = True
        params['has_va_set'] = False
        params['gru_state_count'] = 50
        params['hmm_state_count'] = 5

        if self.type in ['gru', 'gru_hmm']:
            params['max_conn'] = 0
            params['redun_epsilon'] = 0

        return params

    def run(self, x, y=None, va_x=None, va_y=None):
        func = self.func
        keys = get_relevant_args(func, self.unused_params)
        used_params = dict((k, self.params[k]) for k in keys if k in self.params)
        if self.params['has_va_set']:
            used_params['va_obs_set'] = va_x
            used_params['va_out_set'] = va_y

        pred_fun, loglike_fun, weights = func(x, y, **used_params)

        self.params['pred_fun'] = pred_fun
        self.params['loglike_fun'] = loglike_fun
        self.params['trained_weights'] = weights

    def eval(self, tr_x, tr_y, te_x, te_y):
        metrics = dict()

        trained_weights = self.params['trained_weights']
        pred_fun = self.params['pred_fun']
        loglike_fun = self.params['loglike_fun']

        # loglikelihoods
        if self.type in ['lr', 'hmm-ffbs', 'hmm-sgd']:
            metrics['{}:tr_ll_obs'.format(self.name)] = \
                loglike_fun(trained_weights, tr_x, None)
            metrics['{}:te_ll_obs'.format(self.name)] = \
                loglike_fun(trained_weights, te_x, None)

        metrics['{}:tr_ll_out'.format(self.name)] = \
            loglike_fun(trained_weights, tr_x, tr_y)
        metrics['{}:te_ll_out'.format(self.name)] = \
            loglike_fun(trained_weights, te_x, te_y)

        # aucs
        tr_pr_set = pred_fun(trained_weights, tr_x)
        te_pr_set = pred_fun(trained_weights, te_x)

        tr_pr_set = tr_pr_set.reshape(tr_y.shape)
        te_pr_set = te_pr_set.reshape(te_y.shape)

        metrics['{}:tr_auc'.format(self.name)] = \
            get_auc(tr_y.flatten(), tr_pr_set.flatten())
        metrics['{}:te_auc'.format(self.name)] = \
            get_auc(te_y.flatten(), te_pr_set.flatten())

        # accuracy
        metrics['{}:tr_acc'.format(self.name)] = \
            get_accuracy(tr_y, tr_pr_set)
        metrics['{}:te_acc'.format(self.name)] = \
            get_accuracy(te_y, te_pr_set)

        # sparsity
        metrics['{}:sparsity'.format(self.name)] = \
            get_log_sparsity(trained_weights)

        pp_json(metrics)
        return metrics


class RLSTMPipeline(object):

    def __init__(self, dataset, log_file=None, weights_file=None):
        '''
            Args
            ----
            log_file : string
                       path to file to print training log to.
            weights_file : string
                           path to dir to save *npy and *pkl files.
        '''

        self.head = None
        self.tail = None
        self.num_nodes = 0

        self.log_file = log_file
        self.weights_file = weights_file
        self.dataset = dataset

        self.avail_models = ['lr',
                             'hmm-ffbs',
                             'hmm-sgd',
                             'gru',
                             'gru-hmm']

        (tr_obs_set, tr_out_set), (te_obs_set, te_out_set), \
            (va_obs_set, va_out_set) = self.load_data(dataset)

        self.data = ((tr_obs_set, tr_out_set),
                     (te_obs_set, te_out_set),
                     (va_obs_set, va_out_set))
        self.obs_count = tr_obs_set.shape[0]
        self.out_count = tr_out_set.shape[0]

        print('[{}] initialized pipeline'.format(datetime.now()))

    def load_data(self, dataset):
        self.dataset = dataset
        tr_obs_set = np.load(os.path.join(dataset, 'X_train.npy'))
        tr_out_set = np.load(os.path.join(dataset, 'y_train.npy'))
        te_obs_set = np.load(os.path.join(dataset, 'X_test.npy'))
        te_out_set = np.load(os.path.join(dataset, 'y_test.npy'))

        va_obs_set = None
        va_out_set = None

        if os.path.isfile(os.path.join(dataset, 'X_valid.npy')):
            va_obs_set = np.load(os.path.join(dataset, 'X_valid.npy'))
        if os.path.isfile(os.path.join(dataset, 'y_valid.npy')):
            va_out_set = np.load(os.path.join(dataset, 'y_valid.npy'))

        return (tr_obs_set, tr_out_set), (te_obs_set, te_out_set), \
            (va_obs_set, va_out_set)

    def get_node(self, name=None, index=None):
        ''' Select a node (if exists) based on name or index

            Args
            ----
            name: string
                  name of node to select
            index: integer
                   index of node to select

            Returns
            -------
            node: RLSTMNode object
        '''

        if not name and not index:
            return None

        node = self.head
        while node:
            if name and index:
                if node.name == name and node.index == index:
                    return node
            elif name:
                if node.name == name:
                    return node
            else:
                if node.index == index:
                    return node

            node = node.next
        return None

    def add_node(self, model_name, model_class, model_params=None):
        ''' Appends new model to end of file (or loc if specified)

            Args
            ----
            model_name: string
                        name of current node
            model_class: string
                        must be in 'avail_models'
            loc: integer
                 index of node. defaults last
        '''

        if not model_class in self.avail_models:
            return ValueError('model class {} not recognized.'.format(model_class))

        new_node = RLSTMNode(model_name,
                             model_class,
                             self.num_nodes,
                             None,
                             None,
                             model_params=model_params)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

        self.num_nodes += 1

        print('[{}] added new node {}. Total: {} nodes.'.format(
            datetime.now(), model_name, self.num_nodes))

    def run_and_eval(self):
        ''' Runs the entire pipeline. Each node is assumed
            to be a well built model, and is run in turn.
        '''

        print('[{}] executing pipeline'.format(datetime.now()))

        # grab the loaded data
        ((tr_obs_set, tr_out_set),
         (te_obs_set, te_out_set),
         (va_obs_set, va_out_set)) = self.data

        node = self.head
        while node:
            # check params for RLSTMShareWeights object
            # if so, replace w/ new weights
            for param in node.params:
                param_obj = node.params[param]
                if isinstance(param_obj, RLSTMShareWeights):
                    print('[{}] using parent ({}) weights'.format(
                        datetime.now(), param_obj.parent_name))
                    node.params[param] = param_obj.get_parent_weights(self)

            print('[{}] executing node ({})'.format(datetime.now(), node.name))
            if node.params['has_out_set']:
                node.run(tr_obs_set, tr_out_set, va_obs_set, va_out_set)
            else:
                node.run(tr_obs_set, None, va_obs_set, None)

            node = node.next

        node = self.head
        all_metrics = {}
        while node:
            node_metrics = node.eval(tr_obs_set,
                                     tr_out_set,
                                     te_obs_set,
                                     te_out_set)

            all_metrics = merge_two_dicts(all_metrics, node_metrics)
            node = node.next

        if self.log_file:
            with open(self.log_file, 'w') as f:
                print(all_metrics, file=f)

    def save_weights(self):
        ''' to be used after run(). '''
        print('[{}] saving pipeline weights'.format(datetime.now()))

        w_dict = {}

        node = self.head
        while node:
            w_dict[node.name] = node.params['trained_weights']
            node = node.next

        if self.weights_file:
            cPickle.dump(w_dict, open(self.weights_file, 'w'))
