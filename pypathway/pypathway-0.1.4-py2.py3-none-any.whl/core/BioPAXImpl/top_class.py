

# Ontology root class
# Definition: A discrete biological unit used when describing pathways.
class Entity:
    def __init__(self, availability=None, comment=None, dataSource=None, evidence=None,
                 name=None, xref=None):
        self.availability = availability
        self.comment = comment
        self.dataSource = dataSource
        self.evidence = evidence
        self.name = name
        self.xref = xref

    def __repr__(self):
        return str(self.__dict__) + "\n"


# Pathway
# Definition: A set or series of interactions, often forming a network,
# which biologists have found useful to group together for organizational,
# historic, biophysical or other reasons. Pathways can also contain sub- pathways.
class Pathway(Entity):
    def __init__(self, organism=None, pathwayComponent=None, pathwayOrder=None, availavlity=None,
                 comment=None, dataSource=None, evidence=None, name=None, xref=None):
        Entity.__init__(self, availavlity, comment, dataSource, evidence, name, xref)
        self.organism = organism
        # one or more object: Interaction or object: Pathway
        self.pathwayComponent = pathwayComponent
        # 0 or more object: PathwayStep
        self.pathwayOrder = pathwayOrder


# Interaction
# Definition: A biological relationship between two or more entities.
# An interaction is defined by the entities it relates.
# Warning: Interaction is a highly abstract class and use its subclass
class Interaction(Entity):
    def __init__(self, interactionType=None, participant=None, availability=None, comment=None, dataSource=None, evidence=None,
                 name=None, xref=None):
        Entity.__init__(self, availability, comment, dataSource, name, xref)
        # 0 or more object:InteractionVocabulary)
        self.interactionType = interactionType
        # 0 or more object:Entity
        self.participant = participant


# PhysicalEntity
# Definition: A pool of entities, where each entity has a physical structure.
class PhysicalEntity(Entity):
    def __init__(self, cellularLocation=None, feature=None, memeberPhtsicalEntity=None, notFeature=None,
                 availability=None, comment=None, dataSource=None, evidence=None, name=None, xref=None):
        Entity.__init__(self, availability, comment, dataSource, evidence, name, xref)
        # 0 or 1 object:CellularLocationVocabulary
        self.cellularLocation = cellularLocation
        # 0 or more object:EntityFeature
        self.feature = feature
        self.memberPhysicalEntity = memeberPhtsicalEntity
        self.notFeature = notFeature


# Gene
# Definition: An entity that encodes information that can be inherited through replication.
class Gene(Entity):
    def __init__(self, organism=None, availability=None, comment=None, dataSource=None, evidence=None,
                 name=None, xref=None):
        Entity.__init__(self, availability, comment, dataSource, evidence, name, xref)
        # 0 or 1 object:BioSource
        self.organism = organism