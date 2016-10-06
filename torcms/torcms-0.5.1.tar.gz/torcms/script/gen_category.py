# -*- coding: utf-8


import yaml
import json

from torcms.model.category_model import MCategory
from openpyxl.reader.excel import load_workbook
from torcms.model.category_model import MCategory





def gen_infor_category():
    wb = load_workbook(filename='./database/meta/info_tags.xlsx')
    sheet_ranges_arr = [wb['Sheet1'], wb['Sheet2']]
    class_arr = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    sig_name_arr = []
    mappcat = MCategory()
    # 在分类中排序
    order_index = 1
    # 父类索引
    papa_index = 1
    # 子类索引
    c_index = 1
    papa_id = 0
    uid = ''
    p_dic = {}
    # 逐行遍历
    for sheet_ranges in sheet_ranges_arr:

        for row_num in range(3, 48):
            # 父类
            p_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            if p_cell_val and p_cell_val != '':
                cell_arr = p_cell_val.split(',')
                p_uid = cell_arr[0].strip().strip('t')
                role_mask = cell_arr[1].strip().strip('t')
                t_name_arr = sheet_ranges['B{0}'.format(row_num)].value.strip().split(',')
                u_uid = '{0}00'.format(p_uid)

            # 子类
            b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
            c_cell_val = sheet_ranges['C{0}'.format(row_num)].value
            if c_cell_val and c_cell_val != '':
                cell_arr = b_cell_val.split(',')
                c_iud = cell_arr[0].strip().strip('t')
                role_mask = cell_arr[1].strip().strip('t')
                t_name_arr = c_cell_val.strip().split(',')
                u_uid = '{0}{1}'.format(p_uid, c_iud)
            post_data = {
                'name': t_name_arr[0],
                'slug': t_name_arr[1],
                'order': order_index,
                'uid': u_uid,
                'role_mask': role_mask,
                'kind': '20',
            }
            print(post_data)
            mappcat.insert_data(u_uid, post_data)
            order_index = order_index + 1


def gen_doc_category():
    mcat  = MCategory()


    f = open('./database/meta/doc_catalog.yaml')
    out_dic = yaml.load(f)
    print(out_dic)
    vv = json.dumps(out_dic, indent=2)

    porder = 0
    sorder = 0
    for key in out_dic:

        if key.endswith('00'):
            uid = key[1:]
            print(uid)
            cur_dic = out_dic[key]
            porder = cur_dic['order']
            cat_dic = {
                'uid': uid,
                'slug': cur_dic['slug'],
                'name': cur_dic['name'],
                'count': 0,
                'order':porder * 100,
                'kind': '10',
            }

            mcat.insert_data(uid, cat_dic)
        else:
            sub_arr = out_dic[key]
            pid = key[1:3]

            for sub_dic in sub_arr:
                print('x' * 10)
                print(sub_dic)
                # cur_dic = sub_dic
                porder = out_dic['z' + pid + '00']['order']

                for key in sub_dic:

                    uid = key[1:]


                    cur_dic = sub_dic[key]

                    sorder = cur_dic['order']
                    cat_dic = {
                        'uid': uid,
                        'slug': cur_dic['slug'],
                        'name': cur_dic['name'],
                        'count': 0,
                        'order': porder *100 +sorder,
                        'kind': '10',
                    }

                    mcat.insert_data( pid + uid, cat_dic)

def run_gen_category():
    gen_doc_category()
    gen_infor_category()
