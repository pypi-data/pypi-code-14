from types import *
import numpy as np
import math

class Features(object):

    """Functions for applying feature extraction."""

    @classmethod
    def get_splits(self, length, partition_fn):
        """Get indices for dividing a vector into multiple parts.

        Gets the indices for partitioning a vector into multiple subvectors 
        based on a supplied partition function. If the partition function does 
        not evenly divide the vector then the segments furthest from the vector
        center will include the remainder. This function is designed to easily 
        create partitions whose sizes are approximately symmetric about the 
        vector center but may vary in length otherwise. The list of indices
        matches the format required as an argument for numpy.split().
        

        Args:
            length: An int specifying the size of the vector to partition.

            partition_fn: A vectorized callable that accepts and returns int 
                types. A passed int value denotes the distance from the center
                of the vector in partition function distance. A returned int
                should specify the size of the partition at the provided 
                partition distance. We define a partition distance unit to be 
                the number of partitions away from a specified point where 0 
                denotes an initial partition that borders a specified point.

        Returns:
            An array containing the indices at which a vector of the size 
            specified would be split based on the given partition function.

        Raises:
            AssertionError: The length supplied is not positive.

            TypeError: Partition function is not numpy vectorized.

            TypeError: The 'length' argument is not the correct type.

            ValueError: Non-positive value returned by partition function.
        """
        if type(length) is not IntType:
            error_msg = "Vector supplied must be an array-like or numpy array"
            raise TypeError(error_msg)
        assert length > 0, "Length value is not positive"
        if type(partition_fn) is not np.lib.function_base.vectorize:
            error_msg = "Partition function is not vectorized"
            raise TypeError(error_msg)
        #Get the number of partitions needed to span the vector
        pdist = 0
        error_msg = "Non-positive value returned by partition function"
        if partition_fn(pdist) < 1: raise ValueError(error_msg)
        windows_sum = partition_fn(pdist) * 2
        while windows_sum <= length:            
            pdist += 1
            if partition_fn(pdist) < 1: raise ValueError(error_msg)
            windows_sum = partition_fn(np.arange(pdist + 1)).sum() * 2
        #Get the window sizes to use
        right_windows = partition_fn(np.arange(pdist))
        left_windows = partition_fn(np.arange(pdist - 1, -1, -1))
        #Update the first window size to include the remainder
        remainder = length - left_windows.sum() * 2
        left_remainder = int(math.floor(remainder / 2.0))
        left_windows[0] += left_remainder
        #Make partitions
        left_splits = [left_windows[:(i+1)].sum() 
            for i in range(left_windows.size)]
        center = left_windows.sum()
        right_splits = [right_windows[:(i+1)].sum() + center 
            for i in range(right_windows.size-1)]
        splits = np.append(left_splits, right_splits)
        return splits

    @classmethod
    def slope(self, x, y):
        """Calculate a slope.

        Args:
            x = An array-like of x-coordinates.

            y = An array-like of y-coordinates.

        Returns:
            A numpy float64 value for the slope.

        Raises:
            AssertError: Insufficient number of coordinates given.

            ValueError: x and y coordinate vectors not equal in length.
        """
        assert len(y) > 1, "Insufficient number of coordinates given."
        if type(x) is not np.ndarray:
            x = np.array(x)
        if type(y) is not np.ndarray:
            y = np.array(y)
        numerator = (x * y).mean() - x.mean() * y.mean()
        denominator = (x**2).mean() - x.mean()**2
        return numerator/denominator

    @classmethod
    def get_slopes(self, vector):
        """Extract slope values for segments of a given vector.

        Computes the slope assuming that the segments of the given vector
        represent y-coordinate values and x-coordinate values are spaced
        1 unit apart.
 
        Args:
            vector: An array-like of numpy arrays with numeric values.
    
        Returns:
            A numpy array with slope values for each segment in the given 
            vector.

        Raises:
            AttributeError: Segments of vector are not numpy arrays.
        """
        get_x = lambda x: np.arange(x.size)
        x_vals = [get_x(y) for y in vector]
        return np.array([self.slope(x,y) for x,y in zip(x_vals, vector)])

    @classmethod
    def get_pwm_scores(self, motif_sites, score_column=4):
        """Retrieve PWM scores given a list of motif_sites.

        Gets PWM scores from a 2D list of motif site data in Pseudo-BED format
        and stores them into a list.

        Args:
            motif_sites: A 2D list or iterator of motif sites in 
                Pseudo-BED format.

            score_column: The 2nd dimension index in "motif_sites" that
                specifies the position in the list that contains the PWM score.
                By default it is assumed that this is position 4.

        """ 
        scores = []
        for site in motif_sites:
            scores.append(float(site[score_column]))
        return scores

    @classmethod
    def convert_to_cuts(self, motif_sites, aln_data, flank_size, 
        combine_strands=True, f_offset=0, r_offset=0, use_weights=False):
        """Convert motif sites into a matrix of DNaseI digestion site counts.

        Retrieves a vector of DNaseI digestion sites for each motif site in the
        'motif_sites' list. Puts all the vectors into a 2D list.

        Args:
            motif_sites: A 2D list or iterator of motif sites in 
                Pseudo-BED format.

            aln_data: An Alignment object.

            flank_size: An int specifying how many bases upstream and 
                downstream of the motif site center to include. The value
                specifies one flank. The total included bases is flank_size*2.

            combine_strands: A boolean indicating if DNaseI digestion site 
                counts should be aggregated across strands. If 'False' then
                the forward and reverse strand digestion count vectors are
                concatenated with the forward strand being first.

            f_offset: An int denoting the offset downstream from the 5' end of
               a forward (+) strand read. Equivalent to read shifting.

            r_offset: An int denoting the offset upstream from the 5' end of a
               reverse (-) strand read. Equivalent to read shifting.

            use_weights: A boolean indicating whether bias correction weights 
                should be used for each read.

        Returns:
            A 2D list where each inner list contains DNaseI digestion counts
            per base within and/or around a motif site. Each index of the first
            dimension corresponds to a motif site.

        Raises: 
            ValueError - The genomic coordinates are out of range or invalid.
        """
        cut_matrix = []
        for motif_site in motif_sites:
            chrom = motif_site[0]
            start = int(motif_site[1])
            end = int(motif_site[2])
            midpoint = (start+end)/2
            #Extend region by flank size
            start = midpoint - flank_size
            end = midpoint + flank_size
            #Get cut sites
            if combine_strands:
                cut_sites = aln_data.get_cut_sites(chrom, start, end,
                    strand="combined", f_offset=f_offset, r_offset=r_offset,
                    use_weights=use_weights, multi_iter=False)
            else:
                cut_sites = aln_data.get_cut_sites(chrom, start, end,
                    strand=None, f_offset=f_offset, r_offset=r_offset,
                    use_weights=use_weights, multi_iter=False)
            cut_matrix.append(cut_sites)
        return cut_matrix

