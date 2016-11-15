import numpy as np
from itertools import izip
from copy import copy
from scipy import spatial
from rlstm.common_util import unique_rows, is_nominal


def hamming_distance( x , y ):
	'''
	Measures the minimum number of substitutions required
	to change one string into the other.

	Strings are padded if not same length.
	https://en.wikipedia.org/wiki/Hamming_distance
	'''
	if len( x ) > len( y ):
		y = y + ' ' * ( len( x ) - len( y ) )
	elif len( x ) < len ( y ):
		x = x + ' ' * ( len( y ) - len( x ) )

	return sum( c1 != c2 for c1,c2 in izip( x, y ) )


def euclidean_distance( x , y ):
	return np.sqrt( np.sum( ( x - y )**2 ) )


def find_closest( x , Y , A_type ):
	'''
	Find closest vector in Y to x (but not the same).
	'''
	distfun = lambda i : euclidean_distance( x[A_type] , i[A_type] ) + \
						 hamming_distance( x[~A_type] , i[~A_type] )
	dists = np.apply_along_axis( distfun , 1 , Y )
	return np.argmin( dists[ dists > 0] )


def safe_tree_query( x , tree , k=2 , p=2 ):
	a, b = tree.query( x , k=k , p=p )
	if np.sum( a ) > 0:
		return b[-1]
	else:
		return safe_tree_query( x , tree , k=k+1 , p=p )


def munge( T , k , p , s , A_type=None ):
	'''
	MUNGE algorithm for generating arbitrary large numbers of data points
	by sampling from a non-parametric estimate of the joint distribution.

	Bucila, Caruana, Niculescu-Mizil
	https://www.cs.cornell.edu/~caruana/compression.kdd06.pdf

	Continuous attributes are assumed to be linearly scaled to [0,1].

    Args
    ----
    T : 2D array, N x A
        set of training examples,
        N is the number of samples, A is the number of attributes

    k : integer,
    	size multiplier

  	p : float (between 0 and 1),
  		defines a probability that swaps the values of attribute
  		a between examples of two sets

  	s : float,
  		standard deviation of the normal distribution to sample
  		from for continuous attributes

	A_type : 1D boolean array, A
			 True is continous , False is nominal / discrete

    Returns
    -------
    D : 2D array, (N x k) x A,
		unlabeled "munged" data set
    '''

	N , A = T.shape

	if A_type is None:
		A_type = [ True for i in range( A ) ] # default
	A_type = np.array( A_type )

	for k_i in range( k ):
		print( 'duplicating %d' % k_i )
		T_ = copy( T )
		tree = spatial.KDTree( T_ )

		for e_i in range( N ):
			e    = T_[e_i]
			e_i_ = safe_tree_query( e , tree , k=2 , p=2 )
			e_   = T_[e_i_]

			for a_i in range( A ):
				e_a  = e[a_i]
				e_a_ = e_[a_i]

				if A_type[a_i]: # continuous:
					sd = np.abs( e_a - e_a_ ) / float( s )
					if np.random.uniform() <= p:
						e_a  = np.random.normal( e_a_ , sd )
					else:
						e_a_ = np.random.normal( e_a , sd )
				else: # nominal
					if np.random.uniform() >= p:
						tmp  = e_a
						e_a  = e_a_
						e_a_ = tmp

				T_[ e_i , a_i ]  = e_a
				T_[ e_i_ , a_i ] = e_a_

		if k_i == 0:
			D = T_
		else:
			D = np.vstack( ( D , T_ ) ) # union

	return D
