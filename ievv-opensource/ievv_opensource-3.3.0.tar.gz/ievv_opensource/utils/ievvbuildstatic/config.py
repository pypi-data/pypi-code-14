import logging
import os
import shutil
import time
from collections import OrderedDict

from django.apps import apps

from ievv_opensource.utils.ievvbuildstatic import filepath
from ievv_opensource.utils.ievvbuildstatic.watcher import WatchConfigPool
from ievv_opensource.utils.logmixin import LogMixin


class App(LogMixin):
    """
    Configures how ``ievv buildstatic`` should build the static files for a Django app.
    """
    def __init__(self, appname, version, plugins,
                 sourcefolder='staticsources',
                 destinationfolder='static',
                 keep_temporary_files=False):
        """
        Parameters:
            appname: Django app label (I.E.: ``myproject.myapp``).
            plugins: Zero or more :class:`ievv_opensource.utils.ievvbuild.pluginbase.Plugin`
                objects.
            sourcefolder: The folder relative to the app root folder where
                static sources (I.E.: less, coffescript, ... sources) are located.
                Defaults to ``staticsources``.
        """
        self.apps = None
        self.version = version
        self.appname = appname
        self.sourcefolder = sourcefolder
        self.destinationfolder = destinationfolder
        self.installers = {}
        self.plugins = []
        self.keep_temporary_files = keep_temporary_files
        for plugin in plugins:
            self.add_plugin(plugin)

    def add_plugin(self, plugin):
        """
        Add a :class:`ievv_opensource.utils.ievvbuildstatic.lessbuild.Plugin`.
        """
        plugin.app = self
        self.plugins.append(plugin)

    def run(self):
        """
        Run :meth:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.run`
        for all plugins within the app.
        """
        for plugin in self.plugins:
            plugin.runwrapper()

    def install(self):
        """
        Run :meth:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.install`
        for all plugins within the app.
        """
        for plugin in self.plugins:
            plugin.install()
        for installer in self.installers.values():
            installer.install()
        for plugin in self.plugins:
            plugin.post_install()

    def get_app_config(self):
        """
        Get the AppConfig for the Django app.
        """
        if not hasattr(self, '_app_config'):
            self._app_config = apps.get_app_config(self.appname)
        return self._app_config

    def get_appfolder(self):
        """
        Get the absolute path to the Django app root folder.
        """
        return self.get_app_config().path

    def get_app_path(self, apprelative_path):
        """
        Returns the path to the directory joined with the
        given ``apprelative_path``.
        """
        return os.path.join(self.get_appfolder(), apprelative_path)

    def _relative_or_absolute_path_to_absolute_path(self, relative_path_root, pathlist):
        if len(pathlist) == 1 and isinstance(pathlist[0], filepath.FilePathInterface):
            return pathlist[0].abspath
        else:
            if pathlist:
                return os.path.join(relative_path_root, *pathlist)
            else:
                return relative_path_root

    def get_source_path(self, *path):
        """
        Returns the absolute path to a folder within the source
        folder of this app or another app.

        Examples:

            Get the source path for a coffeescript file::

                self.get_source_path('mylib', 'app.coffee')

            Getting the path of a source file within another app using
            a :class:`ievv_opensource.utils.ievvbuildstatic.filepath.SourcePath`
            object (a subclass of :class:`ievv_opensource.utils.ievvbuildstatic.filepath.FilePathInterface`)
            as the path::

                self.get_source_path(
                    ievvbuildstatic.filepath.SourcePath('myotherapp', 'scripts', 'typescript', 'app.ts'))


        Args:
            *path: Zero or more strings to specify a path relative to the source folder of this app -
                same format as :func:`os.path.join`.
                A single :class:`ievv_opensource.utils.ievvbuildstatic.filepath.FilePathInterface`
                object to specify an absolute path.
        """
        sourcefolder = os.path.join(self.get_app_path(self.sourcefolder), self.appname)
        return self._relative_or_absolute_path_to_absolute_path(relative_path_root=sourcefolder,
                                                                pathlist=path)

    def get_destination_path(self, *path, **kwargs):
        """
        Returns the absolute path to a folder within the destination
        folder of this app or another app.

        Examples:

            Get the destination path for a coffeescript file - extension
            is changed from ``.coffee`` to ``.js``::

                self.get_destination_path('mylib', 'app.coffee', new_extension='.js')

            Getting the path of a destination file within another app using
            a :class:`ievv_opensource.utils.ievvbuildstatic.filepath.SourcePath`
            object (a subclass of :class:`ievv_opensource.utils.ievvbuildstatic.filepath.FilePathInterface`)
            as the path::

                self.get_destination_path(
                    ievvbuildstatic.filepath.DestinationPath(
                        'myotherapp', '1.1.0', 'scripts', 'typescript', 'app.ts'),
                    new_extension='.js')

        Args:
            path: Path relative to the source folder.
                Same format as ``os.path.join()``.
                A single :class:`ievv_opensource.utils.ievvbuildstatic.filepath.FilePathInterface`
                object to specify an absolute path.
            new_extension: A new extension to give the destination path.
                See example below.

        """
        new_extension = kwargs.get('new_extension', None)
        destinationfolder = os.path.join(
            self.get_app_path(self.destinationfolder), self.appname, self.version)
        absolute_path = self._relative_or_absolute_path_to_absolute_path(relative_path_root=destinationfolder,
                                                                         pathlist=path)
        if new_extension is not None:
            path, extension = os.path.splitext(absolute_path)
            absolute_path = '{}{}'.format(path, new_extension)
        return absolute_path

    def watch(self):
        """
        Start a watcher thread for each plugin.
        """
        watchconfigs = []
        for plugin in self.plugins:
            watchconfig = plugin.watch()
            if watchconfig:
                watchconfigs.append(watchconfig)
        return watchconfigs

    def iterinstallers(self):
        return self.installers.values()

    def get_installer(self, installerclass):
        """
        Get an instance of the given ``installerclass``.

        Parameters:
            installerclass: A subclass of
                :class:`ievv_opensource.utils.ievvbuildstatic.installers.base.AbstractInstaller`.
        """
        if installerclass.name not in self.installers:
            installer = installerclass(app=self)
            self.installers[installerclass.name] = installer
        return self.installers[installerclass.name]

    def get_logger_name(self):
        return '{}.{}'.format(self.apps.get_logger_name(), self.appname)

    def get_temporary_build_directory_path(self, *path):
        return self.get_source_path('ievvbuildstatic_temporary_build_directory', *path)

    def make_temporary_build_directory(self, name):
        """
        Make a temporary directory that you can use for building something.

        Returns:
            str: The absolute path of the new directory.
        """
        self._delete_temporary_build_directory(name)
        temporary_directory_path = self.get_temporary_build_directory_path(name)
        os.makedirs(temporary_directory_path)
        return temporary_directory_path

    def _delete_temporary_build_directory(self, name):
        """
        Delete a temporary directory created with :meth:`.make_temporary_build_directory`.
        """
        temporary_directory_path = self.get_temporary_build_directory_path(name)
        if os.path.exists(temporary_directory_path):
            shutil.rmtree(temporary_directory_path)
        base_temporary_directory = self.get_temporary_build_directory_path()
        if os.path.exists(base_temporary_directory) and len(os.listdir(base_temporary_directory)) == 0:
            shutil.rmtree(base_temporary_directory)


