class Config(object):

    config = {}

    def get(self, attr, default=None):
        try:
            return self.config[attr]
        except KeyError:
            return default

    def set(self, attr, value):
        self.config[attr] = value
        return value

    def __str__(self):
        return self.__str_config(self.config)

    def __str_config(self, config, indent=""):
        string = ""

        if type(config) is dict:
            for key, value in config.items():
                string += "\n%s%s: %s" % (indent, key, self.__str_config(value, indent=indent + "  "))
        else:
            string += str(config)

        return string


config = Config()
