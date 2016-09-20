from os import path
import pysam

class Alignments(object):

    """Access and process sequence alignment data.

    The Alignment class acts as a wrapper class for pysam to provide additional
    footprinting specific data processing functionality. Information about 
    pysam can be found at http://pysam.readthedocs.org/.

    Attributes:
        _alignment: A pysam AlignmentFile object.

    Args:
        aln_file: A string containing the path and filename for a sorted 
            BAM file. The file must have an index file with the same name 
            but with the '.bai' extension appended. For example, the index 
            file for '/path/file.bam' should be '/path/file.bam.bai'.

    Raises:
        IOError: BAM file could not be found.
        AssertionError: File is not a BAM file.
        IOError: BAM file index could not be found.
    """

    def __init__(self, aln_file):
        """Inits the Alignment class."""
        self._alignment = self._load_alignment(aln_file)

    def __del__(self):
        """Deconstructor.

        Closes the AlignmentFile object in '_alignment'.
        """
        try:
            self._alignment.close()
        except:
            pass

    def _load_alignment(self, filename):
        """Load the BAM data into an AlignmentFile object.

        Args:
            filename: A string for the BAM file to load. The path should be 
                prepended if the file is located outside the working directory.

        Returns:
            A pysam AlignmentFile object.
    
        Raises:
            IOError: BAM file could not be found.
            AssertionError: File is not a BAM file.
            IOError: BAM file index could not be found.
        """
        if not path.isfile(filename): 
            error_msg = "%s could not be found." % filename
            raise IOError(error_msg)
        if path.splitext(filename)[1] != ".bam":
            error_msg = "%s is not a BAM file." % path.basename(filename)
            raise AssertionError(error_msg)
        if not path.isfile(filename + ".bai"):
            error_msg = "Index file %s not found." % (filename + ".bai")
            raise IOError(error_msg)
        print "Loading BAM file %s..." % path.basename(filename)
        return pysam.AlignmentFile(filename, "rb")

    def get_mapped_read_count(self):
        """Get the number of mapped reads in the AlignmentFile object.

        Returns: A long int corresponding to the number of mapped reads in the
            '_alignment' object.
        """
        return self._alignment.mapped

    def get_unmapped_read_count(self):
        """Get the number of unmapped reads in the AlignmentFile object.

        Returns: A long int corresponding to the number of unmapped reads in 
            the '_alignment' object.
        """
        return self._alignment.unmapped
    
    def get_total_read_count(self):
        """Get the total number of reads in the Samfile object.

        Returns: A long int corresponding to the number of total reads in the
            '_alignment' object.
        """
        return self._alignment.mapped + self._alignment.unmapped

    def get_reads(self, chrom, start, end, multi_iter=False):
        """Get reads overlapping a genomic region.

        Retrieves the set of reads overlapping a specified genomic region using
        BED format chromosome coordinates i.e., 0-based indexing [start, end).

        Args:
            chrom: A string for the name of the chromosome for the desired 
                genomic region. Names are derived from the BAM header. 

            start: An int for the 0-based start position of the genomic region.

            end: An int for the 0-based end position of the genomic region. The
               position 'end' denotes one position past the region of interest.

            multi_iter: A boolean indicating whether to enable multipe 
                iterators. This should be 'True' if multiple calls are made to
                this method for the same Alignments object and the iterators 
                are used concurrently.

        Returns:
            An iterator of AlignedSegment objects.

        Raises:
            ValueError - The genomic coordinates are out of range, are invalid,
                or the file does not permit random access.
        """
        return self._alignment.fetch(chrom, start, end, 
            multiple_iterators=multi_iter)

    def get_read_density(self, chrom, start, end, strand=None, 
        use_weights=False, multi_iter=False):
        """Compute the total number of reads overlapping a genomic region.

        Calculates the read density within a genomic region specified using BED
        format chromosome coordinates i.e., 0-based indexing [start, end). 
        Strand-specific read density is computed if specified. It is 
        important to note that a read is counted merely if it overlaps the
        specified region. The read does not have to be fully contained in the
        region.

        Args:
            chrom: A string for the name of the chromosome for the desired 
                genomic region. Names are derived from the BAM header. 

            start: An int for the 0-based start position of the genomic region.

            end: An int for the 0-based end position of the genomic region. The
               position 'end' denotes one position past the region of interest.

            strand: The strand from which to obtain the read density. Must be 
               one of '+', '-', or 'None' (default). If 'None' is specified 
               then reads from both strands are included.

            multi_iter: A boolean indicating whether to enable multipe 
                iterators. This should be 'True' if multiple calls are made to
                this method concurrently for the same Alignments object.

        Returns:
            A float value corresponding to the total read count observed in
            the genomic interval.
        
        Raises:
            KeyError - The tag field 'XW' cannot be found for a read.

            ValueError - The genomic coordinates are out of range, are invalid,
                or the file does not permit random access.

            ValueError - 'strand' is not specified correctly.
        """
        reads = self._alignment.fetch(chrom, start, end, 
            multiple_iterators=multi_iter)
        read_data = []
        if use_weights:
            for read in reads:
                read_data.append((read.is_reverse, read.is_unmapped, 
                    read.get_tag('XW')))
            if strand == "+":
                read_count = 0.0
                for i in read_data:
                    if not i[0] and not i[1]:
                        read_count += i[2]
            elif strand == "-":
                read_count = 0.0
                for i in read_data:
                    if i[0] and not i[1]:
                        read_count += i[2]
            elif strand == None:
                read_count = sum([i[2] for i in read_data if not i[1]])
            else:
                raise ValueError("strand must be '+', '-', or None")
        else:
            read_data = [(read.is_reverse, read.is_unmapped) 
                for read in reads]
            if strand == "+":
                read_count = 0.0
                for i in read_data:
                    if not i[0] and not i[1]:
                        read_count += 1.0
            elif strand == "-":
                read_count = 0.0
                for i in read_data:
                    if i[0] and not i[1]:
                        read_count += 1.0
            elif strand == None:
                read_count = sum([1.0 for i in read_data if not i[1]])
            else:
                raise ValueError("strand must be '+', '-', or None")
        return read_count

    def get_weights(self, chrom, start, end, strand=None, f_offset=0,
        r_offset=0, multi_iter=False):
        """Retrieve bias correction weights for a given region.

        Retrieves the per position bias correction weights within the 
        specified genomic interval. The per read weights for a position are
        totaled to get the per position weight. The BAM file must contain
        bias correction information or else this method will raise an error.

        Args:
            chrom: A string for the name of the chromosome for the desired 
                genomic region. Names are derived from the BAM header. 

            start: An int for the 0-based start position of the genomic region.

            end: An int for the 0-based end position of the genomic region. The
               position 'end' denotes one position past the region of interest.

            strand: The strand from which to obtain the weights. Must be 
               one of '+', '-', or 'None' (default). If 'None' is specified 
               then reads from both strands are included.

            f_offset: An int denoting the offset downstream from the 5' end of
               a forward (+) strand read. Equivalent to read shifting.

            r_offset: An int denoting the offset upstream from the 5' end of a
               reverse (-) strand read. Equivalent to read shifting.

            multi_iter: A boolean indicating whether to enable multipe 
                iterators. This should be 'True' if multiple calls are made to
                this method concurrently for the same Alignments object.

        Returns:
            A 2-D list of bias correction weights where the first dimension
            represents a genomic position. Index 0 corresponds to 'start'. The
            second dimension is a list of all the read weights at a position.

        Raises:
            KeyError - The tag field 'XW' cannot be found for a read.

            ValueError - The genomic coordinates are out of range, are invalid,
                or the file does not permit random access.

            ValueError - 'strand' is not specified correctly.
        """
        reads = self._alignment.fetch(chrom, start, end, 
            multiple_iterators=multi_iter)
        pos_weights = {}
        neg_weights = {}
        for read in reads:
            if read.is_unmapped: continue
            weight = read.get_tag('XW')
            if read.is_reverse:
                cut_site = read.reference_end - r_offset - 1
                if cut_site >= start and cut_site < end:
                    current_weight = neg_weights.get(cut_site, 0.0)
                    neg_weights[cut_site] = current_weight + weight
            else:
                cut_site = read.reference_start + f_offset
                if cut_site >= start and cut_site < end:
                    current_weight = pos_weights.get(cut_site, 0.0)
                    pos_weights[cut_site] = current_weight + weight
        if strand is None:
            pos_weights = [pos_weights.get(x, 0.0) for x in range(start, end)]
            neg_weights = [neg_weights.get(x, 0.0) for x in range(start, end)]
            combined_weights = []
            for x, y in zip(pos_weights, neg_weights):
                combined_weights.append(x + y)
            return combined_weights
        elif strand == '+':
            return [pos_weights.get(x, 0.0) for x in range(start, end)]
        elif strand == '-':
            return [neg_weights.get(x, 0.0) for x in range(start, end)]
        else:
            raise ValueError("strand must be '+', '-', or None")

    def get_cut_sites(self, chrom, start, end, strand=None, f_offset=0,
        r_offset=0, use_weights=False, multi_iter=False):
        """Retrieve DNaseI digestion sites for a genomic region.

        Makes a list of counts relative to the start coordinate of the
        genomic region specified using BED format chromosome coordinates i.e., 
        0-based indexing [start, end). Cuts are assumed to be 5' read ends
        unless offsets are specified.

        Args:
            chrom: A string for the name of the chromosome for the desired 
                genomic region. Names are derived from the BAM header.
 
            start: An int for the 0-based start position of the genomic region.

            end: An int for the 0-based end position of the genomic region. The
               position 'end' denotes one position past the region of interest.

            strand: The strand from which to obtain the cut counts. Must be 
               one of '+', '-', 'combined' or 'None' (default). If 'combined' 
               is specified then reads from both strands are aggregated. If 
               'None' is specified the read vectors for each strand are 
               concatenated with the '+' strand vector being first.

            f_offset: An int denoting the offset downstream from the 5' end of
               a forward (+) strand read. Equivalent to read shifting.

            r_offset: An int denoting the offset upstream from the 5' end of a
               reverse (-) strand read. Equivalent to read shifting.

            use_weights: A boolean indicating whether bias correction weights 
                should be used for each read. The weights are expected to be
                stored as an optional tag 'XW' for each read.

            multi_iter: A boolean indicating whether to enable multipe 
                iterators. This should be 'True' if multiple calls are made to
                this method concurrently for the same Alignments object.

        Returns:
            A list of counts as floats with positions corresponding to the 
            specified genomic interval.

        Raises:
            KeyError - The tag field 'XW' cannot be found for a read.

            ValueError - The genomic coordinates are out of range, are invalid,
                or the file does not permit random access.

            ValueError - 'strand' is not specified correctly.
        """
        if use_weights:
            return self.get_weights(chrom, start, end, strand, f_offset, 
                r_offset, multi_iter)
        reads = self._alignment.fetch(chrom, start, end, 
            multiple_iterators=multi_iter)
        pos_cuts = {}
        neg_cuts = {}
        for read in reads:
            if read.is_unmapped: continue
            if read.is_reverse:
                cut_site = read.reference_end - r_offset - 1
                if cut_site >= start and cut_site < end:
                    neg_cuts[cut_site] = neg_cuts.get(cut_site, 0.0) + 1.0
            else:
                cut_site = read.reference_start + f_offset
                if cut_site >= start and cut_site < end:
                    pos_cuts[cut_site] = pos_cuts.get(cut_site, 0.0) + 1.0
        if strand is None:
            pos_cuts = [pos_cuts.get(x, 0.0) for x in range(start, end)]
            neg_cuts = [neg_cuts.get(x, 0.0) for x in range(start, end)]
            combined_cuts = ([x + y for x, y in zip(pos_cuts, neg_cuts)])
            return combined_cuts
        elif strand == "combined":
            pos_cuts = [pos_cuts.get(x, 0.0) for x in range(start, end)]
            neg_cuts = [neg_cuts.get(x, 0.0) for x in range(start, end)]
            concat_cuts = pos_cuts + neg_cuts
            return concat_cuts
        elif strand == '+':
            return [pos_cuts.get(x, 0.0) for x in range(start, end)]
        elif strand == '-':
            return [neg_cuts.get(x, 0.0) for x in range(start, end)]
        else:
            err_msg = "strand must be '+', '-', 'combined', or None (default)"
            raise ValueError(err_msg)

