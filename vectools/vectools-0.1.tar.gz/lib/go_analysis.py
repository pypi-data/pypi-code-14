import sys
from lib.inputoutput import outputvector
import numpy as np


def gojson2vector(parser):
    """transforms json file containing go dag to adjacency matrix.

    :return:
    """
    parser.add_argument('json', nargs='?', type=str, help='JSON file (Look at https://github.com/berkeleybop/bbop-js/wiki/Graph for how to make a graph), default: STDIN', default="sys.stdin")

    args = parser.parse_args()
    data = _parse_json(args.json)
    adjacency_matrix = np.empty((len(data["nodes"]), len(data["nodes"])), dtype=object)
    nodes = []
    nodes_dict = {}
    for node in data["nodes"]:
        nodes.append(node["id"])

    for i in range(len(nodes)):
        nodes_dict[nodes[i]] = i

    for edge in data["edges"]:
        obj = nodes_dict[edge["obj"]]
        sub = nodes_dict[edge["sub"]]
        pred = edge["pred"]
        adjacency_matrix[obj][sub] = pred

    outputvector(adjacency_matrix, [""] + nodes, nodes)


def _parse_json(filename):
    """
    Function to parse json file or stdin
    :param filename: file to parse, can be sys.stdin as string
    :return: data of the json file
    """
    import json
    if filename != "sys.stdin":
        file = open(filename,'r')
    else:
        file = sys.stdin
    data = json.load(file)
    return data