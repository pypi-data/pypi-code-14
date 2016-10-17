import sys
from lib.inputoutput import ParseVectors, _shared_params
from lib.inputoutput import vecparse, outputvector
import numpy as np
import argparse


def _merge_titles(title1, title2):
    """
    Merges two title lists into one. If the titles of a row/column at given index i==j is not equal, then
     it merges to the form 'title1_title2'
    :param title1: first list
    :param title2: second list
    :return: merged list
    """
    if len(title1) == len(title2):
        for index, value in enumerate(title1):
            if value == title2[index]:
                pass
            else:
                title1[index] = value + "_" + title2[index]
    else:
        raise IndexError("Length of Titles differ")
    return title1


# def colmax(parser):
#     """calculates the maximum of a column
#     Calculates the maximum of a column given by --col
#     It can only calculate it on numbers
#     """
#     parser.add_argument('infiles', nargs='?', type=str, default="sys.stdin")
#     parser.add_argument('--col', type=str, required=True, help="")
#     parser.add_argument('-c', "--column-titles", action="store_true", help='column titles are defined')
#
#     args = parser.parse_known_args()[0]
#     col = int(args.col)
#     matrix, cols, rows, mtype = vecparse(args.infiles, args.column_titles)
#     column = list(map(float, matrix[:, col]))
#     maks = [[np.amax(column)]]
#     if cols is not None:
#         cols = [cols[col]]
#     outputvector(maks, cols)


def add(parser):
    """ Adds matrices or scalars to matrices.
    add n matrices via matrix-addition to stdin or a file
    require n matrices with same dimension of the matrix in stdin or file

    #Examples:

    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2

    $ cat negative_unit_vector.csv
    -1	0	0
    0	-1	0
    0	0	-1

    $ vectortools.py add matrix.csv negative_unit_vector.csv
    1	-1	0
    -1	1	-1
    0	-1	1

    $ vectortools.py add matrix.csv negative_unit_vector.csv negative_unit_vector.csv
    0	-1	0
    -1	0	-1
    0	-1	0

    $ vectortools.py add matrix.csv negative_unit_vector.csv negative_unit_vector.csv matrix.csv
    2	-2	0
    -2	2	-2
    0	-2	2

    """
    parser.add_argument('matrix', nargs='?', type=str, help='Base matrix', default="sys.stdin")
    parser.add_argument('addable_matrices', type=str, help='Matrices to add to the base matrix', nargs='+')

    _shared_params(parser, only_apply_on=True)


    args = parser.parse_args()
    sources = args.addable_matrices
    matrix_in = args.matrix
    #matrix, column_titles, row_titles, m_type = vecparse(matrix_in, args.column_titles, args.row_titles)
    matrix_parser = ParseVectors(matrix_in, has_col_names=args.column_titles, has_row_names=args.row_titles, delimiter=args.delimiter, only_apply_on_columns=args.only_apply_on)
    matrix = matrix_parser.parse()
    column_titles = matrix_parser.col_titles
    row_titles = matrix_parser.row_titles
    for f in sources:
        #matrix_new, columns, rows, m_typ = vecparse(f, args.column_titles, args.row_titles)
        mp = ParseVectors(f, has_col_names=args.column_titles, has_row_names=args.row_titles, delimiter=args.delimiter, only_apply_on_columns=args.only_apply_on)
        matrix_new = mp.parse()
        columns = mp.col_titles
        rows = mp.row_titles
        matrix = matrix + matrix_new

        # if column_titles is not None:
        #     #column_titles = _merge_titles(column_titles, columns)
        # if row_titles is not None:
        #     #row_titles = _merge_titles(row_titles, rows)
    sys.stderr.write(repr(column_titles)+"\n"+str(row_titles)+"\n")
    matrix_parser.out(matrix, column_titles, row_titles)


