import os
import pkg_resources
from django.utils.datastructures import SortedDict
from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.contrib.staticfiles.storage import FileSystemStorage
from django.utils.importlib import import_module
from django.utils._os import upath


class FlexiblePathStorage(FileSystemStorage):

    prefix = None

    def __init__(self, app, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        # app is the actual app module

        self.source_dir = kwargs.get("source_dir", "static")
        del kwargs['source_dir']

        mod = import_module(app)
        mod_path = os.path.dirname(upath(mod.__file__))
        location = os.path.join(mod_path, self.source_dir)

        super(FlexiblePathStorage, self).__init__(location, *args, **kwargs)

class PluginFilesFinder(AppDirectoriesFinder):

    def __init__(self, apps=None, *args, **kwargs):

        self.apps = []
        self.storages = SortedDict()

        for entrypoint in pkg_resources.iter_entry_points(group="djinn.app"):

            app = entrypoint.module_name

            if app in self.storages.keys():
                continue

            app_storage = self.storage_class(app)
            self.storages[app] = app_storage

        for entrypoint in pkg_resources.iter_entry_points(group="djinn.app",
                                                          name="statics"):
            path = entrypoint.load()()
            app = entrypoint.module_name

            self.storages[app] = FlexiblePathStorage(app, source_dir=path)

        for app in self.storages.keys():
            if os.path.isdir(self.storages[app].location):

                if app not in self.apps:
                    self.apps.append(app)
