# A number of properties in the ontology accept instances of utility classes as values.
# Utility classes are created when simple properties are insufficient to describe an aspect of an entity.
# This is a placeholder for classes, used for annotating the "Entity" and its subclasses.
# Mostly, these are not an "Entity" themselves. Examples include references to external databases,
# controlled vocabularies, evidence and provenance. Utility subclasses

# There are 15 direct subclasses of UtilityClass: BioSource, ChemicalStructure, ControlledVocabulary, DeltaG,
# EntityFeature, EntityReference, Evidence, ExperimentalForm, kPrime, PathwayStep, Provenance, Score, SequenceLocation,
# Stoichiometry, and Xref.


class Utility:
    def __init__(self):
        pass


# Definition: The biological source of an entity
class BioSource(Utility):
    def __init__(self, cellType=None, name=None, Xref=None, tissue=None, comment=None):
        Utility.__init__(self)
        # 0 or more object:CellVocabulary e.g. 'HeLa'
        self.cellType = cellType
        # String
        self.name = name
        # instance of UnificationXref
        self.Xref = Xref
        # instance of TissueVocabulary
        self.tissue = tissue
        self.comment = comment


# Definition: Used to describes a small molecule structure.
class ChemicalStructure(Utility):
    def __init__(self, structureData=None, structureFormat=None, comment=None):
        Utility.__init__(self)
        # String
        self.structureData = structureData
        # String
        self.structureFormat = structureFormat
        self.comment = comment


# Definition: Used to reference terms from external controlled vocabularies (CVs) from the ontology.
# Subclasses: CellularLocationVocabulary, CellVocabulary, EntityReferenceTypeVocabulary, EvidenceCodeVocabulary,
#  ExperimentalFormVocabulary, InteractionVocabulary, PhenotypeVocabulary, RelationshipTypeVocabulary,
#  SequenceModificationVocabulary, SequenceRegionVocabulary, TissueVocabulary
class ControlledVocabulary(Utility):
    def __init__(self, term, xref, comment):
        Utility.__init__(self)
        # String
        self.term = term
        # Instance of UnificationXref
        self.xref = xref
        self.comment = comment


# Definition: For biochemical reactions,
# this property refers to the standard transformed Gibbs energy change for a reaction
class DeltaG(Utility):
    def __init__(self, deltaGPrimeO=None, ionicStrength=None, pH=None, pMg=None, temperature=None, comment=None):
        Utility.__init__(self)
        # float
        self.deltaGPrimeO = deltaGPrimeO
        # float
        self.ionicStrength = ionicStrength
        # float
        self.pMg = pMg
        # float
        self.pH = pH
        # float
        self.temperature = temperature
        self.comment = comment


# Definition: A feature or aspect of a physical entity that can be changed
# while the entity still retains its biological identity.
# Subclasses: BindingFeature, FragmentFeature, ModificationFeature
class EntityFeature(Utility):
    def __init__(self, evidence=None, featureLocation=None, featureLocationType=None, memberFeature=None, comment=None):
        Utility.__init__(self)
        # instance of Evidence
        self.evidence = evidence
        # instance of SequenceLocation
        self.featureLocation = featureLocation
        self.featureLocationType = featureLocationType
        self.memeberFeature = memberFeature
        self.comment = comment


# Definition: An entity reference is a grouping of several physical entities across different contexts and
#  molecular states, that share common physical properties and often named and treated as a single
#  entity with multiple states by biologists.
# Subclasses: DnaReference, ProteinReference, RnaReference, SmallMoleculeReference
class EntityReference(Utility):
    def __init__(self, entityFeature=None, entityReferenceType=None, evidence=None, memberEntityReference=None,
                 name=None, xref=None):
        Utility.__init__(self)
        # instance of EntityFeature
        self.entityFeature = entityFeature
        self.entityReferenceType = entityReferenceType
        # instance of Evidence
        self.evidence = evidence
        # instance of EntityReference
        self.memberEntityReference = memberEntityReference
        # String
        self.name = name
        # instance of Xref??
        self.xref = xref


# Definition: The scientific support for a particular assertion, such as the existence of an interaction or pathway.
class Evidence(Utility):
    def __init__(self, confidence=None, evidenceCode=None, experimentalForm=None, xref=None, comment=None):
        Utility.__init__(self)
        # instance of Score
        self.confidence = confidence
        # instance of EvidenceCodeVocabulary
        self.evidenceCode = evidenceCode
        # instance of ExperimentalForm
        self.experimentalForm = experimentalForm
        # instance of Xref
        self.xref = xref
        self.comment = comment


# Definition: The form of a physical entity in a particular experiment,
#  as it may be modified for purposes of experimental design.
class ExperimentalForm(Utility):
    def __init__(self, experimentalFeature=None, experimentalFormDescription=None,
                 experimentalFormEntity=None, comment=None):
        Utility.__init__(self)
        # instance of EntityFeature
        self.experimentalFeature = experimentalFeature
        # instance of ExperimentalFormVocabulary
        self.experimentalFormDescription = experimentalFormDescription
        # instance of PhysicalEntity or object:Gene)
        self.experimentalFormEntity = experimentalFormEntity
        self.comment = comment


# Definition: The apparent equilibrium constant, K', and associated values.
class kPrime(Utility):
    def __init__(self, ionicStrength=None, kPrime=None, ph=None, pMg=None, temperature=None, comment=None):
        Utility.__init__(self)
        # all float
        self.ionicStrength = ionicStrength
        self.kPrime = kPrime
        self.ph = ph
        self.pMg = pMg
        self.temperature = temperature
        self.comment = comment





