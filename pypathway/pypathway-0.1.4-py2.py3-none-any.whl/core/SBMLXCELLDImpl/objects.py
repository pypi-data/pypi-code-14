from xml.sax import ContentHandler, parseString
from libsbml import *
import libsbgnpy.libsbgn as libsbgn
from libsbgnpy.libsbgnTypes import GlyphClass, ArcClass, Language, Orientation


class Reaction:
    def __init__(self, annotation):
        self.anno = annotation
        self.reactants = []
        self.products = []
        self.reactant_links = []
        self.product_links = []
        self.type = None
        self.connectScheme = None
        self.line = []
        self._reslove()
        print self.anno.summary()

    def _reslove(self):
        # Reaction type, must has
        self.type = self.anno.get_child("reactionType").value
        self.line = [self.anno.get_child("line").props["color"], self.anno.get_child("line").props["width"]]
        # these two must exist
        for x in self.anno.get_child("baseReactants").find_by_class("baseReactant"):
            self.reactants.append([x.props["alias"], x.props["species"]])
        for x in self.anno.get_child("baseProducts").find_by_class("baseProduct"):
            self.products.append([x.props["alias"], x.props["species"]])
        self.connectScheme = self.anno.get_child("connectScheme").props["connectPolicy"]
        if self.anno.get_child("listOfReactantLinks"):
            # handle the ReactantLinks
            for x in self.anno.get_child("listOfReactantLinks").find_by_class("reactantLink"):
                self.reactant_links.append([x.props["reactant"], x.props["alias"], x.props["targetLineIndex"]])
        if self.anno.get_child("listOfProductLinks"):
            # handle the productLinks
            for x in self.anno.get_child("listOfProductLinks").find_by_class("productLink"):
                self.reactant_links.append([x.props["product"], x.props["alias"], x.props["targetLineIndex"]])
        if self.reactant_links:
            print "type: {}\nscheme: {}".format(self.type, self.connectScheme)
            print self.reactants
            print self.products
            print self.reactant_links
            print self.anno.get_child("offset")
            print self.anno.get_child("editPoints")
            if self.anno.get_child("listOfModification"):
                print self.anno.get_child("listOfModification").summary()
            print "-------------------------"


