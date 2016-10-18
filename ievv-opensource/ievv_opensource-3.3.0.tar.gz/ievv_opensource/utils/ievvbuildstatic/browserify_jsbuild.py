import os

from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from ievv_opensource.utils.shellcommandmixin import ShellCommandError
from ievv_opensource.utils.shellcommandmixin import ShellCommandMixin


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    """
    Browserify javascript bundler plugin.

    Examples:

        Simple example::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.browserify_jsbuild.Plugin(
                            sourcefile='app.js',
                            destinationfile='app.js',
                        ),
                    ]
                )
            )

        Custom source folder example::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.browserify_jsbuild.Plugin(
                            sourcefolder=os.path.join('scripts', 'javascript', 'api'),
                            sourcefile='api.js',
                            destinationfile='api.js',
                        ),
                    ]
                )
            )
    """
    name = 'browserify_jsbuild'

    def __init__(self, sourcefile, destinationfile,
                 sourcefolder=os.path.join('scripts', 'javascript'),
                 destinationfolder=os.path.join('scripts'),
                 extra_watchfolders=None,
                 sourcemap=False):
        """
        Parameters:
            sourcefile: The source file relative to ``sourcefolder``.
            destinationfile: Path to destination file relative to ``destinationfolder``.
            sourcefolder: The folder where ``sourcefiles`` is located relative to
                the source folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.
                Defaults to ``scripts/javascript``.
            destinationfolder: The folder where ``destinationfile`` is located relative to
                the destination folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.
                Defaults to ``scripts/``.
            extra_watchfolders: List of extra folders to watch for changes.
                Relative to the source folder of the
                :class:`~ievv_opensource.utils.ievvbuild.config.App`.
        """
        super(Plugin, self).__init__()
        self.sourcefile = sourcefile
        self.destinationfile = destinationfile
        self.destinationfolder = destinationfolder
        self.sourcefolder = sourcefolder
        self.extra_watchfolders = extra_watchfolders or []
        self.sourcemap = sourcemap

    def get_sourcefile_path(self):
        return self.app.get_source_path(self.sourcefolder, self.sourcefile)

    def get_destinationfile_path(self):
        return self.app.get_destination_path(self.destinationfolder, self.destinationfile)

    def install(self):
        """
        Installs the ``browserify`` NPM package.

        The package is installed with no version specified, so you
        probably want to freeze the version using the
        :class:`ievv_opensource.utils.ievvbuildstatic.npminstall.Plugin` plugin.
        """
        self.app.get_installer(NpmInstaller).queue_install(
            'browserify')

    def get_browserify_executable(self):
        return self.app.get_installer(NpmInstaller).find_executable('browserify')

    def get_browserify_extra_args(self):
        """
        Get extra browserify args.

        Override this in subclasses to add transforms and such.
        """
        return []

    def make_browserify_args(self):
        """
        Make browserify args list.

        Adds the following in the listed order:

        - ``-d`` if the ``sourcemap`` kwarg is ``True``.
        - the source file.
        - ``-d <destination file path>``.
        - whatever :meth:`.get_browserify_extra_args` returns.

        Should normally not be extended. Extend :meth:`.get_browserify_extra_args`
        instead.
        """
        args = []
        if self.sourcemap:
            args.append('-d')
        args.extend([
           self.get_sourcefile_path(),
           '-o', self.get_destinationfile_path(),
        ])
        args.extend(self.get_browserify_extra_args())
        return args

    def run(self):
        self.get_logger().command_start(
            'Running browserify with {sourcefile} as input and {destinationfile} as output'.format(
                sourcefile=self.get_sourcefile_path(),
                destinationfile=self.get_destinationfile_path()))
        executable = self.get_browserify_executable()
        destination_folder = self.app.get_destination_path(self.destinationfolder)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        try:
            self.run_shell_command(executable, args=self.make_browserify_args(),
                                   _cwd=self.app.get_source_path())
        except ShellCommandError:
            self.get_logger().command_error('browserify build FAILED!')
        else:
            self.get_logger().command_success('browserify build succeeded :)')

    def get_extra_watchfolder_paths(self):
        return map(self.app.get_source_path, self.extra_watchfolders)

    def get_watch_folders(self):
        """
        We only watch the folder where the javascript is located,
        so this returns the absolute path of the ``sourcefolder``.
        """
        folders = [self.app.get_source_path(self.sourcefolder)]
        if self.extra_watchfolders:
            folders.extend(self.get_extra_watchfolder_paths())
        return folders

    def get_watch_extensions(self):
        """
        Returns a list of the extensions to watch for in watch mode.

        Defaults to ``['js']``.

        Unless you have complex needs, it is probably easier to override
        this than overriding
        :meth:`~ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.get_watch_regexes`.
        """
        return ['js']

    def get_watch_regexes(self):
        return ['^.+[.]({extensions})'.format(
            extensions='|'.join(self.get_watch_extensions()))]

    def __str__(self):
        return '{}({})'.format(super(Plugin, self).__str__(), self.sourcefolder)
