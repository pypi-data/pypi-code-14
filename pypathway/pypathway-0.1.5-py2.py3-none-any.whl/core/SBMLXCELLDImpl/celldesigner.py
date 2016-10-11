# Define the cell designer class here


class TreeNode:
    def __init__(self):
        pass


class Bound:
    def __init__(self, h, w, x, y):
        self.h, self.w, self.x, self.y = h, w, x, y


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


# The inner relative type
class InnerPosition:
    def __init__(self, x, y):
        self.x, self.y = x, y


class BoxSize:
    def __init__(self, width, height):
        self.width, self.height = width, height


class SingleLine:
    def __init__(self, width):
        self.width = width


class DoubleLine:
    def __init__(self, innerWidth, outerWidth, thickness):
        self.innerWidth, self.outerWidth, self.thickness = thickness


# P25 usual, brief, complexnoborder
class View:
    def __init__(self, state):
        self.state = state


class UsualView:
    def __init__(self, boxSize, singleLine, paint, innerPosition=None):
        self.boxSize, self.singleLine, self.paint, self.innerPosition = boxSize, singleLine, paint, innerPosition


class BriefView:
    def __init__(self, boxSize, singleLine, paint, innerPosition):
        self.boxSize, self.singleLine, self.paint, self.innerPosition = boxSize, singleLine, paint, innerPosition


# The content is a xhtml
class Notes:
    def __init__(self, content):
        self.content = content


class Info:
    def __init__(self, state=None, prefix=None, label=None, angle=None):
        self.state, self.prefix, self.label, self.angle = state, prefix, label, angle


class ElementEnum:
    def __init__(self): pass
    PROTEIN = 0
    GENE = 1
    RNA = 2
    ANTISENSE_RNA = 3
    PHENOTYPE = 4
    ION = 5
    SIMPLE_MOLECULE = 6
    DRUG = 7
    UNKNOWN = 8
    COMPLEX = 9
    SQUARE = 10
    OVAL = 11
    SQUARE_CLOSEUP_NORTHWEST = 12
    SQUARE_CLOSEUP_NORTHEAST = 13
    SQUARE_CLOSEUP_SOUTHWEST = 14
    SQUARE_CLOSEUP_SOUTHEAST = 15
    SQUARE_CLOSEUP_NORTH = 16
    SQUARE_CLOSEUP_EAST = 17
    SQUARE_CLOSEUP_WEST = 18
    SQUARE_CLOSEUP_SOUTH = 19
    DEGRADED = 20

# They call this class, but not allowed
_Class = ElementEnum


class Name:
    def __init__(self, name):
        self.name = name


# active inactive
class Activity:
    def __init__(self, state):
        self.state = state


# The Extension of Model.Annotation
class ModelVersion:
    def __init__(self, version):
        self.version = version


class ModelDisplay:
    def __init__(self, sizeX, sizeY):
        self.sizeX, self.sizeY = sizeX, sizeY


class ListOfIncludedSpecies:
    def __init__(self, isRef=0, minOcc=0, maxOcc=0, content=0):
        self.isRef, self.minOcc, self.maxOcc, self.content = isRef, minOcc, maxOcc, content


class Species:
    def __init__(self, id, name=None, compartment=None, initialAmount=None, initialConcentration=None,
                 substanceUnits=None, spatialSizeUnits=None, hasOnlySubstanceUnits=None, boundaryCondition=None,
                 charge=None, constant=None):
        self.name, self.compartment, self.initialAmount = name, compartment, initialAmount
        self.initialConcentration, self.substanceUnits, self.spatialSizeUnits = initialConcentration, substanceUnits, spatialSizeUnits
        self.hasOnlySubstanceUnits, self.boundaryCondition = hasOnlySubstanceUnits, boundaryCondition
        self.charge, self.constant = charge, constant


# Caution!
class SpeciesAnnotion:
    def __init__(self, isRef=0, content="conplex"):
        self.isRef, self.content = isRef, content


class ListOfCompartmentAlias:
    def __init__(self, isRef=0, content="complex"):
        self.isRef = isRef
        self.content = content


class CompartmentAlias:
    def __init__(self, compartment, id):
        self.compartment = compartment
        self.id = id


class NamePoint:
    def __init__(self, x, y):
        self.x, self.y = x, y


class ListOfComplexSpeciesAliases:
    def __init__(self, isRef=0, content="complex"):
        self.isRef, self.content = isRef, content


class ComplexSpeciesAlias:
    def __init__(self, id, species, compartmentAlias=None, complexSpeciesAlias=None):
        self.id, self.species, self.compartmentAlias = id, species, compartmentAlias
        self.complexSpeciesAlias = complexSpeciesAlias


