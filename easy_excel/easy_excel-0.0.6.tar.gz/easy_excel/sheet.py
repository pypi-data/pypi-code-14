from xlwt import Workbook
from .column import Column


class Sheet(object):

    def __init__(self, book, name_sheet, columns, objects=None, object=None):
        self.sheet = book.add_sheet(name_sheet)
        self.name = name_sheet
        self.columns = columns

        self.prepare_objects(objects, object)
        self.add_writes()

    def prepare_objects(self, objects, object):

        if objects:
            objects = list(objects)
        else:
            objects = []

        if object:
            objects.append(object)

        self.objects = objects

    def add_writes(self):

        for column in self.columns:
            if not isinstance(column, Column):
                raise Exception('Every column in columns need be instace of Column')

        self.write_collumns()
        self.write_objects_to_sheet()

    def write_collumns(self):
        for index, column in enumerate(self.columns):
            self.sheet.write(0, index, column.name)
            if column.width:
                self.sheet.col(index).width = column.width

    def write_objects_to_sheet(self):

        start_writing_str = 2
        for index_object, object in enumerate(self.objects):
            for index_column, column in enumerate(self.columns):
                record = column.get_attr_for(object)
                self.sheet.write(start_writing_str + index_object, index_column, record)
