import csv

COMMENT_SYMBOL = "#"
KEY_VALUE_DELIMITER = "="

def extract_key_value_pair(line):
    """ Breaks a line into a key-value pair
        @param line - A string representation of a key value pair
        @return a tuple containing the key and the value
    """
    if not line.startswith(COMMENT_SYMBOL): # Ignore comments
        try:
            delimiter_position = line.index(KEY_VALUE_DELIMITER)
            key = line[:delimiter_position]
            value = line[delimiter_position + 1:].strip()
            return (key, value)
        except:
            pass

def extract_key_value_pairs(lines):
    """ Load all of the keys and values from lines into a dictionary
        @param lines - A list of strings containing key value pairs
        @return a dicitionary relating keys to values
    """
    data = dict()
    for line in lines:
        try:
            pair = extract_key_value_pair(line)
            data[pair[0]] = pair[1]
        except:
            pass
    return data

class ConfigurationReader(object):
    def reader(filename):
        if filename.endswith('.csv'): return CSVReader(filename)
        if filename.endswith('.properties'): return PropertiesReader(filename)
    reader = staticmethod(reader)

class PropertiesReader(ConfigurationReader):
    def __init__(self, filename):
        self.filename = filename
    def read(self):
        config = dict()
        with open(self.filename, 'r') as f:
            config = extract_key_value_pairs(f.readlines())
            return config

class CSVReader(ConfigurationReader):
    def __init__(self, filename):
        self.filename = filename
    def read(self):
        config = dict()
        with open(self.filename, 'r', newline='') as f:
            for row in csv.reader(f):
                config[row[0]] = row[1]
        return config
