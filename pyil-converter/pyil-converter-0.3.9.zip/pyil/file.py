import pickle as _pickle
import os as _os
from ._collection import base_file
from binaryornot.check import is_binary as _is_binary
from ._collection import FileError

__doc__ = '''This module contains all the
functions for text file in pyil.'''



def write_to_binary(obj, file):
    """using pickle.dump to convert to binary file.
    If you want to change the method, do:
    write_to_binary=your_function
    make sure your the order of the parameter of your function
    is same as this one."""
    _pickle.dump(obj, file)


def read_binary_file(file):
    """Uses pickle.load() to extract the string from
    the binary file, use read_binary=your_function to
    modify it. It will accept 1 parameter which the
    file object it's going to get the information."""
    return _pickle.load(file)


class text_file(base_file):
    def __init__(self, name: str, res_name: str, **attri):
        """name >- the path of the original file(text file)
        res_name >- the path of the destination file
        (include file name and the extension for the first
        one but no extension for the second one)"""
        if _is_binary(name):
            raise FileError('Cannot open binary files: %s' % name)
        ne, nl, self._dof = ' ', '\n', False
        if len(attri) >= 1:
            for key, item in attri.items():
                if key == 'next_ele_token':
                    ne = attri['next_ele_token']
                elif key == 'next_line_token':
                    nl = attri['next_line_token']
                elif key == 'delete_original_file':
                    self._dof = attri['delete_original_file']
                else:
                    raise KeyError('No such attributes.')
        self._f = open(name, 'r+')
        self.content = self._f.read()
        """The strings contained in the file."""
        temp, temp1, temp2 = [], '', []
        for i in self.content + nl[0]:
            if i in ne:
                temp2.append(temp1)
                temp1 = ''
            elif i in nl:
                temp2.append(temp1)
                temp.append(temp2)
                temp1 = ''
                temp2 = []
            else:
                temp1 += i
        self._path = res_name
        self._formatted_content = temp.copy()
        self._opath = name

    def convert_to_binary_file(self):
        """Convert the file into binary file with extension using pickle.dump."""
        write_to_binary(self.content, open(self._path + '.dat', 'wb'))

    def close(self):
        """Close and save the file."""
        try:
            self._wb.save(self._path + '.xlsx')
        except AttributeError:
            pass
        self._f.close()
        if self._dof:
            _os.unlink(self._opath)


class binary_file(base_file):
    def __init__(self, name: str, res_name: str, **attri):
        """name >- the path of the original file(binary file, uses read_binary() to read)
        res_name >- the path of the destination file
        (include file name and the extension for the first
        one but no extension for the second one)"""
        if not _is_binary(name):
            raise FileError('Cannot open text files: %s' % name)
        ne, nl, self._dof = ' ', '\n', False
        if len(attri) >= 1:
            for key, item in attri.items():
                if key == 'next_ele_token':
                    ne = attri['next_ele_token']
                elif key == 'next_line_token':
                    nl = attri['next_line_token']
                elif key == 'delete_original_file':
                    self._dof = attri['delete_original_file']
                else:
                    raise KeyError('No such attributes.')
        self._f = open(name, 'rb+')
        self.content = read_binary_file(self._f)
        """The strings contained in the file."""
        temp, temp1, temp2 = [], '', []
        for i in self.content + nl[0]:
            if i in ne:
                temp2.append(temp1)
                temp1 = ''
            elif i in nl:
                temp2.append(temp1)
                temp.append(temp2)
                temp1 = ''
                temp2 = []
            else:
                temp1 += i
        self._path = res_name
        self._formatted_content = temp.copy()
        self._opath = name

    def write(self, obj):
        """Uses write_to_binary function to
        write."""
        write_to_binary(obj, self._f)

    def append(self, obj: str):
        """Uses write_to_binary function to
        write."""

        write_to_binary(self.content + obj, self._f)

    def convert_to_text_file(self):
        f = open(self._path, 'w')
        f.write(self.content)
        f.close()

    def close(self):
        """Close and save the file."""
        try:
            self._wb.save(self._path + '.xlsx')
        except AttributeError:
            pass
        self._f.close()
        if self._dof:
            _os.unlink(self._opath)
