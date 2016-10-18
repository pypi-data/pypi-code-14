import numpy as np
from lib.inputoutput import vecparse, outputvector
from lib.inputoutput import ParseVectors
from lib.inputoutput import COLUMN_TITLE_FOR_OUTPUT_MATRICES as standard_col_title
import pickle
import argparse

ROUNDTO = 5


def _shared_params(parser, enable_column_titles=True, enable_row_titles=True, enable_delimiter=True, round_to=True):
    """ This function stores basic arguments used in almost every other function.

    :param parser: An argparse object.
    :return: Does not return anything, however, adds variables to the argparse object.
    """
    if enable_column_titles:
        parser.add_argument('-c', "--column-titles",
                            action="store_true",
                            help='The matrix has column titles.')

    if enable_row_titles:
        parser.add_argument('-r', "--row-titles",
                            action="store_true",
                            help='row titles are defined')

    if enable_delimiter:
        parser.add_argument('-d', "--delimiter",
                            nargs='?',
                            default="\t",
                            help='sequence of characters the columns are separated. default: <TAB>')

    if round_to:
        parser.add_argument(
            "--round-to",
            type=int,
            default=5,
            help='The number of decimal places to round to .')


def _generateparamgrid(kernal_name, C_range, gamma_range, degree_range, coef0_range):
    """ This function handles generating a parameter grid for the grid search from the command line input.

    :param kernal_name: A valid kernel name (str).
    :param C_range: The range of C values (string delimited with commas).
    :param gamma_range: The range of gamma values (list of floats).
    :param degree_range: The range of degree values (list of integers).
    :param coef0_range: The range of coef0 values (list of floats).
    :return: A parameter grid dict inside a list.

    [{ 'C':      [0.001, 0.01, 0.1, 1, 10, 100],
       'gamma':  [0.001, 0.01, 0.1, 1, 10, 100],
        'coef0':  [0.1, 0.0, 1],
        'degree': [3, 4, 5, 6],
        'kernel': [ 'rbf']
    }]

        kernal_name=args.kernel,
        C_range=[float(f) for f in args.C.strip().split(",")],
        gamma_range=[float(f) for f in args.gamma.strip().split(",")],
        degree_range=[int(i) for i in args.degree.strip().split(",")],
        coef0_range=[float(f) for f in args.coef0.strip().split(",")]

    """
    # gammas = np.logspace(-6, -1, 10)
    param_grid = dict()

    if kernal_name == "linear":
        pass
    elif kernal_name == "poly":
        param_grid["degree"] = [degree_range]
        param_grid["coef0"] = [coef0_range]
    elif kernal_name == "rbf":
        param_grid["gamma"] = [float(f) for f in gamma_range.strip().split(",")]
    elif kernal_name == "sigmoid":
        param_grid["coef0"] = [coef0_range]
    else:
        assert False, "Error: Unknown kernal name."

    param_grid["C"] = [float(f) for f in C_range.strip().split(",")]
    param_grid["kernel"] = [kernal_name]
    #'poly',
    #'linear',
    # 'sigmoid'
    # poly   C,degree, coef0.
    # gamma  C, gamma .
    # sigmoid C, coef0.
    return [param_grid]


def _avaliblekernels():
    # @TODO: Get this info from the actually classification class.
    return ["rbf", "linear", "poly", "sigmoid"]



class BandwidthAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if values < 12:
            parser.error("Minimum bandwidth for {0} is 12".format(option_string))
            #raise argparse.ArgumentError("Minimum bandwidth is 12")

        setattr(namespace, self.dest, values)