class SpeciesInfo:
    def __init__(self, in_complex, _class, name, position2compartment=None, complexID=None, homodimer=1,
                 list_of_mod=None, list_of_structural=None, list_of_catalyzed=None):
        self.in_complex = in_complex
        self._class, self.position2compartment, self.complexID = _class, position2compartment, complexID
        self.homodimer, self.list_of_mod, self.list_of_structural = homodimer, list_of_mod, list_of_structural
        self.list_of_catalyzed, self.name = list_of_catalyzed, name
        # infomation that we want to user to fill
        self.id, self.name, self.bbox, self.compartmentRef, \
        self.activity, self.view_state = None, None, None, None, None, None

    def __repr__(self):
        basic = "{}, {}, {}, {}, {}, {}, {}, {}".format(self.in_complex, self.complexID, self.position2compartment,
                                               self._class, self.name, self.list_of_mod, self.list_of_catalyzed,
                                                       self.list_of_structural)
        addition = "\nid:{}, name:{}, bbox:{}, cf: {}, act: {}, vs: {}".format(
            self.id, self.name, self.bbox, self.compartmentRef, self.activity, self.view_state
        )
        return basic + addition

    def file_info(self, id, name, bbox, compartmentRef, activity, view_state):
        self.id, self.name, self.bbox, self.compartmentRef, \
        self.activity, self.view_state = id, name, bbox, compartmentRef, activity, view_state

    def sbgn(self):
        '''
        depend on current info return a sbgn-pd glyph element
        :return: a sbgn glyph element
        '''
        map_to = {
            "PROTEIN": GlyphClass.MACROMOLECULE, "GENE": GlyphClass.NUCLEIC_ACID_FEATURE,
            "RNA": GlyphClass.NUCLEIC_ACID_FEATURE, "ANTISENSE_RNA": GlyphClass.NUCLEIC_ACID_FEATURE,
            "PHENOTYPE": GlyphClass.UNSPECIFIED_ENTITY, "ION": GlyphClass.SIMPLE_CHEMICAL,
            "SIMPLE_MOLECULE": GlyphClass.SIMPLE_CHEMICAL, "DRUG": GlyphClass.MACROMOLECULE,
            "UNKNOWN": GlyphClass.UNSPECIFIED_ENTITY, "COMPLEX": GlyphClass.COMPLEX
        }
        to_complex = {
            GlyphClass.MACROMOLECULE: GlyphClass.MACROMOLECULE_MULTIMER,
            GlyphClass.NUCLEIC_ACID_FEATURE: GlyphClass.NUCLEIC_ACID_FEATURE_MULTIMER,
            GlyphClass.SIMPLE_CHEMICAL: GlyphClass.SIMPLE_CHEMICAL_MULTIMER,
        }
        class_ = map_to[self._class] if self.homodimer == 1 else to_complex[map_to[self._class]]
        g = libsbgn.glyph(class_=class_, id=self.id)    #, compartmentRef=self.compartmentRef)
        g.set_label(libsbgn.label(text=self.name))
        g.set_bbox(libsbgn.bbox(*self.bbox))
        if self.homodimer > 1:
            ui = libsbgn.glyph(class_=GlyphClass.UNIT_OF_INFORMATION, id=self.id+"ui")
            ui.set_bbox(libsbgn.bbox(float(self.bbox[0]) + float(self.bbox[2]) / 2, float(self.bbox[1]) - 11, 30, 22))
            ui.set_label(libsbgn.label(text="N:{}".format(self.homodimer)))
            g.add_glyph(ui)
        for i, md in enumerate(self.modification_generate(self.list_of_mod, self.bbox)):
            state = libsbgn.glyph(class_=GlyphClass.STATE_VARIABLE, id=self.id + str(i))
            state.set_bbox(libsbgn.bbox(float(md[1][0]) - 11, float(md[1][1]) - 11, 22, 22))
            state.set_state(libsbgn.stateType(value=md[0]))
            g.add_glyph(state)
        return g

    def modification_generate(self, list_of_modification, bbox):
        def2lab = {
            "phosphorylated": "P",
            "empty": " ",
            "acetylated": "Ac",
            "ubiquitinated": "Ub",
            "methylated": "Me",
            "hydroxylated": "OH",
            "glycosylated": "G",
            "myristoylated": "My",
            "palmytoyated": "Pa",
            "prenylated": "Pr",
            "protonated": "H",
            "sulfated": "S",
            "don't care": "*",
            "unknown": "?"
        }
        candidate_bbox = [(bbox[0], bbox[1]), (bbox[0], float(bbox[1]) + float(bbox[3])),
                          (float(bbox[0]) + float(bbox[2]), bbox[1]),
                          (float(bbox[0]) + float(bbox[2]), float(bbox[1]) + float(bbox[3]))]
        return [(def2lab[x[1]], candidate_bbox[i]) for i, x in enumerate(list_of_modification)]


class Heap(list):
    def __init__(self):
        list.__init__([])

    def push(self, element):
        self.insert(0, element)

    def peak(self):
        return self[0]


class TreeNode:
    def __init__(self, _class, props, is_root=False):
        self._class = _class
        self.props = props
        self.is_root = is_root
        self.children = []
        self.father = None
        self.value = None

    def add_child(self, child):
        self.children.append(child)

    def set_father(self, father):
        self.father = father

    def summary(self, depth=0):
        self_str = "\t" * depth + "{}: {}, value: {}\n".format(self._class,
                                   ", ".join(["{}: {}".format(k, v) for k, v in self.props.items()]),
                                                               self.value)
        for x in self.children:
            self_str += x.summary(depth=depth+1)
        return self_str

    def __repr__(self):
        return "class: {}, props: {}, value: {}".format(self._class,
                                             ",".join(["{}: {}".format(k, v) for k, v in self.props.items()]),
                                                        self.value)

    def _find_by_class(self, _class, result):
        if self._class == _class:
            result.append(self)
        for x in self.children:
            x._find_by_class(_class, result)

    def find_by_class(self, _class):
        # if not self.is_root:
        #     return None
        result = []
        self._find_by_class(_class, result)
        return result

    def get_child(self, _class):
        for x in self.children:
            if x._class == _class:
                return x
        else:
            return None

    @staticmethod
    def parse(data):
        hander = CELLDHandler()
        parseString(data, hander)
        return hander.root


