from binaryornot.check import is_binary as _is_binary

from .shared._coll import BaseFile as __base
from .shared._coll import FileError

__doc__ = '''This module contains all the
functions for text file in pyil.'''


class TextFile(__base):
    def __init__(self, name: str, res_name: str, **attri):
        """name >- the path of the original file(text file)
        res_name >- the path of the destination file
        (include file name and the extension for the first
        one but no extension for the second one)"""
        if _is_binary(name):  # Check if it is text file.
            raise FileError('Cannot open binary files: %s' % name)
        super().__init__()  # Call super class so I don't have to declare the variable again.
        if len(attri) >= 1:
            for key, item in attri.items():
                if key == 'next_ele_token':
                    self._ne = attri['next_ele_token']
                elif key == 'next_line_token':
                    self._nl = attri['next_line_token']
                elif key == 'delete_original_file':
                    self._dof = attri['delete_original_file']
                else:
                    raise KeyError('No such attributes.')
        self._path = res_name
        self._opath = name
        self._ftext = self._get_ftext()

    def convert_to_binary_file(self):
        """Convert the file into binary file with extension using pickle.dump."""
        from .enum.modifiable import write_to_binary
        write_to_binary(self.text, open(self._path + '.dat', 'wb'))


class BinaryFile(__base):
    def __init__(self, name: str, res_name: str, **attri):
        """name >- the path of the original file(binary file, uses read_binary() to read)
        res_name >- the path of the destination file
        (include file name and the extension for the first
        one but no extension for the second one)"""
        if not _is_binary(name):  # Check if it is binary file.
            raise FileError('Cannot open text files: %s' % name)
        super().__init__()  # Call super class.
        if len(attri) >= 1:  # Get attributes.
            for key, item in attri.items():
                if key == 'next_ele_token':
                    self._ne = attri['next_ele_token']
                elif key == 'next_line_token':
                    self._nl = attri['next_line_token']
                elif key == 'delete_original_file':
                    self._dof = attri['delete_original_file']
                else:
                    raise KeyError('No such attributes.')
        self._path = res_name
        self._opath = name
        self._ftext = self._get_ftext()

    @property
    def text(self):
        """The text in the file, change read_binary_file()
         to change the way it reads the text."""
        from .enum.modifiable import read_binary_file
        return read_binary_file(open(self._opath, 'rb'))

    def write(self, obj):
        """Uses write_to_binary function to
        write."""
        from .enum.modifiable import write_to_binary
        write_to_binary(obj, open(self._opath, 'wb'))
        self._ftext = self._get_ftext()
        return len(obj)

    def append(self, obj: str):
        """Uses write_to_binary function to
        write."""
        from .enum.modifiable import write_to_binary
        write_to_binary(obj, open(self._opath, 'ab'))
        self._ftext = self._get_ftext()
        return len(self.text)

    def convert_to_text_file(self):
        """Convert to text file."""
        f = open(self._path, 'w')
        f.write(self.text)
        f.close()


class CsvFile:
    def __init__(self, name, res_name):
        self.__path = name
        self.__respath = res_name

    @property
    def text(self):
        return open(self.__path).read()

    @property
    def csvformatted_text(self):
        import csv
        return list(csv.reader(open(self.__path)))

    def convert_to_text(self, pure_text=True, next_ele_token=' ', next_line_token='\n'):
        if pure_text:
            with open(self.__respath, 'w')as f:
                f.write(self.text)
        else:
            with open(self.__respath, 'a')as f:
                for i in self.csvformatted_text:
                    f.write(next_ele_token.join(i))
                    f.write(next_line_token)

    def convert_to_binary(self, pure_text=True, next_ele_token=' ', next_line_token='\n'):
        from .enum.modifiable import write_to_binary
        if pure_text:
            write_to_binary(self.text, open(self.__respath, 'wb'))
        else:
            for i in self.csvformatted_text:
                write_to_binary(i, open(self.__respath, 'a'))
                write_to_binary(next_line_token, open(self.__respath, 'a'))

    def convert_to_xlsx(self):
        """Convert the file into Microsoft spread sheet."""
        import openpyxl
        self.__wb = openpyxl.Workbook()
        self.__sheet = self.__wb.get_sheet_by_name("Sheet")
        temp = 1
        for i in self.csvformatted_text:
            self.__write_row(i, temp)
            temp += 1
        self.__wb.save(self.__path + '.xlsx')
        del self.__wb
        del self.__sheet

    def __write_row(self, list_to_write, start_row, start_column=1):
        try:
            self.__sheet.cell(row=start_row, column=start_column).value = list_to_write[start_column - 1]
            return self.__write_row(list_to_write, start_row, start_column=start_column + 1)
        except IndexError:
            return

    def convert_to_json(self, pure_text=True):
        import json
        if pure_text:
            json.dump(self.text, open(self.__respath, 'w'))
        else:
            json.dump(self.csvformatted_text, open(self.__respath, 'w'))