def svmtrain(parser):
    """ Preforms k-fold testing followed by independent set testing on a set of training vectors.
        @TODO: It should be possible to generalize this function further. Think about a many vs many.
        1. Get positive set of vectors.
        2. Get a negative set of vectors.
        3. Assign lables to each.
        Ideal behavior
        output performance of each node in the grid.
        final line it the best parameter.
        many-vs-many possible?
        Find the parameters that make a good model and output them, also output model trained from these.
        Grid Search
            k-fold test & optimal parameter search.
        :return:
    """
    # http://stats.stackexchange.com/questions/95797/how-to-split-the-dataset-for-cross-validation-learning-curve-and-final-evaluat
    # http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV
    # http://scikit-learn.org/stable/modules/sgd.html
    positive_val = 0
    negative_val = 1

    # Get a list of available kernels.
    available_kernels = _avaliblekernels()
    # parser.add_argument('infile', nargs='?', type=str, default="sys.stdin")

    """
    parser.add_argument('--positive-set',
                        dest='positive_set',
                        type=str,
                        required=True,
                        help="Path to positive set vectors.")
    parser.add_argument('--negative-set',
                        dest='negative_set',
                        type=str,
                        required=True,
                        help="Path to negative set vectors.")
    """

    parser.add_argument(
        'datasets',
        metavar='datasets',
        type=str,
        nargs='+',
        help='Files containing vectors for training an SVM.')

    parser.add_argument('--independent-size',
                        dest='independent_size',
                        type=float,
                        default=0.1,
                        help="The percent to include in the test data set.")
    parser.add_argument('--folds',
                        dest='folds',
                        type=int,
                        default=5,
                        help="Number of folds for testing.")
    parser.add_argument('--seed',
                        dest='seed',
                        type=int,
                        default=0,
                        help="rand seed")
    # @TODO: Make default behavior iterate over all kernels ????
    parser.add_argument('--kernel',
                        dest='kernel',
                        type=str,
                        choices=available_kernels,
                        default=available_kernels[0],
                        help="Path to negative set vectors.")
    parser.add_argument('--model_name',
                        dest='model_name',
                        type=str,
                        default=False,
                        help="The base name for the model generated from testing.")

    parser.add_argument(
        '--metrics_file',
        dest='metrics_file',
        type=str,
        default=False,
        help="The name of file to output metrics to.")

    parser.add_argument(
        '--best_metric_file',
        dest='best_metric_file',
        type=str,
        default=False,
        help="The name of file to output data about the best metric to. If not provided printed to STOUT."
    )

    parser.add_argument('--C',
                        type=str,
                        required=False,
                        default="0.001,0.01,0.1,1,10,100",
                        help='Optional: A comma separated list of C values to grid search. Must be greater than 0. ')

    parser.add_argument('--gamma',
                        type=str,
                        required=False,
                        default="0.001,0.01,0.1,1,10,100",
                        help='Optional: A comma separated list of gamma values to grid search.')

    parser.add_argument('--coef0',
                        type=str,
                        required=False,
                        default="0.0,0.1,1",
                        help='Optional: A comma separated list of coef0 values to grid search.')

    parser.add_argument(
        '--degree',
        type=str,
        required=False,
        default="3,4,5,6",
        help='Optional: A comma separated list of degree values to grid search. Must be an integer greater than 1.')

    _shared_params(parser)
    args = parser.parse_known_args()[0]

    from sklearn.cross_validation import train_test_split
    from sklearn.cross_validation import KFold
    from sklearn.svm import SVC
    from sklearn.grid_search import GridSearchCV
    from sklearn.metrics import accuracy_score
    # @TODO: Add svmlight support.
    # from sklearn.datasets import dump_svmlight_file

    vector_list = []  # Store all class vectors in this list.
    id_list = []      # Store all class identities in this
    id_number = 0     # Tells which class id to use, is incremented by one for each class.
    int_to_name_dict = {}  # Use this to convert int ids to file names.

    # Iterate over all input matrices and add them to vector_list, also add each rows class identity to id_list.
    for file_name in args.datasets:

        matrix_obj = ParseVectors(
            file_name=file_name,
            has_col_names=args.column_titles,
            has_row_names=args.row_titles,  # Row titles should just be treated as normal columns.
            delimiter=args.delimiter)

        for row_id, row_vector in matrix_obj.generate(save_row_names=True):
            vector_list.append(row_vector)
            id_list.append(id_number)  # I would like to have names here, but it looks like these must be integers.
        # Increment for next class.

        int_to_name_dict.update({id_number: file_name})
        id_number += 1

    # Convert to numpy arrays.
    vector_array = np.array(vector_list)
    id_array = np.array(id_list)

    # Make training and test classes.
    x_train, x_test, y_train, y_test = train_test_split(
        vector_array,  # Vectors
        id_array,      # Labels
        test_size=args.independent_size,
        random_state=0
    )

    estimator = SVC()

    cross_validation_obj = KFold(
        len(x_train),
        n_folds=args.folds,
        shuffle=True,
        random_state=args.seed
    )

    # Make a grid search object, with desired ranges and kernels.
    param_grid = _generateparamgrid(
        kernal_name=args.kernel,
        C_range=args.C,
        gamma_range=args.gamma,
        degree_range=args.degree,
        coef0_range=args.coef0
    )

    classifier = GridSearchCV(
        estimator=estimator,
        cv=cross_validation_obj,
        param_grid=param_grid
    )

    classifier.fit(x_train, y_train)

    y_preds = classifier.predict(x_test)

    metrics_out_list = []
    for el in classifier.grid_scores_:
        tmp_metrics_out_list = ["mean_of_accuracy_score:%s" % str(round(el[1], ROUNDTO))]
        for key_el in el[0]:
            tmp_metrics_out_list.append(key_el+":%s" % el[0][key_el])
        metrics_out_list.append("\t".join(tmp_metrics_out_list))

    # Output metrics for model.
    if args.metrics_file:
        metrics_file_obj = open(args.metrics_file, 'w')
        metrics_file_obj.write("\n".join(metrics_out_list))
        metrics_file_obj.close()
    else:
        print("\n".join(metrics_out_list))

    # I am not sure which titles I want to use yet.
    best_metrics = [
        "Best_Model_Accuracy\t%s" % round(accuracy_score(y_test, y_preds), args.round_to),
        "Best_Model_Kernel\t%s" % classifier.best_estimator_.kernel,
        "Best_Model_C\t%s" % classifier.best_estimator_.C,
        "Best_Model_Gamma\t%s" % classifier.best_estimator_.gamma,
        "Best_Model_Epsilon\t%s" % classifier.best_estimator_.epsilon,
        "Best_Model_Coef0\t%s" % classifier.best_estimator_.coef0
    ]
    out_str = "\n".join(best_metrics)

    if args.best_metric_file:
        out_metrics_file_obj = open(args.best_metric_file, 'w')
        out_metrics_file_obj.write(out_str)
        out_metrics_file_obj.close()
    else:
        print(out_str)

    # Finally output the metrics file. I would like to use something other than a pickle, but I can't figure out
    # a good alternative. Also using the standard pickle instead of the sci-it learn as the sci-kit learn version
    # will output many files, whereas the, standard pickle only outputs one.
    # If a model name is provided, output a model file.
    # http://scikit-learn.org/stable/modules/model_persistence.html
    if args.model_name:
        with open(args.model_name, 'wb') as fid:
            classifier.best_estimator_.int_to_name_dict = int_to_name_dict
            pickle.dump(classifier.best_estimator_, fid)


