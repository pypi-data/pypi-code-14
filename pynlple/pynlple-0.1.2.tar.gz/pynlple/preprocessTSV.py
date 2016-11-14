# -*- coding: utf-8 -*-
from .processing.preprocessor import DefaultPreprocessorStack

from pynlple.datasource.filesource import FileDataSource

extension = '.tsv'
key = '2016.11.01'
in_folder_path = 'E:/Data/mentions_deduplicated/' + key
out_folder_path = 'E:/Data/mentions_preprocessed/' + key

target_columns = [u'text']

replacers_stack = DefaultPreprocessorStack()

for filepath in FileDataSource.iter_folder_filepaths(in_folder_path, extension):
    dataframe = FileDataSource.read_dataframe(filepath, '\t', {u'text': u''}, 'utf8')

    for target_column in target_columns:
        dataframe[target_column] = dataframe[target_column].apply(replacers_stack.preprocess)

    newpath = filepath.replace(in_folder_path, out_folder_path, 1)
    dataframe.to_csv(newpath, sep='\t', encoding='utf8')
    print('Write: ' + str(len(dataframe.index)) + ' rows to ' + newpath)

