# from tempfile import TemporaryFile
from xlwt import Workbook
from .sheet import Sheet


class Excel(object):
    def __init__(self):
        self.book = Workbook(encoding='utf-8')

    def save(self, file_name, dir=''):

        if not '.xls' in file_name:
            file_name += '.xls'

        file = dir + file_name

        print(file_name)
        self.book.save(file)
        # self.book.save(TemporaryFile())

    def add_sheet(self, name_sheet, columns, objects=None, object=None):
        Sheet(self.book, name_sheet, columns, objects, object)
        # if not isinstance(sheet, Sheet):
        #     raise Exception('sheet need be instance Sheet')
        #
        # self.book._Workbook__worksheets.append(sheet.sheet)
        # self.book = sheet.book

        # if not isinstance(first_sheet, Sheet):
        #     raise Exception('first_sheet need be instance Sheet')
        # self.name_first_sheet = first_sheet.name
        #
        # self.book.add_sheet_reference(first_sheet.sheet)
        # self.book = first_sheet.book