class StructuralStateAngle:
    def __init__(self, angle=0, minOcc=0, maxOcc=1, content="sample"):
        self.angle, minOcc, maxOcc, content = angle, minOcc, maxOcc, content


class ListOfSpeciesTag:
    def __init__(self, minOcc=0, maxOcc="unbounded", content="complex"):
        self.minOcc, self.maxOcc, self.content = minOcc, maxOcc, content


class SpeciesTag:
    def __init__(self):
        pass


class KeyInfo(TreeNode):
    def __init__(self, name, direct):
        TreeNode.__init__(self)
        self.name, direct = name, direct


class TagBound(TreeNode):
    def __init__(self, x, y, w, h):
        TreeNode.__init__(self)
        self.x, self.y, self.w, self.h = x, y, w, h


class TagEdgeLine(TreeNode):
    def __init__(self, width):
        TreeNode.__init__(self)
        self.width = width


class TagFramePaint(TreeNode):
    def __init__(self, data):
        TreeNode.__init__(self)
        self.data = data


class ListOfSpeciesAlias(TreeNode):
    def __init__(self, isRef=0, content="complex"):
        TreeNode.__init__(self)
        self.isRef, self.content = isRef, content


class SpeciesAlias(TreeNode):
    def __init__(self, id, species, compartmentAlias=None, complexSpeciesAlias=None):
        TreeNode.__init__(self)
        self.id, self.species, self.compartmentAlias, self.complexSpeciesAlias = id, species, compartmentAlias, complexSpeciesAlias


