class GenomicPosition(object):

    def __init__(self, chromosome, position, strand='+'):
        self.chromosome = chromosome
        self.position = position
        self.strand = strand

    def __str__(self):
        return '{}:{}'.format(self.chromosome, self.position + 1)

    def __repr__(self):
        return 'GenomicPosition({})'.format(self)

    def __eq__(self, other):
        return self.chromosome == other.chromosome and self.position == other.position and\
            self.strand == other.strand

    def __lt__(self, other):
        return (self.chromosome < other.chromosome) or\
            (self.chromosome == other.chromosome) and (self.position < other.position)

    def __add__(self, other):
        """
        Add an integer to the current position
        :param int other: integer to add
        :return: new position
        :rtype: GenomicPosition
        """
        return GenomicPosition(self.chromosome, self.position + other, strand=self.strand)

    def __sub__(self, other):
        """
        Subtract either an integer from the current position or find the distance between two positions
        :param int other: integer to subtract
        :return: new position
        :rtype: GenomicPosition
        """
        return GenomicPosition(self.chromosome, self.position - other, strand=self.strand)

    def get_distance_to(self, other):
        """
        Get the distance between two positions
        :param other: other position
        :return: distance between positions
        :rtype: int
        """
        if self.chromosome != other.chromosome:
            raise ValueError('Positions on different chromosomes: "{}" and "{}"'.format(self.chromosome, other.chromosome))
        return self.position - other.position
