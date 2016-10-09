# This file implements the subclass of Interaction
# There are five: Control, Conversion,
# GeneticInteraction, MolecularInteraction and TemplateReaction.
from core.BioPAXImpl.top_class import Interaction


# Control
# Definition: An interaction in which one entity regulates, modifies, or otherwise influences another.
# The targets of control processes (i.e. values of the controlled property) should be Interactions or Pathways
# subclass: Catalysis, Modulation, TemplateReactionRegulation
class Control(Interaction):
    def __init__(self, controlled=None, controller=None, controlType=None, availability=None, comment=None,
                 dataSource=None, evidence=None, interactionType=None, name=None, participant=None, xref=None):
        Interaction.__init__(self, interactionType, participant, availability,
                             comment, dataSource, evidence, name, xref)
        # 0 or 1 object:Interaction or object:Pathway
        self.controlled = controlled
        # 0 or more object:PhysicalEntity or object:Pathway
        self.controller = controller
        # relationship: maybe, ACTIVATION, INHIBITION (not in Catalysis) !!<should be implement as a enum or class>
        self.controlType = controlType


# Conversion
# Definition: An interaction in which one or more physical entities
# is physically transformed into one or more other ones.
# Subclasses: BiochemicalReaction, ComplexAssembly, Degradation, Transport
class Conversion(Interaction):
    def __init__(self, conversionDirection=None, left=None, right=None, participant=None,
                 participantStoichiometry=None, spontaneous=None, availability=None, comment=None, dataSource=None,
                 evidence=None, interactionType=None, name=None, xref=None):
        Interaction.__init__(self, interactionType, participant, availability, comment,
                             dataSource, evidence, name, xref)
        self.conversionDirection = conversionDirection
        # 0 or more object:PhysicalEntity
        self.left = left
        # 0 or more object:PhysicalEntity
        self.right = right
        self.participant = participant
        self.participanttStoichiometry = participantStoichiometry
        self.spontaneous = spontaneous


# GeneticInteraction
# Definition: Genetic interactions between genes occur when two genetic perturbations (e.g. mutations)
#  have a combined phenotypic effect not caused by either perturbation alone.
class GeneticInteraction(Interaction):
    def __init__(self, interactionScore=None, interactionType=None, participant=None, phenotype=None,
                 availability=None, comment=None, dataSource=None, evidence=None, name=None, xref=None):
        Interaction.__init__(self, interactionType, participant, availability, comment,
                             dataSource, evidence, name, xref)
        # super, participant: at least 2 Gene object
        # (0 or more object:Score) The score of an interaction e.g. a genetic interaction score.
        self.interactionScore = interactionScore
        # at least 1 object:PhenotypeVocabulary
        self.phenotype = phenotype


# MolecularInteraction
# Definition: An interaction involving molecular contact between physical entities.
#  The exact mechanism may not be known.
# Example: Two proteins observed to interact in a yeast-two-hybrid experiment
#  where there is not enough experimental evidence to suggest that the proteins are forming a complex by themselves
#  without any indirect involvement of other proteins.
class MolecularInteraction(Interaction):
    def __init__(self, participant=None, availability=None, comment=None, dataSource=None, evidence=None,
                 interactionType=None, name=None, xref=None):
        Interaction.__init__(self, interactionType, participant, availability, comment,
                             dataSource, evidence, name, xref)
        # so no new props


# TemplateReaction
# Definition: An interaction where a macromolecule is polymerized from a template macromolecule.
# Examples: DNA to RNA is transcription, RNA to protein is translation and DNA to protein is protein expression
#  from DNA. Other examples are possible.
class TemplateReaction(Interaction):
    def __init__(self, participant=None, product=None, template=None, templateDirection=None, availability=None,
                 comment=None, dataSource=None, evidence=None, interactionType=None, name=None, xref=None):
        Interaction.__init__(self, interactionType, participant, availability, comment,
                             dataSource, evidence, name, xref)
        # 0 or more object:DNARegion
        # DNARegion: which could encode a gene or other things, like transcription factor binding sites.
        # like a chromosome, a plasmid, chromosome 7 of Homo sapiens.
        # Parent class: PhysicalEntity
        # !!<should add impl here?: DNARegion>
        self.product = product
        self.template = template
        self.templateDirection = templateDirection


# ------------ Control subclasses ----------------

# Catalysis
# Definition: A control interaction in which a physical entity (a catalyst)
#  increases the rate of a conversion interaction by lowering its activation energy.
class Catalysis(Control):
    def __init__(self, catalysisDirection=None, cofactor=None, controlled=None, controller=None, controlType=None,
                 availability=None, comment=None, dataSource=None, evidence=None, interactionType=None,
                 name=None, participant=None, xref=None):
        Control.__init__(self, controlled, controller, controlType, availability, comment, dataSource, evidence,
                         interactionType, name, participant, xref)
        # Specifies the reaction direction of the interaction catalyzed by this instance of the catalysis class.
        # REVERSIBLE, PHYSIOL-LEFT-TO-RIGHT PHYSIOL-RIGHT-TO- LEFT, PHYSIOL-LEFT-TO-RIGHT PHYSIOL-RIGHT-TO- LEFT
        self.catalysisDirection = catalysisDirection
        # 0 or more object:PhyicalEntity
        self.cofactor = cofactor


