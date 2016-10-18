from lib.inputoutput import ParseVectors, _shared_params
import numpy as np


def zscorenorm(parser):
    """ Normalizes a matrix via z-score normalization normalization.

    """
    from scipy import stats
    parser.add_argument('vector', nargs='?', type=str, help='vector or matrix to normalize', default="sys.stdin")
    parser.add_argument("--ddof", type=int, help="Degrees of freedom correction in the calculation of the standard deviation.", default=0)
    parser.add_argument("-ms","--meansd",type=str,help="vector with first row means and second row standard deviations for each column",nargs='?')
    _shared_params(parser, only_apply_on=True)
    args = parser.parse_args()
    mp = ParseVectors(args.vector, args.column_titles, args.row_titles, delimiter=args.delimiter,
                                only_apply_on_columns=args.only_apply_on)
    matrix = mp.parse()
    column_titles = mp.col_titles
    row_titles = mp.row_titles
    zscores = []
    if args.meansd is not None:
        ms = ParseVectors(args.meansd,None,None,delimiter=args.delimiter)
        meansd = ms.parse()
        means = meansd[0,:]
        sds = meansd[1,:]
        rows = []
        for index, column in enumerate(matrix.T):
            rows.append((column-means[index])/sds[index])
        rows = np.array(rows)
        zscores = rows.T
    else:
        zscores = stats.zscore(matrix, ddof=args.ddof)
    mp.out(zscores, column_titles, row_titles)


def quantilenorm(parser):
    """ Normalizes a matrix via quantile normalization normalization.

    :return:
    """
    parser.add_argument('vector', nargs='?', type=str, help='matrix to normalize', default="sys.stdin")
    parser.add_argument('--rank-method', nargs='?', type=str, help='method to calculate the ranks of the matrix. Default: min. Could be: average, min, max, dense, ordinal', default="min")
    _shared_params(parser, only_apply_on=True)
    args = parser.parse_args()
    mp = ParseVectors(args.vector, args.column_titles, args.row_titles, delimiter=args.delimiter,
                                only_apply_on_columns=args.only_apply_on)
    matrix = mp.parse()
    column_titles = mp.col_titles
    row_titles = mp.row_titles

    from scipy.stats import rankdata
    ranked_matrix = []
    for column in range(0, np.shape(matrix)[1]):
        #column wise ranking
        ranked_matrix.append(rankdata(matrix[:, column], method=args.rank_method))

    #column wised sorted matrix
    matrix_sorted = np.sort(matrix, axis=0)


    #means of each sorted row
    values = np.zeros(len(matrix))
    #calculate each row
    for index, row in enumerate(matrix_sorted):
        values[index] = np.mean(row)
    #new matrix initialized with zeros. should have size of matrix
    new_matrix = np.zeros(np.shape(matrix))
    #new matrix has oposite shape as ranked_matrix
    it = np.nditer(new_matrix, flags=['multi_index'], op_flags=['writeonly'])
    while not it.finished:
        # print(it.multi_index[1])
        #rank starts with 1 => -1
        it[0] = values[ranked_matrix[it.multi_index[1]][it.multi_index[0]] - 1]
        it.iternext()
    mp.out(new_matrix, column_titles, row_titles)


def medianpolish(parser):
    """ Normalizes a matrix via median polish normalization.

    normalization with median polish.
    inspired by Timothy Chen Allen in
    https://www.youtube.com/watch?v=RtC9ZMOYgk8
    :return:
    """
    parser.add_argument('vector', nargs='?', type=str, help='matrix to normalize', default="sys.stdin")
    parser.add_argument('-i', "--iterations", type=int, help='how many iterations should be made', default=3)
    _shared_params(parser, only_apply_on=True)
    args = parser.parse_args()
    mp = ParseVectors(args.vector, args.column_titles, args.row_titles, delimiter=args.delimiter,
                                only_apply_on_columns=args.only_apply_on)

    #matrix, column_titles, row_titles, m_type = vecparse(args.matrix, args.column_titles, args.row_titles)
    matrix = mp.parse()
    column_titles = mp.col_titles
    row_titles = mp.row_titles
    (nrows, ncols) = np.shape(matrix)
    row_affects = np.zeros(nrows)
    column_affects = np.zeros(ncols)
    common_value = 0
    number_of_iterations = args.iterations
    while number_of_iterations > 0:
        #change the row affect by common_value
        row_affects -= common_value
        #find the median of each of the rows of the matrix and the median of the column_affects
        changing_row_affects = np.median(matrix, axis=1)
        changing_common_value = np.median(column_affects)

        #change matrix with changing row affects
        matrix = matrix - np.repeat(changing_row_affects, ncols).reshape(np.shape(matrix))
        #collapse changing row_affect with row_affect
        row_affects += changing_row_affects
        common_value += changing_common_value

        # change the column affect by common_value
        column_affects -= common_value

        #find the median of each column of the matrix and the median of the row_affects
        changing_column_affects = np.median(matrix, axis=0)
        changing_common_value = np.median(row_affects)

        #change matrix with changing column affect
        matrix = matrix - np.repeat(changing_column_affects, nrows).reshape(np.shape(matrix)[::-1]).T

        #collapse changing column affect with column affect
        column_affects += changing_column_affects
        common_value += changing_common_value

        number_of_iterations -= 1

    mp.out(matrix, column_titles, row_titles)