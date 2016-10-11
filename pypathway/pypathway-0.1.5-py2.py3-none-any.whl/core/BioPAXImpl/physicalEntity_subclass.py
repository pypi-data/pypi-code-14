# This file implements the subclass of Interaction
# There are seven: DnaRegion, SmallMolecule, Dna, Rna, Complex, Protein, RnaRegion
from top_class import PhysicalEntity


# Complex
# Definition: A physical entity whose structure is comprised of other physical entities bound to each
#  other non-covalently, at least one of which is a macromolecule (e.g. protein, DNA, or RNA).
class Complex(PhysicalEntity):
    def __init__(self, component=None, componentStoichiometry=None, memberPhysicalEntity=None, availability=None,
                 cellularLocation=None, comment=None, dataSource=None, evidence=None, feature=None, name=None,
                 notFeature=None, xref=None):
        PhysicalEntity.__init__(self, cellularLocation, feature, memberPhysicalEntity, notFeature, availability,
                                comment, dataSource, evidence, name, xref)
        # 0 or more object:PhysicalEntity
        self.component = component
        # (0 or more object:Stoichiometry
        self.componentStoichiometry = componentStoichiometry
        # super, memberPhysicalEntity - (0 or more object:Complex) Used to create generic complexes.


# DNA
# Definition: A physical entity consisting of a sequence of deoxyribonucleotide monophosphates; a deoxyribonucleic acid.
class DNA(PhysicalEntity):
    def __init__(self, entityReference=None, memberPhysicalEntity=None, availability=None, cellularLocation=None,
                 comment=None, dataSource=None, evidence=None, feature=None, name=None, notFeature=None, xref=None):
        PhysicalEntity.__init__(self, cellularLocation, feature, memberPhysicalEntity, notFeature, availability,
                                comment, dataSource, evidence, name, xref)
        # 0 or more object:DNAReference,
        self.entityRerference = entityReference
        # super, memberPhysicalEntity - (0 or more object:DNA) Used to define a generic DNA molecule
        #  that is a collection of other DNA molecules.


# DNARegion
# Definition: A region of DNA.
class DNARegion(PhysicalEntity):
    def __init__(self, entityReference=None, memberPhysicalEntity=None, availability=None, cellularLocation=None,
                 comment=None, dataSource=None, evidence=None, feature=None, name=None, notFeature=None, xref=None):
        PhysicalEntity.__init__(self, cellularLocation, feature, memberPhysicalEntity, notFeature, availability,
                                comment, dataSource, evidence, name, xref)
        self.entityReference = entityReference


# Protein
# Definition: A physical entity consisting of a sequence of amino acids; a protein monomer; a single polypeptide chain.
class Protein(PhysicalEntity):
    def __init__(self, entityReference=None, memberPhysicalEntity=None, availability=None, cellularLocation=None,
                 comment=None, dataSource=None, evidence=None, feature=None, name=None, notFeature=None, xref=None):
        PhysicalEntity.__init__(self, cellularLocation, feature, memberPhysicalEntity, notFeature, availability,
                                comment, dataSource, evidence, name, xref)
        # 0 or more object:ProteinReference,
        self.entityRerference = entityReference
        # super, memberPhysicalEntity - (0 or more object:Protein) Used to define a generic Protein molecule
        #  that is a collection of other Protein molecules.


# RNA
# A physical entity consisting of a sequence of ribonucleotide monophosphates; a ribonucleic acid.
class RNA(PhysicalEntity):
    def __init__(self, entityReference=None, memberPhysicalEntity=None, availability=None, cellularLocation=None,
                 comment=None, dataSource=None, evidence=None, feature=None, name=None, notFeature=None, xref=None):
        PhysicalEntity.__init__(self, cellularLocation, feature, memberPhysicalEntity, notFeature, availability,
                                comment, dataSource, evidence, name, xref)
        # 0 or more object:RNAReference,
        self.entityRerference = entityReference
        # super, memberPhysicalEntity - (0 or more object:RNA) Used to define a generic RNA molecule
        #  that is a collection of other RNA molecules.


# RNARegion
# Definition: A region of RNA.
class RNARegion(PhysicalEntity):
    def __init__(self, entityReference=None, memberPhysicalEntity=None, availability=None, cellularLocation=None,
                 comment=None, dataSource=None, evidence=None, feature=None, name=None, notFeature=None, xref=None):
        PhysicalEntity.__init__(self, cellularLocation, feature, memberPhysicalEntity, notFeature, availability,
                                comment, dataSource, evidence, name, xref)
        self.entityReference = entityReference


# SmallMolecule
# Definition: A small bioactive molecule.
class SmallMolecule(PhysicalEntity):
    def __init__(self, entityReference=None, memberPhysicalEntity=None, availability=None, cellularLocation=None,
                comment=None, dataSource=None, evidence=None, feature=None, name=None, notFeature=None, xref=None):
        PhysicalEntity.__init__(self, cellularLocation, feature, memberPhysicalEntity, notFeature, availability,
                            comment, dataSource, evidence, name, xref)
        self.entityReference = entityReference