def svmclassify(parser):
    """ Predicts the class of a set of unknown vectors using an SVM model.
    :return:
    """

    # @TODO: Add support for various methods for inputting models.
    parser.add_argument(
        "--model",
        dest="model",
        type=str,
        help="At the moment, needs a model file. ")

    parser.add_argument(
        'unknowns',
        metavar='unknowns',
        type=str,
        nargs='+',
        help='Files containing vectors to classify via SVM.')

    _shared_params(parser)
    args = parser.parse_known_args()[0]

    # Get model, for now this will be a pickle, however, I would like to change this to something safer.
    with open(args.model, 'rb') as pickle_file:
        clf = pickle.load(pickle_file)

    vector_list = []  # Store all class vectors in this list.
    combined_row_titles = []
    # Iterate over all input matrices and add them to vector_list, also add each rows class identity to id_list.

    out_matrix_obj = ParseVectors(
        file_name="",
        has_col_names=args.column_titles,
        has_row_names=args.row_titles,  # Row titles should just be treated as normal columns.
        delimiter=args.delimiter,
        only_apply_on_columns=None)

    # Since we are generating new columns here we must create the column names instead of parsing them.
    if args.column_titles:
        output_column_titles = []
        if args.row_titles:
            output_column_titles.append(standard_col_title)
        output_column_titles += ["Predicted_Class_ID", "Predicted_Class_Name"]

        out_matrix_obj.setcolumntitles(output_column_titles)

    for file_name in args.unknowns:

        matrix_obj = ParseVectors(
            file_name=file_name,
            has_col_names=args.column_titles,
            has_row_names=args.row_titles,  # Row titles should just be treated as normal columns.
            delimiter=args.delimiter,
            only_apply_on_columns=None)

        for row_title, row_vector in matrix_obj.generate():

            # Predict the class of the given vector.
            pred = clf.predict([row_vector])

            out_vec = [
                pred[0],                       # The integer id of the class.
                clf.int_to_name_dict[pred[0]]  # The text name of the class.
            ]

            out_matrix_obj.iterative_out(
                row_title=row_title,
                vector=out_vec,
                column_titles=out_matrix_obj.getcolumntitles(),
            )


