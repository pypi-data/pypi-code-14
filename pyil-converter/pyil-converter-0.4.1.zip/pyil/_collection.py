import re, openpyxl, csv, json, docx, docx.shared, os


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
        self._opath = ''
        self._path = ''
        self._nl = ['\n']
        self._ne = [' ']
        self._dof = False

    @property
    def text(self):
        """The string contained in the file."""
        with open(self._opath)as f:
            return f.read()

    @property
    def _ftext(self):
        temp, temp1, temp2 = [], '', []
        for i in self.text + self._nl[0]:
            if i in self._ne:
                temp2.append(temp1)
                temp1 = ''
            elif i in self._nl:
                temp2.append(temp1)
                temp.append(temp2)
                temp1 = ''
                temp2 = []
            else:
                temp1 += i
        return temp.copy()

    def write(self, obj: str):
        """Write to the original file."""
        with open(self._opath, 'w')as f:
            f.write(obj)
        return len(obj)

    def append(self, obj: str):
        """Append something to the original file."""
        with open(self._opath, 'a')as f:
            f.write(obj)
        return len(obj)

    def convert_to_xlsx(self):
        """Convert the file into Microsoft spread sheet."""
        self._wb = openpyxl.Workbook()
        self._sheet = self._wb.get_sheet_by_name("Sheet")
        temp = 1
        for i in self._ftext:
            self._write_row(i, temp)
            temp += 1
        self._wb.save(self._path + '.xlsx')

    def convert_to_csv(self, next_cell_token=',', next_row_token='\n'):
        """convert the text file into .csv file using csv module."""
        writer = csv.writer(open(self._path, 'w', newline=''), delimiter=next_cell_token,
                            lineterminator=next_row_token)
        for i in self._ftext:
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
        file.write(json.dumps(self.text))
        file.close()

    def close(self, ignore_error=False):
        """Close the file, return 0 if succeeded."""
        if ignore_error:
            try:
                if self._dof:
                    os.unlink(self._opath)
                return 0
            except:
                return 1
        else:
            if self._dof:
                os.unlink(self._opath)
            return 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self):
        return self.text

    def convert_to_docx(self, font=13):
        """Convert to a .docx file."""
        doc = docx.Document()
        para = doc.add_paragraph(self.text)
        para.font.size = docx.shared.Pt(font)
        doc.save(self._path + '.docx')
