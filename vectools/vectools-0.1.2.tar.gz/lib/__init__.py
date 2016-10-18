# This file controls which input names call which functions.

from lib import normalization, mathematics, manipulation, analysis, descriptor_CLI_interfaces, supervised_learning, \
    unsupervised_learning, graph

__version__ = '0.1'

__all__ = [
    "normalization",
    "mathematics",
    "manipulation",
    "analysis",
    "descriptor_CLI_interfaces",
    "supervised_learning",
    "unsupervised_learning",
    "graph",
]

operations_dict = {
    "Normalization": {
        "zscorenorm":   normalization.zscorenorm,
        "quantnorm": normalization.quantilenorm,
        "medpolish": normalization.medianpolish
    },
    "Math": {
        "add": mathematics.add,
        "subtract": mathematics.subtract,
        "multiply": mathematics.multiply,
        # @TODO: Change these to overload the matrix operations
        # add_scalar --> add --scalar
        # "add_scalar": mathematics.addscalar,
        # "multiply_scalar": mathematics.multiplyscalar,
        "dot_product": mathematics.dotproduct,
        "inverse": mathematics.inverse,
        "determinant": mathematics.determinant,
        "eigenvec": mathematics.eigenvectors,
        "eigenvalues": mathematics.eigenvalues,
        "sum": mathematics.sumup
    },
    "Manipulation": {
        "append": manipulation.append_values_to,
        "format": manipulation.format_vec,
        #"to_svmlight": manipulation.to_svmlight,
        #"svml_to_csv": manipulation.to_csv,
        "chop": manipulation.chop,
        "concat": manipulation.concatenate,
        #"creatematrix": creatematrix,
        "join": manipulation.join,
        #"makeaddable": makeaddable,
        "setgrep": manipulation.setgrep,
        "slice": manipulation.vec_slice,
        "sort": manipulation.vecsort,
        "transpose": manipulation.transpose,
        "unique": manipulation.unique
        # "append_matrix": append_matrix,
        # "max": colmax,
    },
    "Analysis and Statistics": {
        #"columnstats": columnstats,
        #"runLDA": runLDA,
        #"pearson": pearson,
        "min": analysis.minimum,
        "max": analysis.maximum,
        "median": analysis.median,
        "sd": analysis.sd,
        "mean": analysis.average,
        "percentile": analysis.percentile,
        "pearson": analysis.pearson_group,
        "pca": analysis.run_pca,
        "spearman": analysis.spearman,
        "confmat": analysis.confusionmatrix,
    },
    "Descriptors": {
        "ncomp":  descriptor_CLI_interfaces.ncomposition_command_line,
        "splitncomp": descriptor_CLI_interfaces.split_ncomposition_command_line,
        "physchem": descriptor_CLI_interfaces.physicochemical_properties_ncomposition_command_line,
        "geary": descriptor_CLI_interfaces.geary_autocorrelation_command_line,
        "moreaubroto": descriptor_CLI_interfaces.normalized_moreaubroto_autocorrelation_command_line,
        "moran": descriptor_CLI_interfaces.moran_autocorrelation_command_line,
        "pseudoaac": descriptor_CLI_interfaces.pseudo_amino_acid_composition_command_line,
        "seqordercoupling": descriptor_CLI_interfaces.sequence_order_coupling_number_total_command_line,
        "quasiseqorder": descriptor_CLI_interfaces.quasi_sequence_order_command_line,
        "summary": analysis.summary
    },
    "Supervised Learning": {
        "svmtrain": supervised_learning.svmtrain,
        "svmclassify": supervised_learning.svmclassify,
        "linreg": supervised_learning.linearregression,
        "neuralnet": supervised_learning.neuralnetwork,
        "randforest": supervised_learning.randomforest
    },
    "Unsupervised Learning": {
        "dbscan": unsupervised_learning.DBSCAN,
        "kmeans": unsupervised_learning.kmeans,
        "silscore": unsupervised_learning.silhouette_score,
    },
    "Graph Operations": {
        "edges": graph.listedges,
        "addedge": graph.addedge,
        "addnode":  graph.addnode,
        "paths": graph.listpaths,
        "graphformat": graph.graphformat,
    }
}