def linearregression(parser):
    """ Preforms linear regression via least squares on a set of vectors.

    :param parser:
    :return:
    """
    from sklearn import datasets, linear_model

    parser.add_argument(
        'matrix',
        nargs='?',
        type=str,
        default="sys.stdin",
        help='matrix with training set. Last column has to be the target values. The others are training sets.',)

    parser.add_argument(
        '-p', '--prediction-set',
        type=str,
        help="Path to prediction set vectors.")

    parser.add_argument(
        '-c', "--column_titles",
        action="store_true",
        help='column titles are defined')

    parser.add_argument(
        '-r', "--row_titles",
        action="store_true",
        help='row titles are defined')

    parser.add_argument("--fast", action="store_true", help='As fast as it could be')

    parser.add_argument('-n', "--normalize", action="store_true", help='If the switch is set the values are normalized before the linear regression')
    parser.add_argument('-o', "--output-coefficients", action="store_true", help='write estimated coefficients on STDERR')
    args = parser.parse_args()
    matrix, column_titles, row_titles, m_type = vecparse(args.matrix, args.column_titles, args.row_titles)
    prediction, column_titles2, row_titles2, m_type2 = vecparse(args.prediction_set, args.column_titles, args.row_titles)
    training = matrix[:, :-1]
    target = matrix[:, -1]
    n = 1
    if args.fast:
        n = -1

    regr = linear_model.LinearRegression(normalize=args.normalize, n_jobs=n)
    regr.fit(training, target)

    if args.output_coefficients:
        import sys
        sys.stderr.write("Interception:\t")
        sys.stderr.write(str(regr.intercept_))
        sys.stderr.write("\nCoefficients:\t")
        sys.stderr.write(str(regr.coef_))
        sys.stderr.write("\n")
    output = np.zeros((prediction.shape[0], prediction.shape[1] + 1))
    output[:, :-1] = prediction
    output[:, -1] = regr.predict(prediction)
    outputvector(output, column_titles, row_titles)


def neuralnetwork():
    """
    :return:
    """
    pass


def randomforest():
    """
    :return:
    """
    pass


def naive_bayes():
    """

    :return:
    """
    pass


def decision_trees():
    """

    :return:
    """
    pass