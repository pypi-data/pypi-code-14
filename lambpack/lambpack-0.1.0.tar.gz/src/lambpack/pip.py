import subprocess

class Pip(object):
    """
    Interface to the `pip install` command line.
    """

    def __init__(self, requirements=[], requirement_files=[]):
        self.requirements = list(requirements)
        self.requirement_files = list(requirement_files)

    def add_requirements(self, *requirements):
        """
        Add requirements, e.g `add_requirements("requests", "flask")`
        """

        if not all(isinstance(requirement, basestring) for requirement in requirements):
            raise TypeError("Requirements must be strings, but received {}".format(requirements))
        self.requirements.extend(requirements)

    def add_requirement_files(self, *requirement_files):
        """
        Add requirement files, e.g `add_requirement_files("requirements.txt", "other-requirements.txt")`
        """

        if not all(isinstance(requirement_file, basestring) for requirement_file in requirement_files):
            raise TypeError("Requirement files must be strings, but received {}".format(requirement_files))
        self.requirement_files.extend(requirement_files)

    def install(self, dest):
        """
        Install `requirements` and `requirement_files` into `dest`.
        """

        if not self.requirements and not self.requirement_files:
            return

        command = self.get_command(dest)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise Exception("{!r} returned code {}\n\nstdout:\n{}\n\nstderr: {}".format(
                command,
                proc.returncode,
                stdout.rstrip(),
                stderr.rstrip()
            ))

    def get_command(self, dest):
        args = ["pip", "install", "-t", dest]
        for filename in self.requirement_files:
            args.extend(["-r", filename])
        args.append("--")
        args.extend(self.requirements)
        return args
