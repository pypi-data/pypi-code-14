import json

from ievv_opensource.utils.ievvbuildstatic.installers.base import AbstractInstaller
from ievv_opensource.utils.shellcommandmixin import ShellCommandError


class NpmInstaller(AbstractInstaller):
    """
    NPM installer.
    """
    name = 'npminstall'

    def __init__(self, *args, **kwargs):
        super(NpmInstaller, self).__init__(*args, **kwargs)
        self.queued_packages = {}

    def queue_install(self, package, version=None):
        """
        Installs the given npm package in the build
        directory for the app.

        Does nothing if the package is already installed.
        """
        if not version:
            version = '*'
        self.get_logger().debug('Queued install of {} (version={}) for {}.'.format(
            package, version, self.app.appname))
        queue = True
        if package in self.queued_packages:
            queued_version = self.queued_packages[package]
            if version == '*':
                queue = False
            elif queued_version == '*':
                queue = True
            else:
                self.get_logger().warning(
                    'Multiple explicit versions of the same NPM package {package} '
                    'specified for {appname}: {version!r} and {queued_version!r}. '
                    'Using {version!r}.'.format(
                        package=package,
                        version=version,
                        queued_version=queued_version,
                        appname=self.app.appname))
                queue = True
        if queue:
            self.queued_packages[package] = version

    def get_packagejson_path(self):
        return self.app.get_source_path('package.json')

    def create_packagejson(self):
        packagedata = {
            'name': self.app.appname,
            # We do not care about the version. We are not building a distributable package.
            'version': '0.0.1',
            'devDependencies': self.queued_packages
        }
        open(self.get_packagejson_path(), 'wb').write(
            json.dumps(packagedata, indent=2).encode('utf-8'))

    def install(self):
        self.get_logger().command_start(
            'Running npm install for {}'.format(self.app.get_source_path()))
        self.create_packagejson()
        try:
            self.run_shell_command('npm',
                                   args=['install'],
                                   kwargs={
                                       '_cwd': self.app.get_source_path()
                                   })
        except ShellCommandError:
            self.get_logger().command_error('npm install FAILED!')
            raise SystemExit()
        else:
            self.get_logger().command_success('npm install succeeded :)')

    def find_executable(self, executablename):
        """
        Find an executable named ``executablename``.

        Returns the absolute path to the executable.
        """
        executablepath = self.app.get_source_path(
            'node_modules', '.bin', executablename)
        return executablepath

    def log_shell_command_stderr(self, line):
        if 'npm WARN package.json' in line:
            return
        super(NpmInstaller, self).log_shell_command_stderr(line)
