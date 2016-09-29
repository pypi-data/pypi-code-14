class GenomicPosition(object):

    def __init__(self, chromosome, position, strand='+'):
        self.chromosome = chromosome
        self.position = position
        self.strand = strand

    def __str__(self):
        return '{}:{}'.format(self.chromosome, self.position + 1)

    def __eq__(self, other):
        return self.chromosome == other.chromosome and self.position == other.position and\
            self.strand == other.strand

    def __lt__(self, other):
        return (self.chromosome < other.chromosome) or\
            (self.chromosome == other.chromosome) and (self.position < other.position)

    def __sub__(self, other):
        """
        Subtract two positions from each other to get the distance
        :param other: other position
        :type other: GenomicPosition
        :return: distance between positions
        :rtype: int
        """
        if self.chromosome != other.chromosome:
            raise ValueError('Positions not on same chromosome')
        return self.position - other.position
