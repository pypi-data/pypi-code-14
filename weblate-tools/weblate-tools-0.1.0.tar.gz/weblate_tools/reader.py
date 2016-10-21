# -*- encoding: utf-8 -*-
import os
import xlrd


class Reader():
    
    PO_SUFFIX = '.po'

    def __init__(self):
        pass

    def read_txt(self, read_filename, output_filename=None):
        """
        未测试
        :param read_filename:
        :param output_filename:
        :return:
        """
        if output_filename is None:
            output_filename = os.path.splitext(read_filename)[0]

        with open(read_filename, 'rt') as txtfile:
            txtstr = txtfile.read()
            acs = txtstr.split('\n\n')
            with open(output_filename + self.PO_SUFFIX, 'w') as pofile:
                pofile.writelines(['msgid ""\n', 'msgstr ""\n\n'])
                for a in acs:
                    contents = a.split('\n')
                    if len(contents) > 1:
                        pofile.writelines([
                            '#. Achievements: ' + contents[0] + ';\n',
                            'msgid "' + contents[0] + '"\n',
                            'msgstr "' + '"\n\n'])
                        pofile.writelines([
                            '#. Achievements: ' + contents[0] + ';\n',
                            'msgid "' + contents[1] + '"\n',
                            'msgstr "' + '"\n\n'])
                    else:
                        pofile.writelines([
                            '#. Achievements: ' + contents[0] + ';\n',
                            'msgid "' + contents[0] + '"\n',
                            'msgstr "' + '"\n\n'])

    def read_xlsx(self, read_filename, sheet_num, id_column, en_column, ch_column,
                  start_row=1, end_row=None, output_filename=None):
        """
        读取xlsx中的信息，如果在一个sheet中有多个列，请多次调用该方法并指定不同的输出文件名
        :param read_filename: 读取的文件名，带后缀（不同版本的文件名后缀可能有区别）
        :param sheet_num: 工作簿序列号
        :param id_column: 标示性说明的列数
        :param en_column: 英文列数
        :param ch_column: 中文列数（最好应事先准备好预备之后写入）
        :param start_row: 开始遍历的行数，一般跳过表头，即第一行
        :param end_row: 结束行数，可不填，默认为全部行
        :param output_filename: 输出文件名，如不填，默认为原文件去掉后缀+po
        :return:
        """
        data = xlrd.open_workbook(read_filename)
        table = data.sheets()[sheet_num]

        if end_row is None:
            end_row = table.nrows
        if output_filename is None:
            output_filename = os.path.splitext(read_filename)[0]

        with open(output_filename + self.PO_SUFFIX, 'w') as pofile:
            pofile.writelines(['msgid ""\n', 'msgstr ""\n\n'])
            for i in range(start_row, end_row):
                # print table.row_values(i)
                row_info = table.row_values(i)
                if row_info[id_column] != '' and row_info[en_column] != '':
                    row1 = '#. ' + str(row_info[id_column]) + ';\n'
                    row2 = 'msgid "' + str(row_info[en_column].encode('utf-8')) + '"\n'
                    row3 = 'msgstr "' + str(row_info[ch_column].encode('utf-8')) + '"\n\n'
                    print [row1, row2, row3]
                    pofile.writelines([row1, row2, row3])