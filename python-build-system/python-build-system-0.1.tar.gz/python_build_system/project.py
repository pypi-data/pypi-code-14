import sys, os, re, shutil, shlex, glob, subprocess
import xml.etree.ElementTree as ET


class Project:
    def __init__(self, **kwargs):
        root = None
        base_dir = os.path.curdir
        if "root" in kwargs:
            root = kwargs["root"]
        elif "file_name" in kwargs:
            file_name = kwargs["file_name"]
            tree = ET.parse(file_name)
            root = tree.getroot()
            base_dir = os.path.dirname(file_name)
        if "base_dir" in kwargs:
            base_dir = kwargs["base_dir"]
        self.base_dir = base_dir
        self.sources = []
        self.params = {}
        self.configs = {}
        self.uses = []
        if root is not None:
            assert(root.tag == "project")
            self.name = root.attrib["name"]
            for child in root:
                if child.tag == "source":
                    file_name = os.path.join(base_dir, child.attrib["file"])
                    self.sources += glob.glob(file_name)
                elif child.tag == "param":
                    name = child.attrib["name"]
                    value = child.attrib["value"]
                    if name in self.params:
                        if name.endswith("[]"):
                            self.params[name] += " " + value
                    self.params[name] = value
                    continue
                elif child.tag == "config":
                    config = Config(child, self)
                    self.configs[config.name] = config
                elif child.tag == "use":
                    package_name = child.attrib["package"]
                    self.uses.append(package_name)

    def load_to_context(self, ctx, config):
        if config:
            if config not in self.configs:
                raise Exception("Configuration \"%s\" not found")
            ctx.add_config(self.configs[config])
        else:
            ctx.add_project(self)


from .config import Config