def subtract(parser):
    """ Substracts matrices via matrix-substraction or scalars
    substract n matrices via matrix-substraction from stdin or a file
    require n matrices with same dimension of the matrix in stdin or file

    #Examples:

    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2

    $ cat unit_vector.csv
    1.0	0.0	0.0
    0.0	1.0	0.0
    0.0	0.0	1.0

    $ vectortools.py subtract matrix.csv unit_vector.csv
    1	-1	0
    -1	1	-1
    0	-1	1

    $ vectortools.py subtract matrix.csv unit_vector.csv unit_vector.csv
    0	-1	0
    -1	0	-1
    0	-1	0

    $ vectortools.py subtract matrix.csv unit_vector.csv unit_vector.csv unit_vector.csv
    -1	-1	0
    -1	-1	-1
    0	-1	-1

    $ vectortools.py subtract matrix.csv unit_vector.csv unit_vector.csv unit_vector.csv negative_unit_vector.csv
    0	-1	0
    -1	0	-1
    0	-1	0

    $ vectortools.py subtract matrix.csv unit_vector.csv unit_vector.csv unit_vector.csv negative_unit_vector.csv matrix.csv
    -2	0	0
    0	-2	0
    0	0	-2

    $ vectortools.py subtract matrix.csv unit_vector.csv unit_vector.csv unit_vector.csv negative_unit_vector.csv matrix.csv negative_unit_vector.csv
    -1	0	0
    0	-1	0
    0	0	-1

    """
    parser.add_argument('matrix', nargs='?', type=str, help='Base matrix', default="sys.stdin")
    parser.add_argument('substractable_matrices', type=str, help='Matrices to add to the base matrix', nargs='+')

    _shared_params(parser, only_apply_on=True)

    args = parser.parse_args()
    sources = args.substractable_matrices
    #matrix_in = args.matrix
    # matrix, column_titles, row_titles, m_type = vecparse(matrix_in, args.column_titles, args.row_titles)
    matrix_parser = ParseVectors(args.matrix,
                                 has_col_names=args.column_titles,
                                 has_row_names=args.row_titles,
                                 delimiter=args.delimiter,
                                 only_apply_on_columns=args.only_apply_on)
    matrix = matrix_parser.parse()
    column_titles = matrix_parser.col_titles
    row_titles = matrix_parser.row_titles
    for f in sources:
        mp = ParseVectors(f,
                         has_col_names=args.column_titles,
                         has_row_names=args.row_titles,
                         delimiter=args.delimiter,
                         only_apply_on_columns=args.only_apply_on)

        matrix_new = mp.parse()
        columns = mp.col_titles
        rows = mp.row_titles
        #matrix_new, columns, rows, m_typ = vecparse(f, args.column_titles, args.row_titles)
        matrix = matrix - matrix_new
        # if column_titles is not None:
        #     column_titles = _merge_titles(column_titles, columns)
        # if row_titles is not None:
        #     row_titles = _merge_titles(row_titles, rows)
    matrix_parser.out(matrix, column_titles, row_titles)


def addscalar(parser):
    """Add scalar to a matrix

    #Examples:
    $ cat unit_vector.csv
    1.0	0.0	0.0
    0.0	1.0	0.0
    0.0	0.0	1.0

    $ vectortools.py add_scalar unit_vector.csv -10
    -9	-10	-10
    -10	-9	-10
    -10	-10	-9

    $ vectortools.py add_scalar unit_vector.csv 1
    2	1	1
    1	2	1
    1	1	2

    $ vectortools.py add_scalar unit_vector.csv -1
    0	-1	-1
    -1	0	-1
    -1	-1	0

    $ vectortools.py add_scalar unit_vector.csv 0.5
    1.5	0.5	0.5
    0.5	1.5	0.5
    0.5	0.5	1.5

    """
    parser.add_argument('matrix', nargs='?', type=str, help='Base matrix', default="sys.stdin")
    parser.add_argument('scalar', type=float, help='scalar to add to the base matrix', nargs=1)

    _shared_params(parser, only_apply_on=True)

    args = parser.parse_args()
    scalar = args.scalar[0]
    if (scalar - int(scalar)) == 0:
        scalar = int(scalar)
    matrix_in = args.matrix
    #matrix, column_titles, row_titles, m_type = vecparse(matrix_in, args.column_titles, args.row_titles)
    matrix_parser = ParseVectors(matrix_in, has_col_names=args.column_titles, has_row_names=args.row_titles,
                                 delimiter=args.delimiter, only_apply_on_columns=args.only_apply_on)
    matrix = matrix_parser.parse()
    column_titles = matrix_parser.col_titles
    row_titles = matrix_parser.row_titles
    matrix = np.add(matrix, scalar)
    matrix_parser.out(matrix, column_titles, row_titles)

def multiplyscalar(parser):
    """Multiply matrix/vector with a scalar

    #Examples:
    $ cat unit_vector.csv
    1.0	0.0	0.0
    0.0	1.0	0.0
    0.0	0.0	1.0

    $ vectortools.py multiply_scalar 5 < unit_vector.csv
    5	0	0
    0	5	0
    0	0	5

    $ vectortools.py multiply_scalar -1 < unit_vector.csv
    -1	0	0
    0	-1	0
    0	0	-1


    """
    parser.add_argument('matrix', nargs='?', type=str, help='Base matrix', default="sys.stdin")
    parser.add_argument('scalar', type=float, help='scalar to add to the base matrix', nargs=1)

    _shared_params(parser, only_apply_on=True)

    args = parser.parse_args()
    scalar = args.scalar[0]
    if scalar - int(scalar) == 0:
        scalar = int(scalar)
    #matrix_in = args.matrix
    matrix_parser = ParseVectors(args.matrix, has_col_names=args.column_titles,
                                 has_row_names=args.row_titles,
                                 delimiter=args.delimiter,
                                 only_apply_on_columns=args.only_apply_on)
    matrix = matrix_parser.parse()
    cols = matrix_parser.col_titles
    rows = matrix_parser.row_titles
    #matrix, column_titles, row_titles, m_type = vecparse(matrix_in, args.column_titles, args.row_titles)
    matrix = np.multiply(matrix, scalar)
    matrix_parser.out(matrix, cols, rows)

