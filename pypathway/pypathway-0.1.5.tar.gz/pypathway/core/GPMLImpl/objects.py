from xml.sax import parseString, ContentHandler
from ...core.objects import Pathway
import json
from ...utils import environment as env
from ...utils import GPMLCorrespondeNodeNotFound
import os
import shutil
from xml.dom.minidom import Document
import math
from ...visualize.options import IntegrationOptions


def contain(rect, source_z, target, target_z):
    if math.fabs(target[0] - rect[0]) <= rect[2] / 2.0 and math.fabs(target[1] - rect[1]) < rect[3] / 2.0 and int(target_z) > int(source_z):
        return True
    else:
        return False


class Shape:
    def __init__(self, type, x, g):
        self.type, self.x, self.g = type, x, g

    def generate(self):
        convert = {
            "Rectangle": "rectangle",
            "RoundedRectangle": "roundrectangle",
            "Oval": "ellipse",
            "Triangle": "triangle"
        }
        if self.type == "Rectangle" or self.type == "RoundedRectangle" or self.type == "Oval" or self.type == "Triangle":
            return [{
                "nodes": {
                    "data": {
                        "id": self.x.props["GraphId"],
                    },
                    "position": {
                        "x": int(float(self.g.props["CenterX"])),
                        "y": int(float(self.g.props["CenterY"])),
                    },
                    "group": "nodes",
                },
                "style": {
                    "selector": "#{}".format(self.x.props["GraphId"]),
                    "style": {
                        "shape": convert[self.g.props.get("ShapeType")],
                        "width": int(float(self.g.props["Width"])),
                        "height": int(float(self.g.props["Height"])),
                        "label": self.x.props.get("TextLabel") or "",
                        # the align of a label:
                        "text-halign": "center",
                        "text-valign": "center",
                        "text-max-width": int(float(self.g.props["Width"])),
                        "text-wrap": "wrap",
                        "background-color": "#{}".format(self.g.props.get("FillColor") or "fff"),
                        "border-width": "1px",
                        # "border-style": "dotted",
                        "border-color": "#000",
                        "opacity": 0.3 if int(float(self.g.props["Width"])) > 500 or int(float(self.g.props["Height"])) > 500 else 1,
                        "z-index": self.g.props["ZOrder"]
                    }
                }
            }]
        elif self.type == "Arc":
            # this means a pi degree circle.

            return None


