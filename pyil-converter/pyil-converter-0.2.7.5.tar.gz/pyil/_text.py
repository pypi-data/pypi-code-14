import os as _os
import openpyxl as _openpyxl
import pickle as _pickle
import csv as _csv
import json as _json
from binaryornot.check import is_binary as _is_binary
from ._collection import FileError
__doc__ = '''This module contains all the
functions for text file in pyil.'''

default_ele_token = [',']
default_line_token = ['\n']


def write_to_binary(obj, file):
    """using pickle.dump to convert to binary file.
    If you want to change the method, do:
    write_to_binary=your_function
    make sure your the order of the parameter of your function
    is same as this one."""
    _pickle.dump(obj, file)


class text_file:
    def __init__(self, name: str, res_name: str, next_ele_token=default_ele_token, next_line_token=default_line_token):
        """name >- the path of the original file(text file)
        res_name >- the path of the destination file
        (include file name and the extension for the first
        one but no extension for the second one)"""
        if _is_binary(name):
            raise FileError('Cannot open binary files: %s' % name)
        self._f = open(name, 'r+')
        self.content = self._f.read()
        temp, temp1, temp2 = [], '', []
        for i in self.content + next_line_token[0]:
            if i in next_ele_token:
                temp2.append(temp1)
                temp1 = ''
            elif i in next_line_token:
                temp2.append(temp1)
                temp.append(temp2)
                temp1 = ''
                temp2 = []
            else:
                temp1 += i
        self._path = res_name
        self._formatted_content = temp.copy()
        self.delete_original_file = False
        self._opath = name

    def write(self, obj: str):
        """Write to the original file."""
        self._f.write(obj)
        return len(self.content)

    def append(self, obj: str):
        """Append something to the original file."""
        self._f.write(self.content + obj)
        return len(obj)

    def convert_to_xlsx(self):
        """Convert the file into Microsoft spread sheet."""
        self._wb = _openpyxl.Workbook()
        self._sheet = self._wb.get_sheet_by_name("Sheet")
        temp = 1
        for i in self._formatted_content:
            self._write_row(i, temp)
            temp += 1

    def convert_to_binary_file(self):
        """Convert the file into binary file with extension using pickle.dump."""
        write_to_binary(self.content, open(self._path + '.dat', 'wb'))

    def convert_to_csv(self, next_cell_token=',', next_row_token='\n'):
        """convert the text file into .csv file using csv module."""
        writer = _csv.writer(open(self._path, 'w', newline=''), delimiter=next_cell_token,
                             lineterminator=next_row_token)
        for i in self._formatted_content:
            writer.writerow(i)

    def _write_row(self, list_to_write, start_row, start_column=1):
        try:
            self._sheet.cell(row=start_row, column=start_column).value = list_to_write[start_column - 1]
            return self._write_row(list_to_write, start_row, start_column=start_column + 1)
        except IndexError:
            return

    def convert_to_json(self):
        """Use json module to convert the file into .json file."""
        file = open(self._path + '.json', 'w')
        file.write(_json.dumps(self.content))
        file.close()

    def close(self):
        """Close and save the file."""
        try:
            self._wb.save(self._path + '.xlsx')
        except AttributeError:
            pass
        self._f.close()
        if self.delete_original_file:
            _os.unlink(self._opath)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