def multiply(parser):
    """ Multiplies matrices via matrix-multiplication or scalars.

    The rows and columns are renamed by col: x0 to xn and row: y0 to yn

    Multiplication of matrices to the base matrix

    #Examples:
    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2
    $ cat inverse_matrix.csv
    0.75	0.5	0.25
    0.5	1.0	0.5
    0.25	0.5	0.75
    $ vectortools.py multiply matrix.csv inverse_matrix.csv
    1.0	0.0	0.0
    0.0	1.0	0.0
    0.0	0.0	1.0

    """
    parser.add_argument('matrix', nargs='?', type=str, help='Base matrix', default="sys.stdin")
    parser.add_argument('multiplicands', type=str, help='Matrices to multiply to the base matrix. ', nargs='+')

    _shared_params(parser, only_apply_on=True)

    args = parser.parse_args()
    base_matrix = args.matrix
    multiplicand_matrices = args.multiplicands
    #matrix, column_titles, row_titles, m_type = vecparse(base_matrix, args.column_titles, args.row_titles)
    matrix_parser = ParseVectors(base_matrix,
                                 has_col_names=args.column_titles,
                                 has_row_names=args.row_titles,
                                 delimiter=args.delimiter,
                                 only_apply_on_columns=args.only_apply_on)
    matrix = matrix_parser.parse()
    column_titles = matrix_parser.col_titles
    row_titles = matrix_parser.row_titles
    for f in multiplicand_matrices:
        mp = ParseVectors(f,
                          has_col_names=args.column_titles,
                          has_row_names=args.row_titles,
                          delimiter=args.delimiter,
                          only_apply_on_columns=args.only_apply_on)
        matrix_new = mp.parse()
        columns = mp.col_titles
        rows = mp.row_titles
        #matrix_new, columns, rows, m_type = vecparse(f, args.column_titles, args.row_titles)
        matrix = np.dot(matrix, matrix_new)
    if columns is not None:
        column_titles = []
        for i in range(0, np.shape(matrix)[0]):
            column_titles.append("x" + str(i))
    if rows is not None:
        row_titles = []
        for i in range(0, np.shape(matrix)[1]):
            row_titles.append("y" + str(i))
    matrix_parser.out(matrix, column_titles, row_titles)

def dotproduct(parser):
    """ Calculates the dot product of two vectors.

    #Examples:

    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2

    $ cat unit_vector.csv
    1.0	0.0	0.0
    0.0	1.0	0.0
    0.0	0.0	1.0

    $ vectortools.py dot_product matrix.csv unit_vector.csv
    6

    """
    parser.add_argument('vector1', nargs='?', type=str, help='first vector, only one value per line', default="sys.stdin")
    parser.add_argument('vector2', nargs=1, type=str, help='second vector, only one value per line')

    _shared_params(parser)

    args = parser.parse_args()
    v1 = args.vector1
    v2 = args.vector2[0]

    #vector1, col1, row1, m_type = vecparse(v1, args.column_titles, args.row_titles)
    matrix_parser = ParseVectors(v1, args.column_titles, args.row_titles, args.delimiter)
    vector1 = matrix_parser.parse()
    col1 = matrix_parser.col_titles
    row1 = matrix_parser.row_titles
    #vector2, col2, row2, m_type = vecparse(v2, args.column_titles, args.row_titles)
    mp = ParseVectors(v2, args.column_titles, args.row_titles, args.delimiter)
    vector2 = mp.parse()
    col2 = mp.col_titles
    row2 = mp.row_titles
    vector1 = vector1.reshape(-1)
    vector2 = vector2.reshape(-1)
    print(np.dot(vector1, vector2))


def inverse(parser):
    """ Calculates the inverse matrix for square matrices. (Must be invertible)

    #Examples:
    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2

    $ vectortools.py inverse matrix.csv
    0.75	0.5	0.25
    0.5	1.0	0.5
    0.25	0.5	0.75


    """
    parser.add_argument('matrix', nargs='?', type=str, help='square matrix to invert', default="sys.stdin")

    _shared_params(parser)

    args = parser.parse_args()
    #matrix, cols, rows, m_type = vecparse(args.matrix, args.column_titles, args.row_titles)
    matrix_parser = ParseVectors(args.matrix, has_col_names=args.column_titles, has_row_names=args.row_titles, delimiter=args.delimiter)
    matrix = matrix_parser.parse()
    cols = matrix_parser.col_titles
    rows = matrix_parser.row_titles
    shape = np.shape(matrix)
    if shape[0] != shape[1]:
        raise ValueError("Matrix is not a square matrix")
    det = _calc_determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is singular. It has no inverse")
    inverse_matrix = np.linalg.inv(matrix)
    matrix_parser.out(inverse_matrix, cols, rows)


