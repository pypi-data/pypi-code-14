import os, glob
from .build_context import BuildContext


class Config:
    def __init__(self, root, project):
        self.project = project
        assert(root.tag == "config")
        self.name = root.attrib["name"]
        self.inherits = root.attrib["inherits"] if "inherits" in root.attrib else None
        self.platform = root.attrib["platform"] if "platform" in root.attrib else None
        self.sources = []
        self.params = {}
        self.uses = []
        for child in root:
            if child.tag == "source":
                file_name = child.attrib["file"]
                self.sources += glob.glob(file_name)
            elif child.tag == "param":
                name = child.attrib["name"]
                value = child.attrib["value"]
                if name in self.params:
                    if name.endswith("[]"):
                        self.params[name] += " " + value
                    continue
                self.params[name] = value
            elif child.tag == "use":
                package_name = child.attrib["package"]
                self.uses.append(package_name)

    def build(self, target="build", build_dir = None, simulation=False):
        if build_dir is None:
            build_dir = os.path.join(self.project.base_dir, "build")
        context = BuildContext(build_dir, simulation)
        context.add_config(self)
        context.build(target)
