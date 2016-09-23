import re


class NoAssignedValueError(Exception):
    pass


class FileError(Exception):
    pass


def _cli(ext: str):
    raise FileError('cannot open file with this extension: %s.' % ext)


def switch_bool(v: bool):
    return False if v else True


def compare(n1: str, n2: str, i=False):
    return re.match(n2.lower(), n1.lower()) != None if i else re.match(n2, n1) is not None


class simplify_str:
    def __init__(self, value: str, casei=False):
        self.v = value
        self.i = casei

    def simplify(self):
        try:
            self.v = float(self.v)
        except ValueError:
            pass
        try:
            self.v = int(self.v)
        except ValueError:
            pass
        try:
            self.v = self._toBool()
        except (ValueError, AttributeError):
            pass
        try:
            self.v = self._toNone()
        except (ValueError, AttributeError):
            pass
        return self.v

    def _toNone(self):
        if self.i:
            if self.v.lower() == 'none':
                return None
            raise ValueError('Unknown None value represation.')
        else:
            if self.v == 'None':
                return None
            raise ValueError('Unknown None value represation.')

    def _toBool(self):
        if self.i:
            if self.v.lower() == 'true':
                return True
            elif self.v.lower() == 'false':
                return False
            raise ValueError('Unknown boolean value.')
        else:
            if self.v == 'True':
                return True
            elif self.v == 'False':
                return False
            raise ValueError('Unknown boolean value.')


class base_file:
    def __init__(self):
        pass
