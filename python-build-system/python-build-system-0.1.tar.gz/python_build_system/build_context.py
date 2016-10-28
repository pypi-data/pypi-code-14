import sys, os,  re, subprocess, shlex, shutil
if sys.version_info >= (3, 5):
    import importlib.util
else:
    import imp
from .project import Project


class BuildContext:
    def __init__(self, build_dir, simulation=False):
        self.build_dir = build_dir
        self.simulation = simulation
        self.sources = []
        self.params = {}
        self.loaded_packages = {}
        self.added_packages = []
        self.configs = {}
        self.rules = []
        self.targets = {}
        self.prebuild_steps = []
        self.project_dir = None

    def add_project(self, project):
        self.add_param("PROJECT_NAME", project.name)
        if self.project_dir is None:
            self.project_dir = project.base_dir
        self.add_sources(project.sources)
        for param_name in project.params:
            self.add_param(param_name, project.params[param_name])
        for use in project.uses:
            self.add_package(use)
        for config_name in project.configs:
            self.configs[config_name] = project.configs[config_name]

    def add_source(self, source):
        self.sources.append(source)

    def add_sources(self, sources):
        self.sources += sources

    def add_config(self, config):
        self.add_param("CONFIG_NAME", config.name)
        for param_name in config.params:
            self.add_param(param_name, config.params[param_name])
        self.add_project(config.project)
        self.sources += config.sources
        if config.inherits:
            self.add_config(self.configs[config.inherits])
        if config.platform:
            self.add_package("platform/" + config.platform)
        for use in config.uses:
            self.add_package(use)

    def add_param(self, name, value):
        if name in self.params:
            if name.endswith("[]"):
                self.params[name] += " " + value
            return
        self.params[name] = value

    def add_rule(self, pattern, handler, prepend = False):
        rule = BuildRule(pattern, handler)
        if prepend:
            self.rules.insert(0, rule)
        else:
            self.rules.append(rule)

    def load_package(self, name):
        if name in self.loaded_packages:
            return self.loaded_packages[name]
        basename = os.path.basename(name)
        paths = []
        if self.project_dir:
            paths.append(os.path.join(self.project_dir, "modules"))
        if "PYTHON_BUILD_SYSTEM_MODULES_PATH" in os.environ:
            paths += os.environ["PYTHON_BUILD_SYSTEM_MODULES_PATH"].split(os.pathsep)
        paths.append(os.path.join(os.path.expanduser("~"), "PythonBuildSystem", "modules"))
        paths.append(os.path.join(os.path.dirname(__file__), "modules"))
        file_name = None
        for path in paths:
            file_name = "%s/%s.py" % (path, name)
            if os.path.isfile(file_name):
                break
            file_name = "%s/%s.xml" % (path, name)
            if os.path.isfile(file_name):
                break
            file_name = "%s/%s/%s.py" % (path, name, basename)
            if os.path.isfile(file_name):
                break
            file_name = "%s/%s/%s.xml" % (path, name, basename)
            if os.path.isfile(file_name):
                break
            file_name = None
        if file_name is None:
            raise Exception("Package \"%s\" not found in %s" % (name, paths))
        if file_name.endswith(".py"):
            if sys.version_info >= (3, 5):
                spec = importlib.util.spec_from_file_location(name, file_name)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            else:
                module = imp.load_source(name, file_name)
            self.loaded_packages[name] = module
            return module
        else:
            project = Project(file_name=file_name)
            self.loaded_packages[name] = project
            return project

    def add_package(self, name):
        parts = name.split(":", 2)
        name = parts[0]
        config = parts[1] if len(parts) > 1 else None
        if name in self.added_packages:
            return
        module = self.load_package(name)
        self.added_packages.append(name)
        module.load_to_context(self, config)

    def get_param(self, name):
        return self.params[name] if name in self.params else ""

    def remove_param(self, name):
        del self.params[name]

    def add_prebuild_step(self, handler):
        self.prebuild_steps.append(handler)

    def add_target(self, name, handler):
        self.targets[name] = handler

    def build(self, target):
        if target == "clean":
            if self.simulation:
                print("rm -rfv \"%s\"" % self.build_dir)
                return
            try:
                shutil.rmtree(self.build_dir)
            except OSError:
                pass
            return
        if self.simulation:
            print("mkdir -p \"%s\"" % self.build_dir)
        else:
            try:
                os.mkdir(self.build_dir)
            except OSError:
                pass
        for prebuild_step in self.prebuild_steps:
            prebuild_step(self)
        for rule in self.rules:
            rule.process(self, self.sources)
        if target == "build":
            return
        elif target in self.targets:
            self.targets[target](self)
            return
        raise Exception("Target %s not found in project" % target)

    def run_command(self, command, inputs, outputs):
        if self.simulation:
            print(command)
            return
        if not isinstance(inputs, list):
            inputs = [inputs]
        if not isinstance(outputs, list):
            outputs = [outputs]
        max_input_mtime = 0
        for input in inputs:
            try:
                input_mtime = os.path.getmtime(input)
                if input_mtime > max_input_mtime:
                    max_input_mtime = input_mtime
            except OSError:
                pass
        min_output_mtime = 2 ** 63
        for output in outputs:
            try:
                output_mtime = os.path.getmtime(output)
                if output_mtime < min_output_mtime:
                    min_output_mtime = output_mtime
            except OSError:
                min_output_mtime = 0
                break
        if (len(outputs) == 0) or (max_input_mtime >= min_output_mtime):
            print(command)
            args = shlex.split(command)
            retval = subprocess.call(args)
            if retval != 0:
                raise Exception("Build command failed")


class BuildRule:
    def __init__(self, pattern, handler):
        self.pattern = pattern
        self.handler = handler
        self.processed_files = []

    def match_file(self, filename):
        return re.match(self.pattern, filename)

    def match_files(self, filenames):
        matched = []
        for filename in filenames:
            if filename in self.processed_files:
                continue
            if self.match_file(filename):
                matched.append(filename)
        return matched

    def run(self, ctx, arg):
        return self.handler(ctx, arg)

    def process(self, ctx, filenames):
        matched = self.match_files(filenames)
        result = self.run(ctx, matched)
        if isinstance(result, str):
            ctx.add_source(result)
        elif isinstance(result, list):
            ctx.add_sources(result)
        for filename in matched:
            result = self.run(ctx, filename)
            if isinstance(result, str):
                ctx.add_source(result)
            elif isinstance(result, list):
                ctx.add_sources(result)
        self.processed_files += matched
        return len(matched)
