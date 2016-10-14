import os
from tempfile import TemporaryFile
from xlwt import Workbook
from .sheet import Sheet


class Excel(object):
    def __init__(self):
        self.book = Workbook(encoding='utf-8')
        self.sheets = []

    def add_sheet(self, sheet):
        if not isinstance(sheet, Sheet):
            raise Exception('sheet need be instance Sheet')

        self.sheets.append(sheet)
        sheet._set_book(self.book)

    def save(self, file_name, dir=''):
        if not '.xls' in file_name:
            file_name += '.xls'

        file = dir + file_name
        self.create_dirs_if_not_existed(file)

        self.book.save(TemporaryFile())
        self.book.save(file)

    @staticmethod
    def create_dirs_if_not_existed(filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                raise Exception()