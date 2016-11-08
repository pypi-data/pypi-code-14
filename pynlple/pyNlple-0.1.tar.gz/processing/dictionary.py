# -*- coding: utf-8 -*-
import io


class DictionaryLookUp(object):

    __X = '@endX!'

    def __init__(self, token_mapping):
        self.dictionary = dict()
        for tokens, class_ in token_mapping:
            self.__setitem__(tokens, class_)

    def __setitem__(self, tokens, class_):
        if type(tokens) == str:
            tokens = tokens.split()
        DictionaryLookUp.__add_to_dict(tokens, 0, self.dictionary, class_)

    def __getitem__(self, tokens):
        if type(tokens) == str:
            tokens = tokens.split()
        return DictionaryLookUp.__get_from_dict(tokens, 0, self.dictionary)

    @staticmethod
    def __add_to_dict(list, index, dict_, tag):
        if index < len(list):
            if list[index] not in dict_:
                dict_[list[index]] = dict()
            DictionaryLookUp.__add_to_dict(list, index + 1, dict_[list[index]], tag)
        elif index == len(list):
            dict_.update({DictionaryLookUp.__X: tag})

    @staticmethod
    def __get_from_dict(list, index, dict_):
        if index < len(list):
            if list[index] not in dict_:
                return None
            return DictionaryLookUp.__get_from_dict(list, index + 1, dict_[list[index]])
        elif index == len(list):
            if DictionaryLookUp.__X in dict_:
                return dict_[DictionaryLookUp.__X]
            else:
                return None

    def get_tag(self, tokens):
        if type(tokens) == str or type(tokens) == list:
            tokens = tokens.split()
        return DictionaryLookUp.__get_from_dict(tokens, 0, self.dictionary)

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


class FileDictionaryLookUp(DictionaryLookUp):

    def __init__(self, file_path, tag, encoding='utf8'):
        super(FileDictionaryLookUp, self).__init__(FileDictionaryLookUp.iter_file(file_path, tag, encoding))

    @staticmethod
    def iter_file(file_path, tag, encoding):
        with io.open(file_path, 'rt', encoding=encoding) as infile:
            for line in infile:
                yield line.strip().split(), tag


class Tagger(object):

    def __init__(self, dictionary_look_up, preprocessing_method=None):
        self.lookup = dictionary_look_up
        self.preprocessing = preprocessing_method
        self.max = self.lookup.get_longest_sequence()

    def __prep(self, tokens):
        if self.preprocessing:
            return self.preprocessing(tokens)
        else:
            return tokens

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