def determinant(parser):
    """ Calculates the determinant for square matrices.

    #Examples:

    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2

    $ vectortools.py determinant matrix.csv
    4
    """
    parser.add_argument('matrix', nargs='?', type=str, help='square matrix to calculate the determinant', default="sys.stdin")

    _shared_params(parser)

    args = parser.parse_args()
    #matrix, cols, rows, m_type = vecparse(args.matrix, args.column_titles, args.row_titles)
    matrix_parser = ParseVectors(args.matrix, args.column_titles, args.row_titles, args.delimiter)
    matrix = matrix_parser.parse()
    column_titles = matrix_parser.col_titles
    row_titles = matrix_parser.row_titles
    shape = np.shape(matrix)
    if shape[0] != shape[1]:
        raise ValueError("Matrix is not a square matrix")
    det = _calc_determinant(matrix)
    sys.stdout.write(str(det) + "\n")


def _calc_determinant(matrix):
    """
    calculates the determinant recursive
    :param matrix: a square matrix
    :return: determinant
    """
    if np.shape(matrix)[0] == 2:
        # sys.stderr.write("{} {}\n{} {}\n".format(matrix[0][0], matrix[1][1], matrix[0][1], matrix[1][0]))
        return matrix[0][0] * matrix[1][1] - (matrix[0][1] * matrix[1][0])
    else:
        det = 0
        for index, el in enumerate(matrix[0]):
            col = list(range(0, np.shape(matrix)[0]))
            col.remove(index)
            row = list(range(1, np.shape(matrix)[0]))
            sub_matrix = matrix[np.ix_(row, col)]
            if index % 2 == 0:
                det += el * _calc_determinant(sub_matrix)
            else:
                det -= el * _calc_determinant(sub_matrix)
        return det


def eigenvalues(parser):
    """ Calculates the eigenvalues of a matrix. The order is the same as in the function eigenvectors

    #Examples:
    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2

    $ vectortools.py eigenvalues matrix.csv
    3.41421356237	2.0	0.585786437627

    """
    parser.add_argument('matrix', nargs='?', type=str, help='matrix to calculate the eigenvalues for', default="sys.stdin")
    _shared_params(parser)
    args = parser.parse_args()
    vector_parser = ParseVectors(args.matrix,
                                 has_col_names=args.column_titles,
                                 has_row_names=args.row_titles,
                                 delimiter=args.delimiter)
    matrix = vector_parser.parse()
    w,v = np.linalg.eig(matrix)
    #outputvector([w], vector_parser.col_titles,vector_parser.row_titles)
    vector_parser.out([w], vector_parser.col_titles,vector_parser.row_titles)

def eigenvectors(parser):
    """ Calculates the eigenvectors of a given matrix. The order is the same as in the function eigenvalues

    #Examples:

    $ cat matrix.csv
    2	-1	0
    -1	2	-1
    0	-1	2

    $ vectortools.py eigenvectors matrix.csv
    -0.5	-0.707106781187	0.5
    0.707106781187	4.05925293379e-16	0.707106781187
    -0.5	0.707106781187	0.5
    """
    parser.add_argument('matrix', nargs='?', type=str, help='matrix to calculate the eigenvectors for', default="sys.stdin")
    _shared_params(parser)
    args = parser.parse_args()
    vector_parser = ParseVectors(args.matrix,
                                 has_col_names=args.column_titles,
                                 has_row_names=args.row_titles,
                                 delimiter=args.delimiter)
    matrix = vector_parser.parse()
    w,v = np.linalg.eig(matrix)
    #outputvector(v, vector_parser.col_titles,vector_parser.row_titles)
    vector_parser.out(v, vector_parser.col_titles, vector_parser.row_titles)


def sumup(parser):
    """ Sums the columns of a matrix

    sums the matrix columnwise
    """
    parser.add_argument('matrix', nargs='?', type=str, help='Base matrix', default="sys.stdin")
    _shared_params(parser, only_apply_on=True)
    args = parser.parse_args()
    matrix_parser = ParseVectors(args.matrix, args.column_titles, args.row_titles, args.delimiter, args.only_apply_on)
    matrix = matrix_parser.parse()
    cols = matrix_parser.col_titles
    rows = matrix_parser.row_titles
    matrix = [np.sum(matrix, axis=0)]
    matrix_parser.out(matrix, cols, None)
