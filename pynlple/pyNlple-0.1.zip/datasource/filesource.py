# -*- coding: utf-8 -*-
import codecs
import csv
from os import walk, path

import pandas


class FileDataSource(object):
    """Class for providing json data from json files."""

    @staticmethod
    def open_file(filepath, encoding='utf8'):
        return codecs.open(filepath, 'r', encoding)

    @staticmethod
    def iter_folder_filepaths(folderpath, extension_suffix):
        for root, dirs, files in walk(folderpath):
            for file_ in files:
                if file_.endswith(extension_suffix):
                    yield path.join(root, file_)

    @staticmethod
    def iter_folder_files(folderpath, extension_suffix, encoding='utf8'):
        for filepath in FileDataSource.iter_folder_filepaths(folderpath, extension_suffix):
            yield FileDataSource.open_file(filepath, encoding)

    @staticmethod
    def read_dataframe_from_folder(folderpath, extension_suffix, separator='\t', fill_na_map=None, encoding='utf8'):
        dataframe = pandas.DataFrame()

        for filepath in FileDataSource.iter_folder_filepaths(folderpath, extension_suffix):
            subframe = FileDataSource.read_dataframe(filepath, separator, fill_na_map, encoding)
            dataframe = dataframe.append(subframe)

        return dataframe

    @staticmethod
    def read_dataframe(dataframe_path, separator='\t', fill_na_map=None, encoding='utf8'):
        dataframe = pandas.read_csv(dataframe_path, sep=separator, quoting=csv.QUOTE_NONE, encoding=encoding)
        dataframe.set_index('id', inplace=True)
        if fill_na_map:
            for key, value in fill_na_map.iteritems():
                dataframe[key].fillna(value, inplace=True)
        dataframe['source'] = dataframe
        print('Read: ' + str(len(dataframe.index)) + ' rows from ' + dataframe_path)
        return dataframe