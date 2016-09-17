class NoAssignedValueError(Exception):
    pass


class FileError(Exception):
    pass


def _cli(ext: str):
    raise FileError('cannot open file with this extension: %s.' % ext)


def switch_bool(v: bool):
    return False if v else True

def compare(n1:str,n2:str,i=False):
    return n1.lower()==n2.lower() if i else n1==n2

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
