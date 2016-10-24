import os
import json


class ConfigKeyError(Exception):
    pass


class Config(object):
    required_fields = ('project_id', 'destination_path', )

    def __init__(self, path):
        self.config_path = path
        self.kwargs = self.get_config()
        self.validate()
        for key, value in self.kwargs.iteritems():
            setattr(self, key, value)
        self.create_dirs()

    def get_config(self):
        json_data = open(self.config_path).read()
        return json.loads(json_data)

    def validate(self):
        for field in self.required_fields:
            if not self.kwargs.get(field):
                raise ConfigKeyError("i18nize configuration is missing '{}' required field.".format(field))

    def create_dirs(self):
        if not os.path.exists(self.destination_path):
            os.makedirs(self.destination_path)