class GPMLParser(Pathway):
    def __init__(self, _class, props, is_root=False):
        Pathway.__init__(self)
        self._class = _class
        self.props = props
        self._is_root = is_root
        self._children = []
        self._father = None
        self.value = None

    # the method general Pathway should provide
    # the convert the gpml to cytoscape.js's config, new we use pvjs.
    def config(self, setting=None):
        if not self.is_root:
            Warning("you are not root")
            return
        result = []
        dataNodes = []
        shapes = []
        # before handle edge, shape must be handled well
        for x in self.find_by_class("Shape"):
            g = x.get_child("Graphics")
            shapes.append(g)
            # print x
            # print g
            s = Shape(g.props["ShapeType"], x, g)
            if s.generate():
                for sg in s.generate():
                    result.append(sg)
        # Handle DataNode first:
        for x in [x.get_child("Graphics") for x in self.find_by_class("DataNode")]:
            # print x
            # print x.father
            parent = None
            parent = None
            for s in shapes:
                if contain([int(float(s.props["CenterX"])),
                            int(float(s.props["CenterY"])),
                            int(float(s.props["Width"])),
                            int(float(s.props["Height"]))], s.props["ZOrder"],
                           [int(float(x.props["CenterX"])), int(float(x.props["CenterY"]))],
                           x.props["ZOrder"]):
                    parent = s
            dataNodes.append(x)
            setting = {
                "nodes": {
                    "data": {
                        "id": x.father.props["GraphId"]
                    },
                    "position": {
                        "x": int(float(x.props["CenterX"])),
                        "y": int(float(x.props["CenterY"])),
                    },
                    "group": "nodes"
                },
                "style": {
                    "selector": "#{}".format(x.father.props["GraphId"]),
                    "style": {
                        "shape": "rectangle",
                        "width": int(float(x.props["Width"])),
                        "height": int(float(x.props["Height"])),
                        "label": x.father.props["TextLabel"],
                        # the align of a label:
                        "text-halign": "center",
                        "text-valign": "center",
                        "background-color": "#fff",
                        "border-width": "1px",
                        # "border-style": "dotted",
                        "border-color": "#000",
                        "font-size": int(float(x.props["FontSize"])),
                        "z-index": 100000 - int(x.props.get("ZOrder"))
                    },
                }
            }
            # if parent:
            #     setting["nodes"]["data"]["parent"] = parent.father.props.get("GraphId")
            result.append(setting)
        # Next is Label:
        for x in self.find_by_class("Label"):
            g = x.get_child("Graphics")
            parent = None
            for s in shapes:
                if contain([int(float(s.props["CenterX"])),
                            int(float(s.props["CenterY"])),
                            int(float(s.props["Width"])),
                            int(float(s.props["Height"]))], s.props["ZOrder"],
                           [int(float(g.props["CenterX"])), int(float(g.props["CenterY"]))],
                           g.props["ZOrder"]):
                    parent = s
            setting = {
                "nodes": {
                        "data": {
                            "id": x.props["GraphId"],
                        },
                        "position": {
                            "x": int(float(g.props["CenterX"])),# - int(float(g.props["Width"])) / 2,
                            "y": int(float(g.props["CenterY"])),# - int(float(g.props["Height"])) / 2
                        },
                        "group": "nodes",
                    },
                "style": {
                    "selector": "#{}".format(x.props["GraphId"]),
                    "style": {
                        "shape": "rectangle",
                        "width": int(float(g.props["Width"])),
                        "height": int(float(g.props["Height"])),
                        "label": x.props["TextLabel"],
                        # the align of a label:
                        "text-halign": "center",
                        "text-valign": "center",
                        "background-opacity": 0,
                        "text-max-width": int(float(g.props["Width"])),
                        "text-wrap": "wrap",
                        "color": "#f00",
                        "font-size": int(float(g.props["FontSize"])),
                        "z-index": 100000 - int(g.props.get("ZOrder"))
                    }
                }
            }
            # if parent:
            #     setting["nodes"]["data"]["parent"] = parent.father.props.get("GraphId")
            result.append(setting)
        # Next handle State, this should find the ref
        for x in self.find_by_class("State"):
            g = x.get_child("Graphics")
            rg = None
            for dn in dataNodes:
                if dn.father.props["GraphId"] == x.props["GraphRef"]:
                    rg = dn
            if not rg:
                raise GPMLCorrespondeNodeNotFound("cant find the related node to a state")
            result.append({
                "nodes": {
                    "data": {
                        "id": x.props["GraphId"],
                    },
                    "position": {
                        "x": int(float(g.props["RelX"])) + int(int(float(rg.props["Width"])) / 2) + int(float(rg.props["CenterX"])),
                        "y": int(float(g.props["RelY"])) + int(int(float(rg.props["Height"])) / 2) + int(float(rg.props["CenterY"]))
                    },
                    "group": "nodes",
                },
                "style": {
                    "selector": "#{}".format(x.props["GraphId"]),
                    "style": {
                        "shape": "ellipse",
                        "width": int(float(g.props["Width"])),
                        "height": int(float(g.props["Height"])),
                        "label": x.props["TextLabel"],
                        # the align of a label:
                        "text-halign": "center",
                        "text-valign": "center",
                        "text-max-width": int(float(g.props["Width"])),
                        "text-wrap": "wrap",
                        "background-color": "#{}".format(g.props.get("FillColor") or "fff"),
                        "font-size": int(float(rg.props["FontSize"])),
                        "border-width": "1px",
                        # "border-style": "dotted",
                        "border-color": "#000",
                        "z-index": 100000 - int(rg.props.get("ZOrder"))
                    }
                }
            })
        # Now add the edge:
        count = 0
        # For edge, we have to create some of Invisible temp node
        for x in self.find_by_class("Point"):
            # print x.father
            if not x.props.get("GraphRef") or True:
                parent = None
                for s in shapes:
                    if contain([int(float(s.props["CenterX"])),
                                int(float(s.props["CenterY"])),
                                int(float(s.props["Width"])),
                                int(float(s.props["Height"]))], s.props["ZOrder"],
                               [int(float(x.props["X"])), int(float(x.props["Y"]))],
                               x.father.props["ZOrder"]):
                        parent = s
                # print "parent is {}".format(parent)
                # we need to create temp node for them
                node_id = "t{}{}".format(int(float(x.props["X"])), int(float(x.props["Y"])))
                x.props["GraphRef"] = node_id
                settings = {
                    "nodes": {
                        "data": {
                            "id": node_id,
                        },
                        "position": {
                            "x": int(float(x.props["X"])),
                            "y": int(float(x.props["Y"])),
                        "group": "nodes",
                        }
                    },
                    "style": {
                        "selector": "#{}".format(node_id),
                        "style": {
                            "shape": "ellipse",
                            "width": 2,
                            "height": 2,
                            "background-color": "#{}".format("f00"),
                            "z-index": 100000 - int(x.father.props.get("ZOrder"))
                        }
                    }
                }
                # if parent:
                #     settings["nodes"]["data"]["parent"] = parent.father.props["GraphId"]
                result.append(settings)
        for x in self.find_by_class("Interaction"):
            g = x.get_child("Graphics")
            p1, p2 = g.find_by_class("Point")[0], g.find_by_class("Point")[1]
            # draw the arraw
            if not g.props.get("LineStyle"):
                linestyle = "solid"
            elif g.props.get("LineStyle"):
                linestyle = "dashed"
            result.append({
                "nodes": {
                    "data": {
                        "id": "{}-{}".format(p1.props["GraphRef"], p2.props["GraphRef"]),
                        "source": p1.props["GraphRef"],
                        "target": p2.props["GraphRef"]
                    },
                    "group": "edges",
                },
                "style": {
                    "selector": "#{}".format("{}-{}".format(p1.props["GraphRef"], p2.props["GraphRef"])),
                    "style": {
                        "line-color": "#{}".format(g.props.get("Color") or "000"),
                        "line-width": g.props.get("LineThickness"),
                        "line-style": linestyle,
                        'target-arrow-color': "#{}".format(g.props.get("Color") or "000"),
                        'target-arrow-shape': 'triangle',
                        'target-arrow-fill': "filled",
                        'curve-style': 'bezier',
                        'arrow-size': 2,
                        "z-index": 100000 - int(g.props.get("ZOrder"))
                    }
                }
            })
            count += 1
        return result

    def draw_old(self, setting=None):
        config = self.config()
        if env():
            from IPython.display import HTML
            with open(os.path.dirname(os.path.abspath(__file__)) + "/../../static/box.html") as fp:
                con = fp.read()
            try:
                shutil.rmtree(os.getcwd() + "/static")
            except:
                import traceback
                print(traceback.format_exc())
                pass
            if not self.option:
                self.option = []
            with open(os.path.dirname(os.path.abspath(__file__))
                                + "/../../static/KGMLandGPML/gpml_data/config.json", "w") as fp:
                fp.write(json.dumps({"pathway": config, "option": self.option}))
            shutil.copytree(os.path.dirname(os.path.abspath(__file__)) + "/../../static", os.getcwd() + "/static")
            # the kegg view
            ratio = "0.7"
            con = con.replace("{{path}}", "'static/KGMLandGPML/gpml.html'").replace("{{ratio}}", ratio)
            return HTML(con)

    def draw(self, setting=None):
        if env():
            from IPython.display import HTML
            with open(os.path.dirname(os.path.abspath(__file__)) + "/../../static/box.html") as fp:
                con = fp.read()
            try:
                shutil.rmtree(os.getcwd() + "/GPML")
            except:
                # import traceback
                # print traceback.format_exc()
                pass
            if not self.option:
                self.option = []
            # with open(os.path.dirname(os.path.abspath(__file__))
            #                     + "/../../static/GPML/gpml_data/config.json", "w") as fp:
            #     fp.write(json.dumps({"option": self.option.json
            #     if isinstance(self.option, IntegrationOptions) else self.option}))
            # data = self.export()
            # with open(os.path.dirname(os.path.abspath(__file__))
            #                     + "/../../static/GPML/gpml_data/pathway.xml", "w") as fp:
            #     fp.write(data)
            shutil.copytree(os.path.dirname(os.path.abspath(__file__)) + "/../../static/GPML/", os.getcwd() + "/GPML")
            with open(os.getcwd() + "/GPML/gpml_data/config.json", "w") as fp:
                fp.write(json.dumps({"option": self.option.json
                if isinstance(self.option, IntegrationOptions) else self.option}))
            data = self.export()
            with open(os.getcwd() + "/GPML/gpml_data/pathway.xml", "w") as fp:
                fp.write(data)
            # the kegg view
            ratio = "0.7"
            con = con.replace("{{path}}", "'GPML/gpml.html'").replace("{{ratio}}", ratio)
            return HTML(con)

    def export(self, format=None):
        '''
        Export the GPML file.
        :param format: raise warning, if not input a GPML
        :return:
        '''
        doc = Document()
        root = doc.createElement(self._class)
        for k, v in self.props.items():
            root.setAttribute(k, v)
        for x in self.children:
            x._xml_object(root, doc)
        doc.appendChild(root)
        return doc.toprettyxml(indent='  ')

    def _xml_object(self, father, doc):
        me = doc.createElement(self._class)
        for k, v in self.props.items():
            if k == "ref" or k == "_father" or k == "_is_root" or k == "_children" or k == "core_implement":
                continue
            if not v:
                continue
            if k == "_class":
                k = "class"
            me.setAttribute(k, str(v))
        father.appendChild(me)
        children = self.children
        for x in children:
            x._xml_object(me, doc)

    def integrate(self, id_lists, visualize_option_lists):
        self.option = IntegrationOptions()
        self.option.set(id_lists, visualize_option_lists)

    def _flatten(self, list):
        list.append(self)
        for x in self.children:
            x._flatten(list)

    def flatten(self):
        result = []
        self._flatten(result)
        return result

    # the property should impl
    @property
    def root(self):
        raise NotImplementedError

    @property
    def is_root(self):
        return self._is_root

    @property
    def father(self):
        return self._father

    @property
    def children(self):
        return self._children

    @property
    def members(self):
        return self.flatten()

    @property
    def nodes(self):
        return [x for x in self.members if x._class == "DataNode"]

    @property
    def entities(self):
        return self.nodes

    @property
    def reactions(self):
        return [x for x in self.members if x._class == "Interaction"]

    @property
    def graphics(self):
        return [x for x in self.flatten() if x._class == "Graphics"]

    def add_child(self, child):
        self._children.append(child)

    def set_father(self, father):
        self._father = father

    def xrefs(self):
        return [x for x in self.children if x._class == "Xref"]

    @property
    def external_id(self):
        res = {}
        for x in self.xrefs():
            if x.props.get("Database") and x.props.get("ID"):
                res[x.props.get("Database")] = x.props.get("ID")
        return res

    def summary(self, depth=0):
        self_str = "\t" * depth + "{}: {}, value: {}\n".format(self._class,
                                   ", ".join(["{}: {}".format(k, v) for k, v in self.props.items()]),
                                                               self.value)
        for x in self._children:
            self_str += x.summary(depth=depth+1)
        return self_str

    def __repr__(self):
        return "class: {}, props: [{}], value: {}, database ID: {}\n".format(self._class,
                                             ",".join(["{}: {} ".format(k, v) for k, v in self.props.items()]),
                                                        self.value.encode("utf8") if self.value else None,
                                                                           self.external_id)

    def _find_by_class(self, _class, result):
        if self._class == _class:
            result.append(self)
        for x in self._children:
            x._find_by_class(_class, result)

    def find_by_class(self, _class):
        # if not self.is_root:
        #     return None
        result = []
        self._find_by_class(_class, result)
        return result

    def get_child(self, _class):
        for x in self._children:
            if x._class == _class:
                return x
        else:
            return None

    @staticmethod
    def parse(data):
        hander = GPMLHandler()
        parseString(data.encode("utf8"), hander)
        return hander.root


class Heap(list):
    def __init__(self):
        list.__init__([])

    def push(self, element):
        self.insert(0, element)

    def peak(self):
        return self[0]


class GPMLHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.gap = 0
        self.root = None
        self.heap = Heap()
        self.current_content = ""

    def startElement(self, name, attrs):
        # print "\t" * self.gap + "{}: {}".format(name, ",".join(["{}:{}".format(k, v) for k, v in attrs.items()]))
        if name == "Pathway":
            self.root = GPMLParser(name, dict(attrs), True)
            self.heap.push(self.root)
        else:
            node = GPMLParser(name, dict(attrs), False)
            father = self.heap.peak()
            father.add_child(node)
            node.set_father(father)
            self.heap.push(node)

    def endElement(self, name):
        self.gap -= 1
        self.heap.pop(0)

    def characters(self, content):
        if content.strip():
            self.heap.peak().value = content.strip()

# if __name__ == '__main__':
#     file_path = "/Users/sheep/Downloads/WP2593_86961.gpml"
#     with open(file_path) as fp:
#         con = fp.read()
#     tree = GPMLParser.parse(con)
#     print tree.config()