class Apps(LogMixin):
    """
    Basically a list around :class:`.App` objects.
    """
    def __init__(self, *apps, help_header=None):
        """
        Parameters:
            apps: :class:`.App` objects to add initially. Uses :meth:`.add_app` to add the apps.
        """
        self.apps = OrderedDict()
        self.help_header = help_header
        for app in apps:
            self.add_app(app)

    def add_app(self, app):
        """
        Add an :class:`.App`.
        """
        app.apps = self
        self.apps[app.appname] = app

    def get_app(self, appname):
        """
        Get app by appname.
        """
        return self.apps[appname]

    def install(self):
        """
        Run :meth:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.install`
        for all plugins within all :class:`apps <.App>`.
        """
        for app in self.apps.values():
            app.install()

    def log_help_header(self):
        if self.help_header:
            self.get_logger().infobox(self.help_header)

    def iterapps(self):
        """
        Get an interator over the apps.
        """
        return self.apps.values()

    def run(self):
        """
        Run :meth:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin.run`
        for all plugins within all :class:`apps <.App>`.
        """
        for app in self.iterapps():
            app.run()

    def watch(self):
        """
        Start watcher threads for all folders that at least one
        :class:`plugin <ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin>`
        within any of the :class:`apps <.App>` has configured to be watched for changes.

        Blocks until ``CTRL-c`` is pressed.
        """
        watchconfigpool = WatchConfigPool()
        for app in self.apps.values():
            watchconfigpool.extend(app.watch())
        all_observers = watchconfigpool.watch()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for observer in all_observers:
                observer.stop()

        for observer in all_observers:
            observer.join()

    def get_logger_name(self):
        return 'ievvbuildstatic'

    def __configure_shlogger(self, loglevel, handler):
        shlogger = logging.getLogger('sh.command')
        shlogger.setLevel(loglevel)
        shlogger.addHandler(handler)
        shlogger.propagate = False

    # def __configure_ievvbuild_logger(self, loglevel, handler):
    #     logger = self.get_logger()
    #     logger.setLevel(loglevel)
    #     logger.addHandler(handler)
    #     logger.propagate = False

    def configure_logging(self, loglevel=logging.INFO,
                          shlibrary_loglevel=logging.WARNING):
        # formatter = logging.Formatter('[%(name)s:%(levelname)s] %(message)s')
        handler = logging.StreamHandler()
        # handler.setFormatter(formatter)
        # handler.setLevel(loglevel)
        # self.__configure_ievvbuild_logger(loglevel=loglevel,
        #                                   handler=handler)
        self.__configure_shlogger(loglevel=shlibrary_loglevel,
                                  handler=handler)
