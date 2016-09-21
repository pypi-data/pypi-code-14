import xlrd
from collections import defaultdict

def read_sheet_into_matrix(sh,xf):
    matrix = []
    for row in range(sh.nrows):
        vcol = []
        for col in range(sh.ncols):
            cell = sh.cell_value(row,col)
            if xf:
                cell = (1, sh.cell(row,col), sh)
            vcol.append( cell )
        matrix.append(vcol)
    return matrix

def read_book_into_matrix(wb, sheet_idx, xf = True):
    sh = wb.sheet_by_index(sheet_idx)
    return read_sheet_into_matrix(sh,xf)

def read_xls_into_matrix(fname, sheet_idx, xf = True):
    wb = xlrd.open_workbook(fname, formatting_info = xf)
    return read_book_into_matrix(wb,sheet_idx,xf)


def read_xls_into_dictionary(fname, sheet, xf = True):
    matrix = read_xls_into_matrix(fname,sheet, xf)
    headers_def = matrix.pop(0)
    dictionary = defaultdict(list)
    headers = []
    for num,name in enumerate(headers_def):
        if len(name)>0:
            headers.append((num,name))
    for row in matrix:
        for col,name in headers:            
            dictionary[name].append( row[col] )
    return dictionary

def read_xls_into_dataframe(fname, sheet, keyname, multiline=False, xf = True):
    matrix = read_xls_into_matrix(fname,sheet, xf)
    headers_def = matrix.pop(0)
    dataframe = defaultdict(list)
    headers = []
    keynum = None
    for num,name in enumerate(headers_def):
        if len(name)>0:
            if name == keyname:
                keynum = num
            else:
                headers.append((num,name))            
    for row in matrix:
        key = row[keynum]
        if key not in dataframe or multiline:
            for col,name in headers:
                dataframe[key].append(row[col])
            if multiline:
                dataframe[key].append("NEWLINE")                
    return dataframe, headers

def read_xls_into_dataset(fname, sheet, keyname, xf = True):
    dictionary = read_xls_into_dictionary(fname,sheet, xf)
    headers = dictionary.keys()
    lids = dictionary[keyname]
    dataset = {}
    for key, col in dictionary.items():
        for num,lid in enumerate(lids):
            if lid not in dataset:
                dataset[lid] = {}
            if key not in dataset[lid]:
                dataset[lid][key] = []
            dataset[lid][key].append(col[num])
    return dataset

def read_xls_into_dataset1(fname, sheet, keyname, xf = True):
    dataset = read_xls_into_dataset(fname,sheet,keyname, xf)
    for key1, idict in dataset.items():
        for key2 in idict.keys():
            dataset[key1][key2] = dataset[key1][key2][0]
    return dataset
            
    
                               
