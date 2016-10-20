from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from . import browserify_jsbuild


class Plugin(browserify_jsbuild.Plugin):
    """
    Browserify javascript babel build plugin.

    Examples:

        Simple example::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.browserify_babelbuild.Plugin(
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
                        ievvbuildstatic.browserify_babelbuild.Plugin(
                            sourcefolder=os.path.join('scripts', 'javascript', 'api'),
                            sourcefile='api.js',
                            destinationfile='api.js',
                        ),
                    ]
                )
            )

    """
    name = 'browserify_babelbuild'

    def __init__(self, echmascript_version='es2015', **kwargs):
        """
        Parameters:
            babel_preset: The babel preset to use
            **kwargs: Kwargs for
                :class:`ievv_opensource.utils.ievvbuildstatic.browserify_jsbuild.Plugin`.
        """
        self.echmascript_version = echmascript_version
        super(Plugin, self).__init__(**kwargs)

    def install(self):
        """
        Installs the ``babelify`` and ``babel-preset-<echmascript_version kwarg>``
        NPM packages in addition to the packages installed by
        :meth:`ievv_opensource.utils.ievvbuildstatic.browserify_jsbuild.Plugin.install`.

        The packages are installed with no version specified, so you
        probably want to freeze the versions using the
        :class:`ievv_opensource.utils.ievvbuildstatic.npminstall.Plugin` plugin.
        """
        super(Plugin, self).install()
        self.app.get_installer('npm').queue_install(
            'babelify')
        self.app.get_installer('npm').queue_install(
            'babel-preset-{}'.format('es2015'))

    def get_babelify_presets(self):
        """
        Get a list of babelify presets.

        This is the presets that go into ``<HERE>`` in
        ``babelify -t [ babelify --presets [ <HERE> ] ]``.

        Defaults to ``["<the echmascript_version kwarg>"].
        """
        presets = [self.echmascript_version]
        return presets

    def make_presets_args(self):
        presets = self.get_babelify_presets()
        presets_args = []
        if presets:
            presets_args.extend(['--presets', '['])
            presets_args.extend(presets)
            presets_args.append(']')
        return presets_args

    def get_browserify_extra_args(self):
        return ['-t', '[', 'babelify'] + self.make_presets_args() + [']']