class ListOfGroup(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class Group(TreeNode):
    def __init__(self, id, members):
        TreeNode.__init__(self)
        self.id, self.members = id, members


class ListOfProtein(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class Protein(TreeNode):
    def __init__(self, id, name, type):
        TreeNode.__init__(self)
        self.id, self.name, self.type = id, name, type


class ListOfBindingRegions(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class BindingRegion(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class ListOfModificationResidues(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class ModificationResidue(TreeNode):
    def __init__(self, id, name=None, angle=None, side=None):
        TreeNode.__init__(self)
        self.id, self.name, self.angle, self.side = id, name, angle, side


class ListOfRegionsType(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class Region(TreeNode):
    def __init__(self, id, size, pos=None, type=None, name=None, active=None):
        TreeNode.__init__(self)
        self.id, self.size, self.pos, self.type, self.name, self.active = id, size, pos, type, name, active


class ListOfGenes(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class Gene(TreeNode):
    def __init__(self, id, name, type):
        TreeNode.__init__(self)
        self.id, self.name, self.type = id, name, type


class ListOfRNAs(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class RNA(TreeNode):
    def __init__(self, id, name, type):
        TreeNode.__init__(self)
        self.id, self.name, self.type = id, name, type


class ListOfAntisenseRNAs(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class AntisenseRNA(TreeNode):
    def __init__(self, id, name, type):
        TreeNode.__init__(self)
        self.id, self.name, self.type = id, name, type


class ListOfLayers(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class Layer(TreeNode):
    def __init__(self, locked, visible, id=None, name=None):
        TreeNode.__init__(self)
        self.locked, visible, id, name = locked, visible, id, name


class ListOfTexts(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class LayerSpeciesAlias(TreeNode):
    def __init__(self, targetType, targetID, x, y):
        TreeNode.__init__(self)
        self.targetType, targetID, x, y = targetType, targetID, x, y


class ListOfSquares(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class LayerCompartmentAlias(TreeNode):
    def __init__(self, type):
        TreeNode.__init__(self)
        self.type = type


class ListOfFreeLines(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class LayerFreeLine(TreeNode):
    def __init__(self, isArrow=None, isDotted=None):
        TreeNode.__init__(self)
        self.isArrow, self.isDotted = isArrow, isDotted


class ListOfBlockDiagrams(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class BlockDiagram(TreeNode):
    def __init__(self, protein):
        TreeNode.__init__(self)
        self.protein = protein


class Canvas(TreeNode):
    def __init__(self, height, width):
        TreeNode.__init__(self)
        self.height, self.width = height, width


class Block(TreeNode):
    def __init__(self, width, height, x, y, nameOffsetX, nameOffsetY):
        TreeNode.__init__(self)
        self.width, self.height, self.x, self.y, self.nameOffsetX, self.nameOffsetY = width, height, x, y, nameOffsetX, nameOffsetY


class Halo(TreeNode):
    def __init__(self, width, height, x, y):
        TreeNode.__init__(self)
        self.width, self.height, self.x, self.y = width, height, x, y


class ListOfResiduesInBlockDiagram(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class RresidueInBlockDiagram(TreeNode):
    def __init__(self, type, id, offsetX, name=None, residue=None, nameOffsetX=None, nameOffsetY=None):
        self.type, self.id, self.offsetX, self.name, self.residue = type, id, offsetX, name, residue
        self.nameOffsetX, self.nameOffsetY = nameOffsetX, nameOffsetY
        TreeNode.__init__(self)


class ListOfExternalNamesForResidue(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class ExternalNameForResidue(TreeNode):
    def __init__(self, id, offsetY, name, nameOffsetX, nameOffsetY, protein=None):
        TreeNode.__init__(self)
        self.id, self.offsetY, self.name, self.nameOffsetX = id, offsetY, name, nameOffsetX
        self.nameOffsetY, self.protein = nameOffsetY, protein


class ListOfExternalConnectionsInBlockDiagram(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class ExternalConnectionsInBlockDiagram(TreeNode):
    def __init__(self, residue, type, predefined):
        self.residue, self.type, self.predefined = residue, type, predefined
        TreeNode.__init__(self)


class ListOfBindingSitesInBlockDiagram(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class BindingSiteInBlockDiagram(TreeNode):
    def __init__(self, id, offsetY, name, nameOffsetX, nameOffsetY):
        TreeNode.__init__(self)
        self.id, self.offsetY, self.name, self.nameOffsetX = id, offsetY, name, nameOffsetX
        self.nameOffsetY = nameOffsetY


class ListOfEffectSitesInBlockDiagram(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class EffectSiteInBlockDiagram(TreeNode):
    def __init__(self, id, offsetY, name, nameOffsetX, nameOffsetY, reaction=None, species=None):
        TreeNode.__init__(self)
        self.id, self.offsetY, self.name, self.nameOffsetX = id, offsetY, name, nameOffsetX
        self.nameOffsetY, self.reaction, self.species = nameOffsetY, reaction, species


class EffectInBlockDiagram(TreeNode):
    def __init__(self, type):
        self.type = type
        TreeNode.__init__(self)


class EeffectTargetInBlockDiagram(TreeNode):
    def __init__(self, protein):
        TreeNode.__init__(self)
        self.protein = protein


class DegradedInBlockDiagram(TreeNode):
    def __init__(self, id, offsetY):
        self.id, self.offsetY = id, offsetY
        TreeNode.__init__(self)


class DegradedShapeInBlockDiagram(TreeNode):
    def __init__(self, width, height, offsetX, offsetY):
        self.width, self.height, self.offsetX, self.offsetY = width, height, offsetX, offsetY
        TreeNode.__init__(self)


class ListOfInternalOperatorsInBlockDiagram(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class InternalOperatorInBlockDiagram(TreeNode):
    def __init__(self, id, type, subType, offsetX, offsetY):
        self.id, self.type, self.subType, self.offsetX, self.offsetY = id, type, subType, offsetX, offsetY
        TreeNode.__init__(self)


class InternalOperatorValueInBlockDiagram(TreeNode):
    def __init__(self, value, offsetX, offsetY):
        TreeNode.__init__(self)
        self.value, self.offsetX, self.offsetY = value, offsetX, offsetY


class ListOfInternalLinksInBlockDiagram(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)


class InternalLinkInBlockDiagram(TreeNode):
    def __init__(self, id, type):
        self.id, self.type = id, type
        TreeNode.__init__(self)


class StartingPointInBlockDiagram(TreeNode):
    def __init__(self, offsetX, offsetY, residue=None, bindingSite=None, operator=None):
        self.offsetX, offsetY, self.residue, self.bindingSite, self.operator = offsetX, offsetY, residue, bindingSite, operator
        TreeNode.__init__(self)


class EndPointInBlockDiagram(TreeNode):
    def __init__(self, offsetX, offsetY, residue=None, bindingSite=None, operator=None, link=None, degrade=None):
        self.offsetX, offsetY, self.residue, self.bindingSite, self.operator = offsetX, offsetY, residue, bindingSite, operator
        self.link, self.degrade = link, degrade
        TreeNode.__init__(self)


# Compartment.Annotation
# has a Name, and is already defined

# Species.Annotation

class PositionToCompartment(TreeNode):
    def __init__(self, position):
        TreeNode.__init__(self)
        self.position = position


class ComplexSpecies(TreeNode):
    def __init__(self, sid):
        TreeNode.__init__(self)
        self.sid = sid


class SpeciesIdentity(TreeNode):
    def __init__(self):
        TreeNode.__init__(self)

















