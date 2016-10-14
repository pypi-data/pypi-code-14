import xlwt
from .column import Column


class Sheet(object):

    name = None
    title = None
    columns = None

    title_style = xlwt.easyxf(
        'font: height 300, name Times New Roman, bold True;'
        # 'align: horizontal center;'
        # 'alignment: wrap on;'
        # 'borders: left thin, right thin, top thin, bottom thin;'
    )
    column_style = xlwt.easyxf(
        'font: bold True;'
        'align: vertical center, horizontal center;'
    )
    object_style = xlwt.easyxf(
        'align: vertical center, horizontal center;'
    )

    def _set_book(self, book):
        self.sheet = book.add_sheet(self.name)
        self._add_writes()

    def __init__(self, name=None, columns=None, objects=None, object=None, title=None):

        if name: self.name = name
        if columns: self.columns = columns
        if title: self.title = title
        if not self.columns: self.columns = []
        self._prepare_objects(objects, object)

    def _prepare_objects(self, objects, object):

        if objects:
            objects = list(objects)
        else:
            objects = []

        if object:
            objects.append(object)

        self.objects = objects

    def _add_writes(self):

        for column in self.columns:
            if not isinstance(column, Column):
                raise Exception('Every column in columns need be instace of Column')

        self._line_index = 0
        self._write_title()
        self._write_collumns()
        self._write_objects_to_sheet()

    def _write_title(self):
        if self.title:
            self.sheet.row(self._line_index).height = 450
            self.sheet.write(self._line_index, 0, self.title, self.title_style)

            self._line_index += 2

    def _write_collumns(self):
        for index, column in enumerate(self.columns):
            self.sheet.write(self._line_index, index, column.name, self.column_style)
            if column.width:
                self.sheet.col(index).width = column.width

        if self.columns: self._line_index += 1

    def _write_objects_to_sheet(self):

        start_writing_str = self._line_index
        for index_object, object in enumerate(self.objects):
            for index_column, column in enumerate(self.columns):
                record = column.get_attr_for(object)
                self.sheet.write(start_writing_str + index_object, index_column, record, self.object_style)

        self._line_index += len(self.objects)
