import re, openpyxl, csv, json, os


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
        self._wb = openpyxl.Workbook()
        self._sheet = self._wb.get_sheet_by_name("Sheet")
        temp = 1
        for i in self._formatted_content:
            self._write_row(i, temp)
            temp += 1

    def convert_to_csv(self, next_cell_token=',', next_row_token='\n'):
        """convert the text file into .csv file using csv module."""
        writer = csv.writer(open(self._path, 'w', newline=''), delimiter=next_cell_token,
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
        file.write(json.dumps(self.content))
        file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self):
        return self.content
