import os
import json


class ConfigKeyError(Exception):
    pass


class Config(object):
    required_fields = ('PROJECT_ID', 'DESTINATION_DIR', 'LIVE', )

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
        if not os.path.exists(self.DESTINATION_DIR):
            os.makedirs(self.DESTINATION_DIR)