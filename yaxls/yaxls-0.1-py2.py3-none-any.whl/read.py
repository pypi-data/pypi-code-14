import xlrd
from collections import defaultdict

def read_xls_into_matrix(fname, sheet_idx):
    wb = xlrd.open_workbook(fname)
    sh = wb.sheet_by_index(sheet_idx)
    matrix = []
    for row in range(sh.nrows):
        vcol = []
        for col in range(sh.ncols):
            vcol.append( sh.cell_value(row,col))
        matrix.append(vcol)
    return matrix
    

def read_xls_into_dictionary(fname, sheet):
    matrix = read_xls_into_matrix(fname,sheet)
    headers_def = matrix.pop(0)
    dictionary = defaultdict(list)
    headers = []
    for num,name in enumerate(headers_def):
        if len(name)>0:
            headers.append((num,name))
    print headers
    for row in matrix:
        for col,name in headers:            
            dictionary[name].append( row[col] )
    return dictionary

def read_xls_into_dataframe(fname, sheet, keyname, multiline=False):
    matrix = read_xls_into_matrix(fname,sheet)
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

def read_xls_into_dataset(fname, sheet, keyname):
    dictionary = read_xls_into_dictionary(fname,sheet)
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

def read_xls_into_dataset1(fname, sheet, keyname):
    dataset = read_xls_into_dataset(fname,sheet,keyname)
    for key1, idict in dataset.items():
        for key2 in idict.keys():
            dataset[key1][key2] = dataset[key1][key2][0]
    return dataset
            
    
                               