# Modulation
# Definition: A control interaction in which a physical entity modulates a catalysis interaction.
class Modulation(Control):
    def __init__(self, controlled=None, controller=None, availability=None, comment=None, controlType=None,
                 dataSource=None, evidence=None, interactionType=None, name=None, participant=None, xref=None):
        Control.__init__(self, controlled, controller, controlType, availability, comment, dataSource, evidence,
                         interactionType, name, participant, xref)


# TemplateReactionRegulation
# Definition: Regulation of a TemplateReaction by a controlling physical entity.
class TemplateReactionRegulation(Control):
    def __init__(self, controlled=None, controller=None, controlType=None, availability=None, comment=None,
                 dataSource=None, evidence=None, interactionType=None, name=None, participant=None, xref=None):
        Control.__init__(self, controlled, controller, controlType, availability, comment, dataSource, evidence,
                         interactionType, name, participant, xref)

# ------------ Conversion subclasses -----------------


# BiochemicalReaction
# A conversion interaction in which one or more entities (substrates)
#  undergo covalent changes to become one or more other entities (products).
# Subclasses: TransportWithBiochemicalReaction
class BiochemicalReaction(Conversion):
    def __init__(self, deltaG=None, deltaH=None, deltaS=None, eCNumber=None, kEQ=None, participant=None,
                 availability=None, comment=None, conversionDirection=None, dataSource=None, evidence=None,
                 interactionType=None, left=None, name=None, participantStoichiometry=None, right=None,
                 spontaneous=None, xref=None):
        Conversion.__init__(self, conversionDirection, left, right, participant, participantStoichiometry, spontaneous,
                            availability, comment, dataSource, evidence, interactionType, name, xref)
        # standard transformed Gibbs energy change for a reaction written in terms of biochemical reactants
        self.deltaG = deltaG
        # standard transformed enthalpy change for a reaction written in terms of biochemical reactants
        self.deltaH = deltaH
        # standard transformed entropy change for a reaction written in terms of biochemical reactants
        self.deltaS = deltaS
        # The unique number assigned to a reaction by the Enzyme Commission of
        #  the International Union of Biochemistry and Molecular Biology.
        self.eCNumber = eCNumber
        # k,
        self.kEQ = kEQ


# ComplexAssembly
# Definition: A conversion interaction in which a set of physical entities, at least one being a macromolecule
#  (e.g. protein, RNA, or DNA), aggregate to from a complex physicalEntity.
class ComplexAssembly(Conversion):
    def __init__(self, participant=None, availability=None, comment=None, conversionDirection=None, dataSource=None,
                 evidence=None, interactionType=None, left=None, name=None, participantStoichiometry=None, right=None,
                 spontaneous=None, xref=None):
        Conversion.__init__(self, conversionDirection, left, right, participant, participantStoichiometry, spontaneous,
                            availability, comment, dataSource, evidence, interactionType, name, xref)


# Degradation
# Definition: The process of degrading a physical entity.
#  The physical entity is converted to unspecified degraded components.
class Degradation(Conversion):
    def __init__(self, conversionDirection=None, participant=None, availability=None, comment=None, dataSource=None,
                 evidence=None, interactionType=None, left=None, name=None, participantStoichiometry=None, right=None,
                 spontaneous=None, xref=None):
        Conversion.__init__(self, conversionDirection, left, right, participant, participantStoichiometry, spontaneous,
                            availability, comment, dataSource, evidence, interactionType, name, xref)


# Transport
# Definition: A conversion interaction in which a physical entity (or set of physical entities)
#  changes location within or with respect to the cell.
# Subclasses: TransportWithBiochemicalReaction
class Transport(Conversion):
    def __init__(self, participant=None, availability=None, comment=None, conversionDirection=None, dataSource=None,
                 evidence=None, interactionType=None, left=None, name=None, participantStoichiometry=None, right=None,
                 spontaneous=None, xref=None):
        Conversion.__init__(self, conversionDirection, left, right, participant, participantStoichiometry, spontaneous,
                            availability, comment, dataSource, evidence, interactionType, name, xref)


# TransportWithBiochemicalReaction a sub cclass of BiochemicalReaction
# Definition: A conversion interaction that is both a BiochemicalReaction and a Transport.
class TransportWithBiochemicalReaction(BiochemicalReaction):
    def __init__(self, participant=None, availability=None, comment=None, conversionDirection=None, dataSource=None,
                 deltaG=None, deltaH=None, deltaS=None, eCNumber=None, evidence=None, interactionType=None, kEQ=None,
                 left=None, name=None, partipantStoichiometry=None, right=None, spontaneous=None, xref=None):
        BiochemicalReaction.__init__(self, deltaG, deltaH, deltaS, eCNumber, kEQ, participant, availability,
                                     comment, conversionDirection, dataSource, evidence, interactionType, left, name,
                                     partipantStoichiometry, right, spontaneous, xref)
