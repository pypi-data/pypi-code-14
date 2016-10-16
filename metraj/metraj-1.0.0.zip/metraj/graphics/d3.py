"""
Some d3 trajectory plots (with networkx)
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from util import RandomColor

import matplotlib as mpl
# mpl.rcParams["savefig.dpi"] = 50


def simple_nx_trajectory(frame, node_size=10, figsize=50, show=True, newfig=True, ax=None):
    """
    Construct a networkx graph from the trajectory and plot it using matplotlib (not d3)

    :param frame: Trajectory
    :return: figure
    """

    # First construct the graph; each node is connected only the next one
    G = nx.Graph()
    n = len(frame)
    for i in range(n-1):
        G.add_edge(i, i+1)

    # generate plot
    if newfig:
        plt.figure(figsize=(figsize, figsize))

    if ax is None:
        ax = plt.gca()

    nx.draw(G, pos=frame[list(frame.geo_cols)].values, node_size=node_size, node_color=np.random.rand(3,1), ax=ax)

    if show:
        plt.show()


def simple_d3_trajectory(frame):
    pass


def simple_nx_segmented_trajectory(frame, ax=None):

    # First construct the graph; each node is connected only the next one
    G = nx.Graph()
    n = len(frame)
    for i in range(n - 1):
        G.add_edge(i, i + 1)

    if ax is None:
        ax = plt.gca()

    # Draw nodes and edges seperately
    pos = frame[list(frame.geo_cols)].values
    node_sizes = (frame["DBSCAN_n"].values > 500) * 10

    color = RandomColor.sample_map()

    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=node_sizes, linewidths=0, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=color, ax=ax, alpha=.6)


def nx_trajectory(frame, ax=None, node_sizes=10, static_node_size=20, cmap='jet'):

    # First construct the graph; each node is connected only the next one
    G = nx.Graph()
    n = len(frame)
    for i in range(n - 1):
        G.add_edge(i, i + 1)

    if ax is None:
        ax = plt.gca()

    # Draw nodes and edges seperately
    pos = frame[list(frame.geo_cols)].values

    if node_sizes is None:
        node_sizes = (frame["DBSCAN_n"].values > 500) * static_node_size

    # color = RandomColor.sample_map(cmap=plt.cm.get_cmap(cmap))
    color = RandomColor.sample_rgb()

    nx.draw_networkx_nodes(G, pos, node_color=color, node_size=node_sizes, linewidths=0, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=color, ax=ax, alpha=.85)


def intensity_map(frames, nbins=200, figsize=20):
    plt.figure(figsize=(figsize, figsize), facecolor='black')
    plt.axis('off')

    pos = np.vstack((frame[list(frame.geo_cols)].values for frame in frames))
    hist, xedges, yedges = np.histogram2d(pos[:, 0], pos[:, 1], bins=nbins)

    plt.imshow(hist, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], cmap=plt.get_cmap('hot'), norm=LogNorm())
    plt.savefig("C:\\temp\\heat.png", facecolor="black")
    plt.savefig("C:\\temp\\heat.pdf", facecolor="black")