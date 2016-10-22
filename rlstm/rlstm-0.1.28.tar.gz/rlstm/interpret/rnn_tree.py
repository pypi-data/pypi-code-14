"""
One way of interpreting a network is to pass the inputs
and predictions into a decision tree. Analyzing the branches
may provide some idea for the its decision function.

To help interpreting, we can show either
    1) the decision tree as a figure
    2) code w/ branching statements that represent the tree

"""

import pydotplus
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz, _tree
from rlstm.nn_util import flatten_io
from rlstm.common_util import np_safe_to_int

def train_decision_tree(func, model_weights, inputs):
    ''' Given a black box model with a prediction function,
        we can pass the (inputs, preds) into a decision
        tree.

        Args
        ----
        func : python hashable function
               This function accepts <inputs>
        model_weights : np array
                        trained nn weights
        inputs : np array
                 training inputs

        Returns
        -------
        Decision tree

    '''
    outputs = func(model_weights, inputs)
    tree = DecisionTreeClassifier()

    inputs = np_safe_to_int(inputs)
    outputs = np_safe_to_int(outputs)

    if len(inputs.shape) > 2:
        inputs, outputs = flatten_io(inputs, outputs)

    tree.fit(inputs.T, outputs.T)
    return tree


def visualize_tree(tree,
                   feature_names=None,
                   target_names=None,
                   save_path=None,
                   notebook_display=False):
    ''' Create a png of the tree branching

        Args
        ----
        tree : sci-kit learn tree
        feature_names : list
                        list of features
        target_names : list
                       list of classes
        save_path : string (None default)
                    where to save the file (png)

    '''
    if feature_names is None:
        num_features = len(tree.feature_importances_)
        feature_names = ['feat-{}'.format(i+1) for i in range(num_features)]

    if target_names is None:
        num_targets = len(tree.classes_)
        target_names = ['out-{}'.format(i+1) for i in range(num_targets)]

    dot_data = export_graphviz(tree,
                               out_file=None,
                               feature_names=feature_names,
                               class_names=target_names,
                               filled=True,
                               rounded=True,
                               special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)

    if not save_path is None:
        graph.write_pdf(save_path)

    if notebook_display:
        from IPython.display import Image
        Image(graph.create_png())


def interpret_tree(tree, feature_names=None):
    ''' Given an sci-kit learn decision tree, return "code"
        that's basically just fancy if/else statements

        Based on work here:
        http://stackoverflow.com/questions/20224526/..
        how-to-extract-the-decision-rules-from-scikit-learn-decision-tree

        Args
        ----
        tree : sci-kit learn object
        feature_names : list
                        list of features

        Returns
        -------
        rules : string
                source code in Python

    '''
    def safe_str(x):
        return str(x).replace('\n', ' ')

    if feature_names is None:
        num_features = len(tree.feature_importances_)
        feature_names = ['feat_{}'.format(i+1) for i in range(num_features)]

    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree.tree_.feature
    ]
    print('def tree({}):'.format(', '.join(feature_names)))

    def recurse(node, depth):
        indent = "    " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print "{}if {} <= {}:".format(indent, name, threshold)
            recurse(tree_.children_left[node], depth + 1)
            print "{}else:  # if {} > {}".format(indent, name, threshold)
            recurse(tree_.children_right[node], depth + 1)
        else:
            print "{}return {}".format(indent, safe_str(tree_.value[node]))

    recurse(0, 1)
