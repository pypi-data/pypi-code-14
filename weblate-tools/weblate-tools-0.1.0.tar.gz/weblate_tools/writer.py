# -*- encoding: utf-8 -*-
import xlrd
from xlutils.copy import copy


class Writer():

    PO_SUFFIX = '.po'

    def __init__(self):
        pass

    def write_xlsx(self, read_filename, write_filename, sheet_num, en_column, ch_column,
                  start_row=1, end_row=None):
        """
        读取po文件中翻译完毕的内容，填进xlsx文件中
        :param read_filename: po文件，不带后缀
        :param write_filename: xlsx文件，需要后缀
        :param sheet_num: sheet编号
        :param en_column: 英文列号
        :param ch_column: 译文列号
        :param start_row: 起始行号，默认为1跳过表头
        :param end_row: 终止行号，默认为全部
        :return:
        """

        read_book = xlrd.open_workbook(write_filename)
        write_book = copy(read_book)
        read_sheet = read_book.sheet_by_index(sheet_num)

        if end_row is None:
            end_row = read_sheet.nrows
        write_sheet = write_book.get_sheet(sheet_num)

        with open(read_filename + self.PO_SUFFIX, 'r') as f:
            total = f.readlines()

        # 将原文和译文以字典键值对的形式临时储存
        zh_matchs = {}
        for i in range(0, len(total)):
            if total[i].startswith('msgid'):
                zh_matchs[total[i][7:-2]] = total[i+1][8:-2]

        for i in range(start_row, end_row):
            if read_sheet.col_values(en_column)[i] != "" and read_sheet.col_values(en_column)[i] in zh_matchs.keys():
                write_sheet.write(i, ch_column, zh_matchs[str(read_sheet.col_values(en_column)[i])].decode('utf-8'))
        write_book.save(write_filename)