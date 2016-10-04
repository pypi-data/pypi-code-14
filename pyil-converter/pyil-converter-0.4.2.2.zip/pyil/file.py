import pickle as _pickle
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


class TextFile(base_file):
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

    def convert_to_binary_file(self):
        """Convert the file into binary file with extension using pickle.dump."""
        write_to_binary(self.text, open(self._path + '.dat', 'wb'))


class BinaryFile(base_file):
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

    @property
    def text(self):
        """The text in the file, change read_binary_file()
         to change the way it reads the text."""
        return read_binary_file(open(self._opath, 'rb'))

    def write(self, obj):
        """Uses write_to_binary function to
        write."""
        write_to_binary(obj, open(self._opath, 'wb'))
        return len(obj)

    def append(self, obj: str):
        """Uses write_to_binary function to
        write."""
        write_to_binary(obj, open(self._opath, 'ab'))
        return len(self.text)

    def convert_to_text_file(self):
        """Convert to text file."""
        f = open(self._path, 'w')
        f.write(self.text)
        f.close()
