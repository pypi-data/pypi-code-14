import csv

COMMENT_SYMBOL = "#"
KEY_VALUE_DELIMITER = "="

class ConfigurationWriter(object):
    def writer(filename):
        if filename.endswith('.csv'): return CSVWriter(filename)
        if filename.endswith('.properties'): return PropertiesWriter(filename)
    writer = staticmethod(writer)

class CSVWriter(ConfigurationWriter):
    def __init__(self, filename):
        self.filename = filename
    def write(self, config):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for k, v in config.items():
                writer.writerow([k,v])

class PropertiesWriter(ConfigurationWriter):
    def __init__(self, filename):
        self.filename = filename
    def write(self, config):
        with open(self.filename, 'w') as f:
            for k, v in config.items():
                f.write(k + KEY_VALUE_DELIMITER + v + '\n')
