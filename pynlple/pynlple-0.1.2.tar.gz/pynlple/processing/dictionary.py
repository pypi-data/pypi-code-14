# -*- coding: utf-8 -*-

from pynlple.datasource.filesource import FileDataSource
from pynlple.exceptions import DataSourceException
from pynlple.module import append_paths, list_dir, is_file, strip_extension, abs_path, exists, is_folder


class DictionaryLookUp(object):

    __X = '@endX!'

    def __init__(self, token_mappings, preprocessing_method=None):
        self.dictionary = dict()
        self.preprocess = preprocessing_method
        for tokens, class_ in token_mappings:
            self.__setitem__(tokens, class_)

    def __setitem__(self, tokens, class_):
        if type(tokens) == str:
            tokens = tokens.split()
        DictionaryLookUp.__add_to_dict(self.__prep(tokens), 0, self.dictionary, class_)

    def __getitem__(self, tokens):
        if type(tokens) == str:
            tokens = tokens.split()
        return DictionaryLookUp.__get_from_dict(self.__prep(tokens), 0, self.dictionary)

    @staticmethod
    def __add_to_dict(list_, index, dict_, tag):
        if index < len(list_):
            if list_[index] not in dict_:
                dict_[list_[index]] = dict()
            DictionaryLookUp.__add_to_dict(list_, index + 1, dict_[list_[index]], tag)
        elif index == len(list_):
            dict_.update({DictionaryLookUp.__X: tag})

    @staticmethod
    def __get_from_dict(list_, index, dict_):
        if index < len(list_):
            if list_[index] not in dict_:
                return None
            return DictionaryLookUp.__get_from_dict(list_, index + 1, dict_[list_[index]])
        elif index == len(list_):
            if DictionaryLookUp.__X in dict_:
                return dict_[DictionaryLookUp.__X]
            else:
                return None

    def get_tag(self, tokens):
        if type(tokens) == str or type(tokens) == list:
            tokens = tokens.split()
        return DictionaryLookUp.__get_from_dict(self.__prep(tokens), 0, self.dictionary)

    def __prep(self, tokens):
        if self.preprocess:
            return [self.preprocess(token) for token in tokens]
        else:
            return tokens

    def get_longest_sequence(self):
        return DictionaryLookUp.__find_local_max(self.dictionary, 0, 0)

    @staticmethod
    def __find_local_max(dict_, current, max_):
        if current > max_:
            max_ = current
        for key in dict_.keys():
            if key != DictionaryLookUp.__X:
                max_ = DictionaryLookUp.__find_local_max(dict_[key], current + 1, max_)
        return max_


class FileFolderTokenMapping(object):

    def __init__(self, source_paths=None, data_folder=None, recursive=True, extension='.txt', encoding='utf8'):
        if data_folder:
            self.__data_folder = data_folder
        else:
            self.__data_folder = abs_path(__file__, 'data')
        self.__recursive = recursive
        self.__extension = extension
        self.__encoding = encoding
        self.__file_tag_mappings = set()
        self.__parse_mapping_sources(self.__file_tag_mappings, '', source_paths)

    def __parse_mapping_sources(self, file_tag_mappings, path_prefix, source_paths):
        if not source_paths or len(source_paths) == 0:
            self.__sweep_folder_or_file(file_tag_mappings, path_prefix, '', True)
        elif type(source_paths) is str:
            self.__sweep_folder_or_file(file_tag_mappings, path_prefix, source_paths, True)
        elif type(source_paths) is list or type(source_paths) is set:
            for seed_path in source_paths:
                self.__parse_mapping_sources(file_tag_mappings, path_prefix, seed_path)
        elif type(source_paths) is dict and all(type(key) is str for key in source_paths):
            for prefix, suffix in source_paths.items():
                self.__parse_mapping_sources(file_tag_mappings, append_paths(path_prefix, prefix), suffix)

    def __sweep_folder_or_file(self, file_tag_mappings, path_prefix, folder_or_file_subpath, recursive):
        absolute_file_or_folder_path = append_paths(self.__data_folder, path_prefix, folder_or_file_subpath)
        if not exists(absolute_file_or_folder_path):
            raise DataSourceException('[{0}] File/folder could not be found: {1}'
                                      .format(__name__, absolute_file_or_folder_path))
        if is_file(absolute_file_or_folder_path):
            # Here check if we have extension set. Use it to check file ending if set
            if not self.__extension or absolute_file_or_folder_path.endswith(self.__extension):
                tag = FileFolderTokenMapping.normalize_tag(append_paths(path_prefix, strip_extension(folder_or_file_subpath)))
                file_tag_mappings.add((absolute_file_or_folder_path, tag))
        elif is_folder(absolute_file_or_folder_path):
            if recursive:
                for element_name in list_dir(absolute_file_or_folder_path):
                    new_path_prefix = append_paths(path_prefix, folder_or_file_subpath)
                    self.__sweep_folder_or_file(file_tag_mappings, new_path_prefix, element_name, self.__recursive)

    @staticmethod
    def normalize_tag(tag):
        return tag.replace('\\', '/')

    def get_file_tag_mappings(self):
        return self.__file_tag_mappings

    def __iter__(self):
        for file_path, tag in self.__file_tag_mappings:
            for line in FileDataSource.open_file(file_path, self.__encoding):
                yield line.strip().split(), tag


class DictionaryBasedTagger(object):

    def __init__(self, dictionary_look_up):
        self.lookup = dictionary_look_up
        self.max = self.lookup.get_longest_sequence()

    def get_tagged_entities(self, tokens, all_=False):
        entities = list()
        i = 0
        while i < len(tokens):
            j = i + self.max if i + self.max <= len(tokens) else len(tokens)
            while j > i:
                class_ = self.lookup[tokens[i:j]]
                if class_ is not None:
                    entities.append((i, j, class_))
                    if not all_:
                        i = j - 1
                        break
                j -= 1
            i += 1
        return entities