# A Handler class
class CELLDHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.gap = 0
        self.root = None
        self.heap = Heap()
        self.current_content = ""

    def startElement(self, name, attrs):
        if name == "annotation":
            self.root = TreeNode(name, attrs, True)
            self.heap.push(self.root)
            return
        name = name.replace("celldesigner:", "")
        node = TreeNode(name, attrs)
        father = self.heap.peak()
        father.add_child(node)
        node.set_father(father)
        self.heap.push(node)

    def endElement(self, name):
        name = name.replace("celldesigner:", "")
        if not self.heap.peak()._class == name:
            exit()
            raise Exception("Unclosed Tag")
        self.heap.pop(0)

    def characters(self, content):
        self.heap.peak().value = content.strip()


class SBML2SBGN:
    def __init__(self, file):
        # Init SBGN first:
        self.sbgn = libsbgn.sbgn()
        self.map = libsbgn.map()
        self.map.set_language(Language.PD)
        self.sbgn.set_map(self.map)
        # Load SBML
        reader = SBMLReader()
        document = reader.readSBML(file)
        model = document.getModel()
        self.model = model
        self.anno = TreeNode.parse(model.getAnnotationString())
        self.canvas = None
        self.overall()
        self.compartment()
        self.species()
        self.reaction()

    def overall(self):
        # print "[INF]: Try to get canvas size:"
        # canvas size:
        canvas = self.anno.find_by_class("modelDisplay")[0]
        self.canvas = [float(canvas.props["sizeX"]), float(canvas.props["sizeY"])]
        box = libsbgn.bbox(x=0, y=0, w=canvas.props["sizeX"], h=canvas.props["sizeY"])
        self.map.set_bbox(bbox=box)
        # print "[INF]: Get canvas size done"

    def compartment(self):
        '''
        This function, convert the compartment in the cell design to the SBGN-PD's compartment.
        :return:
        '''
        # handle compartment
        compartmentAlias = self.anno.find_by_class("compartmentAlias")
        # for x in compartmentAlias:
        #     print x.summary()
        for x in self.model.getListOfAllElements():
            if x.getElementName() == "compartment":
                # print x.id, x.name
                if x.id == "default":
                    continue
                alias = ""
                for c in compartmentAlias:
                    if c.props["compartment"] == x.id:
                        alias = c
                        break
                point = alias.get_child("point")
                _class = alias.get_child("class")
                # print point.props["x"], point.props["y"], _class.value
                box = self.get_square_rect([float(point.props["x"]), float(point.props["y"])], _class.value)
                compartment = libsbgn.glyph(class_=GlyphClass.COMPARTMENT, id=x.id)
                compartment.set_bbox(libsbgn.bbox(*box))
                compartment.set_label(libsbgn.label(text=x.name))
                self.map.add_glyph(compartment)

    def species(self):
        includeSpecies = self.anno.find_by_class("species")
        complex_element_list = []
        for x in includeSpecies:
            sf = self.species_anno_handle(x.get_child("annotation"))
            setattr(x, "id", x.props["id"])
            setattr(x, "name", x.props["name"])
            self.species_characters_handle(sf, x)
            #self.map.add_glyph(sf.sbgn())
            complex_element_list.append(sf)
        for x in self.model.getListOfAllElements():
            if x.getElementName() == "species":
                # print x.id, x.name, x.compartment
                sf = self.species_anno_handle(TreeNode.parse(x.getAnnotationString()))
                self.species_characters_handle(sf, x)
                childerns = []
                if sf._class == "COMPLEX":
                    childerns = [x for x in complex_element_list if x.complexID == sf.id]
                    bbox = self.handle_complex_size([x.bbox for x in childerns])
                    sf.bbox = bbox
                glyph = sf.sbgn()
                for c in childerns:
                    glyph.add_glyph(c.sbgn())
                self.map.add_glyph(glyph)
                # handle modification
                # if sf.list_of_mod:
                #     print "mod: {}".format(sf.list_of_mod)
                # if sf.list_of_structural:
                #     print "mod: {}".format(sf.list_of_structural)
        # The complex internal element is in the position of Model.Annotation: listOfIncludedSpecies
        # print "[INF]: Modification"
        # print [x for x in self.anno.find_by_class("modification")]
        # self.sbgn.write_file("/Users/sheep/test2.sbgn")

    def reaction(self):
        for x in self.model.getListOfAllElements():
            if x.getElementName() == "reaction":
                if x.id == "r38":
                    r = Reaction(TreeNode.parse(x.getAnnotationString()))


    def export(self):
        pass

    # Utils function
    def get_square_rect(self, point, word):
        if not self.canvas:
            raise Exception("canvas not set")
        if word == "SQUARE_CLOSEUP_NORTH":
            return [0, point[1], self.canvas[0], self.canvas[1] - point[1]]
        elif word == "SQUARE_CLOSEUP_EAST":
            return [0, 0, point[0], self.canvas[1]]
        elif word == "SQUARE_CLOSEUP_WEST":
            return [point[0], 0, self.canvas[0] - point[0], self.canvas[1]]
        elif word == "SQUARE_CLOSEUP_SOUTH":
            return [0, 0, self.canvas[0], point[1]]
        elif word == "SQUARE_CLOSEUP_NORTHWEST":
            return [point[0], point[1], self.canvas[0] - point[0], self.canvas[1] - point[1]]
        elif word == "SQUARE_CLOSEUP_NORTHEAST":
            return [0, point[1], point[0], self.canvas[1] - point[1]]
        elif word == "SQUARE_CLOSEUP_SOUTHWEST":
            return [point[0], 0, self.canvas[0] - point[0], point[1]]
        elif word == "SQUARE_CLOSEUP_SOUTHEAST":
            return [0, 0, point[0], point[1]]

    def species_anno_handle(self, tree):
        '''
        Handle the annotation used by species, return the information.
        :return:
        '''
        # print tree.summary()
        is_complex, p2c, cid, hd, list_of_mod, list_of_state, list_of_cata = None, None, None, None, [], [], []
        name, _class = "", ""
        if tree.get_child("positionToCompartment"):
            is_complex = False
            p2c = tree.get_child("positionToCompartment").value
        else:
            cid = tree.get_child("complexSpecies").value
        si = tree.get_child("speciesIdentity")
        name = si.get_child("name").value if si.get_child("name") else ""
        _class = si.get_child("class").value
        if not si.get_child("state"):
            # seems no modification.
            hd = 1
        else:
            si = si.get_child("state")
            hd = si.get_child("homodimer").value if si.get_child("homodimer") else 1
            if si.get_child("listOfModifications"):
                for x in si.get_child("listOfModifications").children:
                    # print x.props["residue"], x.props["state"]
                    list_of_mod.append([x.props["residue"], x.props["state"]])
            if si.get_child("listOfStructuralStates"):
                for x in si.get_child("listOfStructuralStates").children:
                    list_of_state.append([x.props["structuralState"]])
            if si.get_child("listOfCatalyzedReactions"):
                for x in si.get_child("listOfCatalyzedReactions").children:
                    list_of_cata.append([x.props["reaction"]])
        # print list_of_mod
        return SpeciesInfo(is_complex, _class, name, p2c, cid, hd, list_of_mod, list_of_state, list_of_cata)

    def species_characters_handle(self, sf, s):
        complexSpeciesAliases = self.anno.find_by_class("complexSpeciesAlias")
        speciesAlign = self.anno.find_by_class("speciesAlias")
        if sf._class == "COMPLEX":
            for x in complexSpeciesAliases:
                if s.id == x.props["species"]:
                    # print(s)
                    props = dict(x.get_child("bounds").props)
                    sf.file_info(s.id, s.name, [props["x"], props["y"], props["w"], props["h"]],
                                 x.props["compartmentAlias"], x.get_child("activity").value,
                                 x.get_child("view").props["state"])
        else:
            for x in speciesAlign:
                if s.id == x.props["species"]:
                    props = dict(x.get_child("bounds").props)
                    ca = dict(x.props).get("compartmentAlias")
                    sf.file_info(s.id, s.name, [props["x"], props["y"], props["w"], props["h"]],
                                 ca, x.get_child("activity").value,
                                 x.get_child("view").props["state"])
            pass

    def handle_complex_size(self, sets):
        '''
        The complex bbox, however, bad!
        :param sets: a list of element in the complex
        :return: the bbox of complex
        '''
        xs = [float(x[0]) for x in sets] + [float(x[0]) + float(x[2]) for x in sets]
        ys = [float(x[1]) for x in sets] + [float(x[1]) + float(x[3]) for x in sets]
        return [min(xs) - 3, min(ys) - 3, max(xs) - min(xs) + 6, max(ys) - min(ys) + 6]


