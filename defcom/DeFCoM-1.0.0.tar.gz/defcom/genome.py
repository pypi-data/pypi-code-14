from os import path
from pysam import FastaFile

class Genome(object):

    """Access and process genomic sequence information.
    
    Provides functionality to retrieve and process genomic sequence data. The
    class acts as a wrapper around the pysam FastaFile class.
    
    Attributes:
        _genome: A pysam Fastafile object.

    Args:
        fasta_file: A string containing the path and filename for a genome 
            FASTA file. The file must have an index file with the same name but
            with the '.fai' extension appended. For example, the index file for
            '/path/file.fa' should be '/path/file.fa.fai'.

    Raises:
        IOError: FASTA file could not be found or opened.

        IOError: FASTA file index could not be found.
    """

    def __init__(self, fasta_file):
        """Initialize Genome class."""
        self._genome = self._load_fasta(fasta_file)

    def __del__(self):
        """Deconstructor for the Genome class."""
        try:
            self._genome.close()
        except:
            pass

    def _load_fasta(self, filename):
        """Load the FASTA file data into a FastaFile object.

        Args:
            filename: A string for the FASTA file to load. The path should be
                prepended if the file is located outside the working directory.

        Returns:
          A pysam FastaFile object.

        Raises:
            IOError: FASTA file could not be found or opened.

            IOError: FASTA file index could not be found.
        """
        print "Loading FASTA file %s..." % path.basename(filename)
        if not path.isfile(filename):
            error_msg = "%s could not be found." % filename
            raise IOError(error_msg)
        if not path.isfile(filename + ".fai"):
            error_msg = "Index file %s not found." % (filename + ".fai")
            raise IOError(error_msg)
        return FastaFile(filename)

    def get_genome_filename(self):
        """Get the associated FASTA file name.

        Returns:
            A string for the FASTA file name.
        """
        return path.basename(self._genome.filename)

    def get_chr_names(self):
        """Return the chromosome names associated with the genome.

        Returns:
            A tuple containing chromosome names as strings.
        """
        return self._genome.references

    def get_chr_length(self, chrom):
        """Get the length of specified chromosome.
        
        Args:
            chrom: A string specifying the chromosome of interest. Must follow
                the naming convention specified by the FASTA file.

        Returns:
            An int value representing the length of the chromosome.

        Raises:
            KeyError: Chromosome name could not be found.
        """
        try:
            return self._genome.get_reference_length(chrom)
        except KeyError:
            print ("Genome has the following chromosome/reference names:\n")
            for i in self._genome.references: print i
            error_msg = "\n%s not found in reference list!" % chrom
            raise KeyError(error_msg)

    def get_sequence(self, chrom, start, end, strand="+"):
        """Get nucleotide sequence from genomic coordinates.

        Retrieves the nucleotide sequence for a specified genomic region using
        BED format chromosome coordinates i.e., 0-based indexing [start, end).

        Args:
            chrom: A string specifying the chromosome of interest. Must follow
                the naming convention specified by the FASTA file.

            start: An int for the 0-based start position of the genomic region.

            end: An int for the 0-based end position of the genomic region. The
               position 'end' denotes one position past the region of interest.

            strand: The strand from which to obtain the cut counts. Must be 
               either '+' or '-'.

        Returns:
            A string of uppercase nucleotides corresponding to specified
            strand of the genomic region supplied.

        Raises:
            KeyError - The chromosome name is specified incorrectly.

            ValueError - The genomic coordinates are out of range, are invalid,
                or the file does not permit random access.

            ValueError - 'strand' is not specified correctly.
        """
        if strand == "+":
            return self._genome.fetch(chrom, start, end).upper()
        elif strand == "-":
            dna = self._genome.fetch(chrom, start+1, end+1).upper()
            return self.reverse_complement(dna)
        else:
            raise ValueError("strand must be '+' or '-'")

    @classmethod
    def complement(self, sequence):
        """Get the complement of the given DNA sequence.
           
        Args:
            sequence: A string from alphabet {A,C,G,T,N,a,c,g,t,n}.
    
        Returns:
            A string with the complementary DNA sequence of the sequence 
            provided.

        Raises:
            KeyError: The string provided contains characters other than 
                'A', 'C', 'G', 'T', 'N', 'a', 'c', 'g', 't', and 'n'.
        """
        seq_dict = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N',
            'a':'T', 't':'A', 'g':'C', 'c':'G', 'n':'N',}
        try:        
            return "".join([seq_dict[i] for i in sequence.upper()])
        except KeyError:
            error_msg = "DNA sequence must be from {A,C,G,T,N,a,c,g,t,n}"
            raise KeyError(error_msg)
    
    @classmethod
    def reverse_complement(self, sequence):
        """Reverse complement the given DNA sequence.
           
        Args:
            sequence: A string from alphabet {A,C,G,T,N,a,c,g,t,n}.
    
        Returns:
            A string with the reverse complement DNA sequence of the sequence 
            provided.

        Raises:
            KeyError: The string provided contains characters other than 
                'A', 'C', 'G', 'T', and 'N'.
        """
        return self.complement(sequence)[::-1]
