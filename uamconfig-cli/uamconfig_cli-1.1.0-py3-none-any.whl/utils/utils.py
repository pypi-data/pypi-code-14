from __future__ import generators
from uamconfig.utils.ConfigReader import *
from uamconfig.utils.ConfigWriter import *

def get_properties(filename):
    config_reader = ConfigurationReader.reader(filename)
    return config_reader.read()

def export_differences(config, filename):
    config_writer = ConfigurationWriter.writer(filename)
    config_writer.write(config)
