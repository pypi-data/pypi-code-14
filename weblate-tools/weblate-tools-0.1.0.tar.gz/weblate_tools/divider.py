# -*- encoding: utf-8 -*-
import os
import re

# 对大块po文件进行分割和合并的代码


class Divider():
    """
    将大小较大的po文件按字节数或待翻译条数分割成等大的小文件
    默认使用相同的文件名加上分隔符和数字后缀
    如abc.po分割成abc-1.po/abc-2.po/.etc
    """
    PO_SUFFIX = '.po'

    def __init__(self, po_filename, dir_name='', separator='-'):
        self.po_filename = po_filename
        self.dir_name = dir_name
        self.separator = separator

    def cut_po_file(self, output_filename, **kwargs):
        """
        :param output_filename: 输出文件名
        :param kwargs: key-value参数，key需要为'byte_length'/'item_count'，来表示字节数或条目数
        :return: 无返回
        """
        with open(self.dir_name + self.po_filename + self.PO_SUFFIX, 'rt') as rf:
            lines = rf.readlines()  # 读取所有行数
            package = []  # 暂时存放一个小文件的所有行，达到大小后存进一个文件里
            file_count = 1  # 文件个数，递增，用来标示数字后缀

            # 获取第一个翻译条目的行号，去掉文件头部的无关信息
            for i in lines:  # 遍历所有行
                if i.startswith('#.'):  # 如果以#.开头，表示是一个翻译条目的开始
                    lines = lines[lines.index(i):]
                    break
            
            # 根据输入参数确定按字节或条目数量确定大小
            if 'byte_length' in kwargs.keys():
                # 如果是字节数，将package中所有行拼接并计算长度
                package_size = len(''.join(package))
                goal_size = kwargs['byte_length']
            elif 'item_count' in kwargs.keys():
                # 如果是条目数，直接计算package中所有行，但条目数=行数/4
                package_size = len(package)
                goal_size = kwargs['item_count'] * 4
            else:
                raise KeyError, 'Invalid key value: it should be "byte_length" or "item_count"'
            
            # 确定输出文件名，如果没有给定，则使用原来的文件名
            if output_filename is None:
                output_filename = self.po_filename
                
            for i in range(len(lines)):
                if package_size < goal_size:
                    # 如果不满足大小，往package中再添加一行，继续循环
                    package.append(lines[i])
                    package_size += 1
                elif not lines[i].startswith('#.'):
                    # 如果满足了大小，但当前行不是第一行
                    # 说明上一个条目还没有完整结束，依然继续添加
                    # 直到满足大小之后的第一个条目结束
                    package.append(lines[i])
                    package_size += 1
                else:
                    # 满足上面两个条件之后，将package中所有行输出到新文件中
                    with open(self.dir_name + output_filename + self.separator + str(file_count) + self.PO_SUFFIX, 'w') \
                            as wf:
                        wf.writelines(['msgid ""\n', 'msgstr ""\n\n'])  # 第一行为空白的文件头
                        wf.writelines(package)
                        file_count += 1
                    package = [lines[i]]  # package重置为下一个条目的第一行
                    package_size = 1
                    
            # 遍历结束后，对不满足大小的剩余行全部输出到最后一个文件中
            with open(self.dir_name + output_filename + self.separator + str(file_count) + self.PO_SUFFIX, 'w') as wf:
                wf.writelines(['msgid ""\n', 'msgstr ""\n\n'])
                wf.writelines(package)

    def merge_po_file(self, postfix='', input_filename=None, output_filename=None):
        """
        weblate会同步整个文件和分文件，这个方法并不常用
        :param postfix: 合并文件的后缀
        :param input_filename: 输入文件名
        :param output_filename: 输出文件名
        :return:
        """
        # 如果没有指定具体的文件名，则使用初始的po文件名
        if input_filename is None:
            input_filename = self.po_filename
        if output_filename is None:
            output_filename = self.po_filename

        # 获取所有匹配（文件名+分隔符）的小文件
        po_files = [file for file in os.listdir(self.dir_name) if re.compile(input_filename+self.separator).match(file)]
        # 按照数字后缀将文件名进行排序
        po_files.sort(key=lambda x:int(re.compile(input_filename+self.separator + '(\d+)').match(x).group(1)))

        total = []
        for po in po_files:
            with open(self.dir_name + po, 'r') as rf:
                lines = rf.readlines()  # 读取所有行数

                # 获取第一个翻译条目的行号，去掉文件头部的无关信息
                for i in lines:  # 遍历所有行
                    if i.startswith('#.'):  # 如果以#.开头，表示是一个翻译条目的开始
                        lines = lines[lines.index(i):]
                        break
                total += lines
        with open(self.dir_name + output_filename + self.separator + postfix + self.PO_SUFFIX, 'w') as wf:
            wf.writelines(['msgid ""\n', 'msgstr ""\n\n'])  # 第一行为空白的文件头
            wf.writelines(total)