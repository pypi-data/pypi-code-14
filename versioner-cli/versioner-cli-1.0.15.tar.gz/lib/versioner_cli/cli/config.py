from future.utils import iteritems
import yaml
import logging

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


class VersionerConfig(object):

    def read_config(self):
        with open(self.path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as msg:
                print(msg)
                logger.error(msg)

    def __unicode__(self):
        string = ''
        for key, value in iteritems(vars(self)):
            string += '{}: {}\n'.format(key, value)
        return string

    def __str__(self):
        string = ''
        for key, value in iteritems(vars(self)):
            string += '{}: {}\n'.format(key, value)
        return string

    def __init__(self, path):
        self.path = path
        for k, v in self.read_config().items():
            setattr(self, k, v)


