"""
This module contains functions related to unsupervised learning.
"""
import argparse
import sys
import numpy as np
from lib.inputoutput import ParseVectors
from lib.inputoutput import outputvector
from lib.inputoutput import ParseFasta
from lib.inputoutput import VectorFormats
from lib.inputoutput import ParseVectors, _shared_params, _slice_list


def kmeans(parser):
    """ Preforms k-means clustering on a set of vectors.

    :param parser:
    :return:
    """

    from sklearn.cluster import KMeans

    parser.add_argument(
        'infile',
        nargs='?',
        type=str,
        default="sys.stdin"
    )

    parser.add_argument(
        '-v', "--print-input-vectors",
        action="store_true",
        help='Print the vectors after their class assignments.'
    )

    parser.add_argument(
        '-k',
        required=True,
        type=int,
        help=''
    )

    parser.add_argument(
        '-rs', '--random-state',
        type=int,
        default=None,
        help=''
    )

    _shared_params(parser, only_apply_on=True)

    args = parser.parse_args()

    # Parse the vectors
    vector_parser = ParseVectors(
        file_name=args.infile,
        has_col_names=args.column_titles,
        has_row_names=args.row_titles,
        delimiter=args.delimiter,
        only_apply_on_columns=args.only_apply_on
    )
    vectors = vector_parser.parse()

    # Predict cluster memberships.
    y_pred = KMeans(n_clusters=args.k, random_state=args.random_state).fit_predict(vectors)  #

    #
    labled_vectors = []
    for i in range(len(vectors)):
        labled_vectors.append(np.insert(vectors[i], 0, y_pred[i]))

    ParseVectors("").out(
        labled_vectors,
        column_titles=vector_parser.col_titles,
        row_titles=vector_parser.row_titles
    )


def silhouette_score(parser):
    """ Calculate the silhouette score of a set of clusters.

    Input all as one vector
    OR
    as a label vector and main vector

    :param parser:
    :return:
    """
    from sklearn.metrics import silhouette_score

    # metrics.silhouette_score
    #parser.add_argument(
    #    'infile',
    #    nargs='?',
    #    type=str,
    #    default="sys.stdin"
    #)

    parser.add_argument(
        '--labels',
        type=str,
        help="The labels assigning vectors to classes.",
        default=None
    )

    parser.add_argument(
        '--vectors',
        type=str,
        help="Vectors that have been assigned to classes.",
        default=None
    )

    _shared_params(parser, only_apply_on=True)

    args = parser.parse_args()

    lable_parser = ParseVectors(
        file_name=args.labels,
        has_col_names=False,  #  args.column_titles,
        has_row_names=False,  #  args.row_titles,
        delimiter=args.delimiter,
        only_apply_on_columns=args.only_apply_on
    )
    labels = lable_parser.parse()
    labels = np.array([x[0] for x in labels])

    vector_parser = ParseVectors(
        file_name=args.vectors,
        has_col_names=False,  #  args.column_titles,
        has_row_names=False,  #  args.row_titles,
        delimiter=args.delimiter,
        only_apply_on_columns=args.only_apply_on
    )
    vectors = vector_parser.parse()

    sil_score_obj = silhouette_score(
        vectors,
        labels,
        metric='euclidean',
        # sample_size=sample_size
    )

    print(sil_score_obj)


def som():
    # TODO
    x = 0


def heirarchicalcluster():
    # TODO
    x = 0
    # http://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering
    # http://scikit-learn.org/stable/auto_examples/cluster/plot_ward_structured_vs_unstructured.html
    # ward = AgglomerativeClustering(n_clusters=6, linkage='ward').fit(X)
    # ward = AgglomerativeClustering(n_clusters=6, connectivity=connectivity, linkage='ward').fit(X)
    pass


def DBSCAN(parser):
    """ Preforms density based clustering of a set of vectors.

    :param parser:
    :return:
    """
    _shared_params(parser)

    from sklearn.cluster import DBSCAN
    from sklearn import metrics
    from sklearn.datasets.samples_generator import make_blobs
    from sklearn.preprocessing import StandardScaler

    ##############################################################################
    # Generate sample data
    centers = [[1, 1], [-1, -1], [1, -1]]

    X, labels_true = make_blobs(
        n_samples=750,
        centers=centers,
        cluster_std=0.4,
        random_state=0)

    # print(X)

    for el in X:
        print(el)
    """
    X = StandardScaler().fit_transform(X)
    ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    """
