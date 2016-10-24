import os
import json


class ConfigKeyError(Exception):
    pass


class Config(object):
    required_fields = ('project_id', 'destination_dir', 'live', )

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.validate()

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.create_dirs()

    def validate(self):
        for field in self.required_fields:
            if self.kwargs.get(field) is None:
                raise ConfigKeyError("i18nize configuration is missing '{}' required field.".format(field))

    def create_dirs(self):
        if not os.path.exists(self.destination_dir):
            os.makedirs(self.destination_dir)