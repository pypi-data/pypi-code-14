"""
Functions and classes for handling next generation sequencing data.
:author: Manuel Tuschen
:license: FreeBSD

License
----------
Copyright (c) 2016, Manuel Tuschen
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import division, absolute_import, unicode_literals, print_function

import re

from miscpy import prepareLoading, prepareSaving

from ._ngsData import Data


__all__ = ["GFF3Entry", "GFF"]

class GFF3Entry:
    """
    GFF version 3 entry.
    http://gmod.org/wiki/GFF3

    Notes on comparing GFF entries.
    Entris are considered equal only if all entris are equal.
    One entry is regarded as larger only if the sequence id is larger or equal
    and the start position is truly larger. One entry is regarded as
    larger-equalonly if the sequence id is larger or equal and the start
    position is larger or equal. The same rules apply for smaller.

    Attributes
    ----------
    seqid : basestring
        The ID of the landmark used to establish the coordinate system for the
        current feature. IDs may contain any characters, but must escape any
        characters not in the set [a-zA-Z0-9.:^*$@!+_?-|]. In particular, IDs
        may not contain unescaped whitespace and must not begin with an
        unescaped ">". To escape a character in this, or any of the other GFF3
        fields, replace it with the percent sign followed by its hexadecimal
        representation. For example, ">" becomes "%E3". See URL Encoding (or:
        'What are those "%20" codes in URLs?') for details
        (http://www.blooberry.com/indexdot/html/topics/urlencoding.htm).
    source : basestring
       The source is a free text qualifier intended to describe the algorithm or
       operating procedure that generated this feature. Typically this is the
       name of a piece of software, such as "Genescan" or a database name, such
       as "Genbank." In effect, the source is used to extend the feature
       ontology by adding a qualifier to the type creating a new composite type
       that is a subclass of the type in the type column. It is not necessary to
       specify a source. If there is no source, put a "." (a period) in this
       field.
    type : basestring
        The type of the feature (previously called the "method"). This is
        constrained to be either: (a) a term from the "lite" sequence ontology,
        SOFA; or (b) a SOFA accession number. The latter alternative is
        distinguished using the syntax SO:000000. This field is required.
    start : int
        The start of the feature, in 1-based integer coordinates, relative to
        the landmark given in column 1. Start is always less than or equal to
        end. For zero-length features, such as insertion sites, start equals
        end and the implied site is to the right of the indicated base in the
        direction of the landmark. The field is required.
    end : int
        The end of the feature, in 1-based integer coordinates, relative to
        the landmark given in column 1. Start is always less than or equal to
        end. For zero-length features, such as insertion sites, start equals
        end and the implied site is to the right of the indicated base in the
        direction of the landmark. The field is required.
    score : float
        The score of the feature, a floating point number. As in earlier
        versions of the format, the semantics of the score are ill-defined.
        It is strongly recommended that E-values be used for sequence
        similarity features, and that P-values be used for ab initio gene
        prediction features. If there is no score, put a "." (a period) in this
        field.
    strand : char
        The strand of the feature. + for positive strand
        (relative to the landmark), - for minus strand, and . for features that
        are not stranded. In addition, ? can be used for features whose
        strandedness is relevant, but unknown.
    phase : int
        For features of type "CDS", the phase indicates where the feature
        begins with reference to the reading frame. The phase is one of the
        integers 0, 1, or 2, indicating the number of bases that should be
        removed from the beginning of this feature to reach the first base of
        the next codon. In other words, a phase of "0" indicates that the next
        codon begins at the first base of the region described by the current
        line, a phase of "1" indicates that the next codon begins at the second
        base of this region, and a phase of "2" indicates that the codon begins
        at the third base of this region. This is NOT to be confused with the
        frame, which is simply start modulo 3. If there is no phase, put a "."
        (a period) in this field. For forward strand features, phase is counted
        from the start field. For reverse strand features, phase is counted
        from the end field. The phase is required for all CDS features.
    attributes : dict
        A list of feature attributes in the format tag=value. Multiple
        tag=value pairs are separated by semicolons. URL escaping rules are
        used for tags or values containing the following characters: ",=;".
        Spaces are allowed in this field, but tabs must be replaced with the
        %09 URL escape. This field is not required.  Multiple attributes of
        the same type are indicated by separating the values with the comma ","
        character.
        Some keys have predefined meanings:
        ID
            Indicates the unique identifier of the feature. IDs must be unique
            within the scope of the GFF file.
        Name
            Display name for the feature. This is the name to be displayed to
            the user. Unlike IDs, there is no requirement that the Name be
            unique within the file.
        Alias
            A secondary name for the feature. It is suggested that this tag be
            used whenever a secondary identifier for the feature is needed,
            such as locus names and accession numbers. Unlike ID, there is no
            requirement that Alias be unique within the file.
        Parent
            Indicates the parent of the feature. A parent ID can be used to
            group exons into transcripts, transcripts into genes, and so forth.
            A feature may have multiple parents. Parent can *only* be used to
            indicate a partof relationship.
        Target
            Indicates the target of a nucleotide-to-nucleotide or
            protein-to-nucleotide alignment. The format of the value is
            "target_id start end [strand]", where strand is optional and may
            be "+" or "-". If the target_id contains spaces, they must be
            escaped as hex escape %20.
        Gap
            The alignment of the feature to the target if the two are not
            collinear (e.g. contain gaps). The alignment format is taken from
            the CIGAR format described in the Exonerate documentation.
            http://cvsweb.sanger.ac.uk/cgi-bin/cvsweb.cgi/exonerate?cvsroot=Ensembl).
            See the GFF3 specification for more information.
        Derives_from
            Used to disambiguate the relationship between one feature and
            another when the relationship is a temporal one rather than a
            purely structural "part of" one. This is needed for polycistronic
            genes. See the GFF3 specification for more information.
        Note
            A free text note.
        Dbxref
            A database cross reference. See the GFF3 specification for more
            information.
        Ontology_term
            A cross reference to an ontology term. See the GFF3 specification
            for more information.
    valid : bool
        To check if the entry is a valid one.

    Methods
    -------
    """

    def __init__(self, seqid, scource, type, start, end, score=None,
                 strand=None, phase=None, attributes=None):

        self.seqid = seqid
        self.source = scource
        self.type = type
        self.start = start
        self.end = end
        self.score = score
        self.strand = strand
        self.phase = phase
        self.attributes = attributes

    def __getattr__(self, valid):
        return self._valid()

    def __str__(self):
        sep = '\t'
        gsep = ';'
        newline = '\n'

        seqid = str(self.seqid)
        source = str(self.source)
        type = str(self.type)
        start = str(self.start)
        end = str(self.end)
        if self.score is None:
            score = '.'
        else:
            score = str(self.score)
        if self.strand is None:
            strand = '.'
        else:
            strand = str(self.strand)
        if self.phase is None:
            phase = '.'
        else:
            phase = str(self.phase)
        group = ""
        for key, value in self.attributes.items():
            group += str(key) + '=' + str(value) + gsep
        group = group.rstrip(gsep)

        return seqid + sep + source + sep + type + sep + start + sep + end + sep + \
               score + sep + strand + sep + phase + sep + group + \
               newline

    def __lt__(self, other):
        if self.seqid <= other.seqid and self.start < other.start:
            return True
        else:
            return False

    def __le__(self, other):
        return not other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        attr_equal = True
        if self.attributes.keys != other.attribues.keys:
            return False
        for key in self.attributes.keys():
            if self.attributes[key] != other.attribues[key]:
                return False

        if self.seqid == other.seqid and self.source == other.source and \
                        self.type == other.type and self.start == other.start and self.end \
                == other.end and self.score == other.score and self.strand == \
                other.starnd and self.pahse == other.phase and attr_equal:
            return True
        else:
            return False

    def __neg__(self, other):
        return not self == other

    def _valid(self):

        pattern = re.compile("[a-zA-Z0-9.:^*$@!+_?-|]")
        strand_pattern = re.compile("[+-.?]")
        # check seqid
        if not pattern.match(self.seqid):
            print("seqid", self.seqid)
            return False

        # check source:
        if not pattern.match(self.source):
            print("source", self.source)
            return False

        # check type:
        if not pattern.match(self.type):
            print("type", self.type)
            return False

        # check start"
        if not isinstance(self.start, int):
            print("start", self.start)
            return False
        if self.start < 1:
            print("start", self.start)
            return False

        # check end
        if not isinstance(self.end, int):
            print("end", self.end)
            return False
        if self.end < self.start:
            print("end", self.end)
            return False

        # check score
        if not (self.score is None or isinstance(self.score, float)):
            print("score", self.score)
            return False

        # check strand
        if not (self.strand is None or strand_pattern.match(self.strand)):
            print("strand", self.strand)
            return False

        # check phase:
        if not (self.phase is None or self.phase in [-1, 0, 1, 2, ]):
            print("phase", self.phase)
            return False

        return True


class GFF(Data):
    """
    A GFF object is designed to parse data from an GFF file or write its
    data to an GFF file. GFF version 3 is currently supported. GFF supports
    iterator and mutable sequence protocols. Items can be accessed by an tuple
    key (seqid, n), i.e. the nth entry of seqid.

    Attributes
    ----------
    version : int
        The GFF version

    Methods
    -------
    append(value) :
        Append another GFFentry.
    sort() :
        Sort entries;
    parse(name, path, extension="gff", validate=True) :
        Parse data from path/name.extension and store them in the GFF object.
    write(name, path, extension="gff", validate=True) :
        Write data to path/name.extension
    """

    def __init__(self, version=3):

        super().__init__(GFF3Entry)
        if version != 3:
            raise ValueError("Requested version not supported")
        self.version = version
        self._header_general = ["##gff-version {v} \n".format(v=self.version)]
        self._header_region = {}
        self._extension = "gff"

    def parse(self, name, path, extension="gff", validate=True):
        fname = prepareLoading(name, path, extension=extension)

        if self.version == 3:
            self.__parse3(fname, validate=validate)
        else:
            raise ValueError("Requested version not supported!")

    def write(self, name, path, extension="gff", validate=True):
        fname = prepareSaving(name, path, extension=extension)

        if self.version == 3:
            self.__write3(fname, validate=validate)
        else:
            raise ValueError("Requested version not supported!")

    def __parse3(self, fname, validate):
        """
        parse gff version 3 file.
        """
        self._header_region = {}

        splitter = '\t'
        counter = 0
        with open(fname, 'r') as file:
            for line in file:
                counter += 1

                # handel header lines
                if line[0] in self._header_char:

                    if "version" in line:
                        continue

                    if "##sequence-region" in line:
                        split = line.find(' ')
                        if split == -1:
                            raise IOError(
                                "Invalid GFF file! No 'seqid' region header in line {c}".format(
                                    c=counter))
                        key = line[split:]
                        split = key.find(' ')
                        if split == -1:
                            raise IOError(
                                "Invalid GFF file! No 'seqid' region header in line {c}".format(
                                    c=counter))
                        key = key[0:split]
                        key = key.lstrip()
                        self._header_region[key] = line
                    else:
                        self._header_general.append(line)
                    continue

                # find reference_sequence
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'seqid' entry in line {c}".format(
                            c=counter))
                seqid = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find source
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'source' entry in line {c}".format(
                            c=counter))
                source = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find method
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'type' entry in line {c}".format(
                            c=counter))
                type = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find start
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'start' entry in line {c}".format(
                            c=counter))
                start = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find stop
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'end' entry in line {c}".format(
                            c=counter))
                end = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find score
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'score' entry in line {c}".format(
                            c=counter))
                if line[0:split] == '.':
                    score = None
                else:
                    score = float(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find strand
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'strand' entry in line {c}".format(
                            c=counter))
                strand = line[0:split]
                line = line[split + 1:]
                line = line.lstrip(splitter)

                # find phase
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid GFF file! No 'phase' entry in line {c}".format(
                            c=counter))
                if line[0:split] == '.':
                    phase = None
                else:
                    phase = int(line[0:split])
                line = line[split + 1:]

                # remove remaining tab and line end character
                line = line.lstrip()
                line = line.rstrip()

                entry = GFF3Entry(seqid, source, type, start, end, score=score,
                                  strand=strand, phase=phase)

                gsplitter = ';'
                separator = '='
                attributes = {}
                while len(line) > 0:

                    # extract  and value
                    split = line.find(gsplitter)
                    if split == -1:
                        split = len(line)

                    keyvalue = line[0:split]
                    key, _, value = keyvalue.partition(separator)

                    attributes[key] = value
                    line = line[split + 1:]
                    line = line.lstrip(gsplitter)
                    line = line.rstrip(gsplitter)
                    line = line.lstrip()
                    line = line.rstrip()
                if len(attributes) > 0:
                    entry.attributes = attributes
                if validate:
                    if not entry.valid:
                        raise IOError(
                            "Invalid GFF file! Entry in line {c} is {e}".format(
                                c=counter, e=str(entry)))

                # check if key is already there
                self.append(entry)

    def __write3(self, fname, validate):
        with open(fname, 'w') as file:
            head = "##gff-version 3 \n"
            if self._header_general[0] != head:
                self._header_general.insert(0, head)

            # write header first
            for item in self._header_general:
                file.write(item)

            # write data
            for key in self._keys:
                if key in self._header_region:
                    for item in self._header_region[key]:
                        file.write(item)

                for item in self._data[key]:
                    if validate:
                        if not item.valid:
                            raise ValueError(
                                "Can not write file due to invalid GFF entry: " + str(
                                    item))
                        file.write(str(item))