class VisibleSBML:
    def __init__(self, model):
        self.model = model

    def handle_annotation(self):
        pass

    def convert_to(self):
        pass

def sbgn_test():
    sbgn = libsbgn.sbgn()
    map = libsbgn.map()
    map.set_language(Language.PD)
    sbgn.set_map(map)

    box = libsbgn.bbox(x=0, y=0, w=363, h=253)
    map.set_bbox(bbox=box)

    # glyphs with labels
    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id='glyph1')
    g.set_label(libsbgn.label(text='Ethanol'))
    g.set_bbox(libsbgn.bbox(x=40, y=120, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id='glyph_ethanal')
    g.set_label(libsbgn.label(text='Ethanal'))
    g.set_bbox(libsbgn.bbox(x=220, y=110, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.MACROMOLECULE, id='glyph_adh1')
    g.set_label(libsbgn.label(text='ADH1'))
    g.set_bbox(libsbgn.bbox(x=106, y=20, w=108, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id='glyph_h')
    g.set_label(libsbgn.label(text='H+'))
    g.set_bbox(libsbgn.bbox(x=220, y=190, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id='glyph_nad')
    g.set_label(libsbgn.label(text='NAD+'))
    g.set_bbox(libsbgn.bbox(x=40, y=190, w=60, h=60))
    map.add_glyph(g)

    g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id='glyph_nadh')
    g.set_label(libsbgn.label(text='NADH'))
    g.set_bbox(libsbgn.bbox(x=300, y=150, w=60, h=60))
    map.add_glyph(g)

    # glyph with ports (process)
    g = libsbgn.glyph(class_=GlyphClass.PROCESS, id='pn1',
                      orientation=Orientation.HORIZONTAL)
    g.set_bbox(libsbgn.bbox(x=148, y=168, w=24, h=24))
    map.add_glyph(g)

    # arcs
    # create arcs and set the start and end points
    a = libsbgn.arc(class_=ArcClass.CONSUMPTION, source="glyph1", target="pn1", id="a01")
    a.set_start(libsbgn.startType(x=98, y=160))
    a.set_end(libsbgn.endType(x=136, y=180))
    map.add_arc(a)

    a = libsbgn.arc(class_=ArcClass.PRODUCTION, source="pn1", target="glyph_nadh", id="a02")
    a.set_start(libsbgn.startType(x=184, y=180))
    a.set_end(libsbgn.endType(x=300, y=180))
    map.add_arc(a)

    a = libsbgn.arc(class_=ArcClass.CATALYSIS, source="glyph_adh1", target="pn1", id="a03")
    a.set_start(libsbgn.startType(x=160, y=80))
    a.set_end(libsbgn.endType(x=160, y=168))
    map.add_arc(a)

    a = libsbgn.arc(class_=ArcClass.PRODUCTION, source="pn1", target="glyph_h", id="a04")
    a.set_start(libsbgn.startType(x=184, y=180))
    a.set_end(libsbgn.endType(x=224, y=202))
    map.add_arc(a)

    a = libsbgn.arc(class_=ArcClass.PRODUCTION, source="pn1", target="glyph_ethanal", id="a05")
    a.set_start(libsbgn.startType(x=184, y=180))
    a.set_end(libsbgn.endType(x=224, y=154))
    map.add_arc(a)

    a = libsbgn.arc(class_=ArcClass.CONSUMPTION, source="glyph_nad", target="pn1", id="a06")
    a.set_start(libsbgn.startType(x=95, y=202))
    a.set_end(libsbgn.endType(x=136, y=180))
    map.add_arc(a)

    # write everything to a file
    sbgn.write_file('/Users/sheep/test.sbgn')

if __name__ == '__main__':
    convert = SBML2SBGN("/Users/sheep/Downloads/JAK_STAT_signaling_pathway.xml")
    #sbgn_test()
