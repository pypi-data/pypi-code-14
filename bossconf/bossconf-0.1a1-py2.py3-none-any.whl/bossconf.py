import yaml
import os

from token_injector import TokenInjector

class BossConf():
    "A very simple class to read config file"

    config = None;

    def __init__(self, config_path, config_file="config.yaml"):
        
        # load file from path
        with open(config_path + "/" + config_file, 'r') as f:
            self.config = yaml.load(f)


    def get(self, nmsp = None, token_mapping = None, only_key = False):
        """ abstract getter """
        data = None
        if nmsp:
            if type(nmsp) is list:
                data = self.config
                if data:
                    i = 0
                    rec_level = len(nmsp)
                    for p_nmsp in nmsp:
                        i = i + 1
                        if p_nmsp in data:
                            if only_key and i == rec_level and type(data[p_nmsp]) is dict:
                                data = data[p_nmsp].keys()
                            else:
                                data = data[p_nmsp]
                        else:
                            data = None
                            break
            else:
                data = self.config[nmsp]
        else:
            data = self.config
        if token_mapping:
            self.token_injector = TokenInjector(token_mapping, '`%s`')
            data = self.get_untokenized_data(data, token_mapping)
        return data

    def get_untokenized_data(self, data, mapping):
        """ untokenize tree data """
        untokenized_data = {}
        for key, value in data.iteritems():
            if type(value) == list:
                val_container = []
                for val in value:
                   val_container.append(self.token_injector(val)) 
                untokenized_data[key] = val_container
            elif type(value) == dict:
                untokenized_data[key] = self.get_untokenized_data(value, mapping)
            else:
                untokenized_data[key] = self.token_injector(value)

        return untokenized_data
