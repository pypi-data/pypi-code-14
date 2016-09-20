from bisect import bisect_left
from os import path
import pysam
import random

class MotifSites(object):

    """Access and process pseudo-BED annotations for motif sites.
    
    Provides functionality for working with motif predictions. Assumes that
    coordinates are 0-based [start, end).
    
    Attributes:
        _motif_sites: A pysam Tabixfile object.

        filename: The filename associated with the Tabixfile object.

        num_sites: Number of motif site annotations in the given file
    
    Args:
        motif_file: A string specifying the path and filename of the 
            pseudo-BED file containing motif sites. The file must be gzipped 
            and have the '.gz' file extension. It should also have an index 
            file with the same name but with the '.tbi' extension appended. 
            For example, '/path/file.bed' should be gzipped to 
            '/path/file.bed.gz' and have an index file called 
            '/path/file.bed.gz.tbi'.

    Raises:
        IOError: File could not be found or opened.

        IOError: File index could not be found.

        IOError: Gzipped version of file could not be found.
    """

    def __init__(self, motif_file):
        """Initialize MotifSites class."""
        self._motif_sites = self.__load_motif_sites(motif_file)
        self.filename = motif_file
        self.num_sites = len(tuple(
            self._motif_sites.fetch(multiple_iterators=True)))

    def __del__(self):
        """Deconstructor for MotifSites.

        Closes the Tabixfile object in '_motif_sites'.
        """
        try:
            self._motif_sites.close()
        except:
            pass

    def __load_motif_sites(self, filename):
        """Load the pseudo-BED file data into a Tabixfile object.

        Args:
            filename: A string for the psuedo-BED file. The path should be
                prepended if the file is located outside the working directory.

        Returns:
          A pysam Tabixfile object.
        
        Raises:
            IOError: File could not be found or opened.

            IOError: File index could not be found.

            IOError: Gzipped version of file could not be found.
        """
        print "Loading BED file %s..." % path.basename(filename)
        if not path.isfile(filename):
            error_msg = "%s could not be found." % filename
            raise IOError(error_msg)
        if not path.isfile(filename + ".gz"):
            error_msg = "%s could not be found." % (filename + ".gz")
            raise IOError(error_msg)
        if not path.isfile(filename + ".gz.tbi"):
            error_msg = "Index file %s not found." % (filename + ".gz.tbi")
            raise IOError(error_msg)
        tabixfile = pysam.Tabixfile(filename + ".gz", "r")
        return tabixfile

    def get_all_sites(self):
        """Retrieve all motif sites in the MotifSites object.

        Retrieves all the motif sites for the MotifSites object and stores 
        them in an iterator.

        Returns:
            A pysam iterator containing motif site data.
        """
        return self._motif_sites.fetch(parser=pysam.asTuple(), 
            multiple_iterators=True)

    def get_chr_sites(self, chrom, multi_iter=False):
        """Retrieve all motif sites on a specified chromosome.

        Retrieves all the motif sites in the MotifSites object from a 
        specified chromosome and stores them in an iterator.

        Args:
            chrom: A string specifying the chromosome of interest. Must follow
                the naming convention specified by the pseudo-BED file.

            multi_iter: A boolean indicating whether to enable multipe 
                iterators. This should be 'True' if multiple calls are made to
                this method concurrently for the same MotifSites object.

        Returns:
            A pysam iterator that contains motif site data.

        Raises: 
            ValueError - The genomic coordinates are out of range or invalid.
        """
        return self._motif_sites.fetch(reference=chrom,
            parser=pysam.asTuple(), multiple_iterators=multi_iter)
    
    def get_sites(self, chrom, start, end, multi_iter=False):
        """Retrieve motif sites overlapping a genomic interval.

        Retrieves the motif sites in the MotifSites object that overlap 
        with a specified genomic interval. Does not require complete overlap.

        Args:
            chrom: A string specifying the chromosome of interest. Must follow
                the naming convention specified by the pseudo-BED file.

            start: An int for the 0-based start position of the genomic region.

            end: An int for the 0-based end position of the genomic region. The
               position 'end' denotes one position past the region of interest.

            multi_iter: A boolean indicating whether to enable multipe 
                iterators. This should be 'True' if multiple calls are made to
                this method concurrently for the same MotifSites object.

        Returns:
            A pysam iterator that contains motif site data.

        Raises: 
            ValueError - The genomic coordinates are out of range or invalid.
        """
        return self._motif_sites.fetch(chrom, start, end, 
            parser=pysam.asTuple(), multiple_iterators=multi_iter)


    def subsample_sites(self, n_samples, iterations=1):
        """Choose a random subset of motif sites.

        Chooses a random subset of motif sites assuming that n_samples is less 
        than the total number of sites. If n_samples is greater than or equal 
        to the total number of sites, then the whole set is returned.

        Args:
            n_samples: The number of sites to subsample.

        Returns:
            A 2D list containing pseudo-BED format data for the sites selected.
        """

        ######## 
        # TO DO: APPLY PARALLEL PROCESSING FOR OBTAINING SAMPLES
        ########

        def binary_search(a, x, lo=0, hi=None):
            """Binary search algorithm."""
            hi = hi if hi is not None else len(a) 
            pos = bisect_left(a,x,lo,hi)
            return (True if pos != hi and a[pos] == x else False)

        counter = 0
        site_list = [[] for i in xrange(iterations)]
        indices = range(self.num_sites)
        #Apply random sampling if needed
        sample_idx = []
        for i in xrange(iterations):
            if self.num_sites <= n_samples:
                n_samples = self.num_sites
                subset = indices
            else:
                subset = random.sample(indices, n_samples)
                subset.sort()
            sample_idx.append(subset)
        motif_sites = self._motif_sites.fetch(parser=pysam.asTuple(),
            multiple_iterators=True)
        for site in motif_sites:
            for i in xrange(iterations):
                idx = sample_idx[i]
                if binary_search(idx, counter, hi=n_samples):
                    site_list[i].append(site)
            counter += 1
        return site_list

