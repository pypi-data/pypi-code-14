import os
from tempfile import TemporaryFile
from xlwt import Workbook
from .sheet import Sheet


class Excel(object):
    def __init__(self):
        self.book = Workbook(encoding='utf-8')

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

    def save(self, file_name, dir=''):
        if not '.xls' in file_name:
            file_name += '.xls'

        file = dir + file_name
        self.create_dirs_if_not_existed(file)
        print(file_name)

        self.book.save(TemporaryFile())
        self.book.save(file)

    @staticmethod
    def create_dirs_if_not_existed(filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                raise Exception()