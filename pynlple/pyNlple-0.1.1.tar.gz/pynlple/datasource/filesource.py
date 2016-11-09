# -*- coding: utf-8 -*-
import csv
import io
from os import walk, path

import pandas

from pynlple.module import append_paths, file_name


class FileDataSource(object):
    """Class for providing json data from json files."""

    @staticmethod
    def open_file(filepath, encoding='utf8'):
        return io.open(filepath, 'rt', encoding=encoding)

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

    SOURCE_COLUMN_NAME = 'source_filepath'

    @staticmethod
    def read_dataframe_from_folder(folderpath, extension_suffix, separator='\t', fill_na_map=None, encoding='utf8'):
        dataframe = pandas.DataFrame()

        for filepath in FileDataSource.iter_folder_filepaths(folderpath, extension_suffix):
            subframe = FileDataSource.read_dataframe(filepath, separator, fill_na_map, encoding)
            subframe[FileDataSource.SOURCE_COLUMN_NAME] = filepath
            dataframe = dataframe.append(subframe)

        return dataframe

    @staticmethod
    def read_dataframe(dataframe_path, separator='\t', fill_na_map=None, encoding='utf8'):
        dataframe = pandas.read_csv(dataframe_path, sep=separator, quoting=csv.QUOTE_NONE, encoding=encoding)
        dataframe.set_index('id', inplace=True)
        if fill_na_map:
            for key, value in fill_na_map.iteritems():
                dataframe[key].fillna(value, inplace=True)
        print('Read: ' + str(len(dataframe.index)) + ' rows from ' + dataframe_path)
        return dataframe

    @staticmethod
    def write_dataframe(dataframe, dataframe_path, separator='\t', encoding='utf8'):
        dataframe.to_csv(dataframe_path, sep='\t', encoding='utf8')
        print('Write: ' + str(len(dataframe.index)) + ' rows to ' + dataframe_path)

    @staticmethod
    def write_dataframe_to_folder(dataframe, folderpath, separator='\t', encoding='utf8'):
        for filepath in dataframe[FileDataSource.SOURCE_COLUMN_NAME].unique():
            subframe = dataframe.loc[FileDataSource.SOURCE_COLUMN_NAME == filepath]
            filename = file_name(filepath)
            new_path = append_paths(folderpath, filename)
            FileDataSource.write_dataframe(subframe, new_path, separator, encoding)
