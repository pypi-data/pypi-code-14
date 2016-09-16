import xlwt

def write_xls_from_matrix(fname, sheet_name, matrix):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet_name)    
    for r,row in enumerate(matrix):
        for c,cell in enumerate(row):
            ws.write(r, c, cell)
    wb.save(fname)


def write_xls_from_dictionary(fname, sheet_name, dictionary, headers = None):
    mheaders = sorted(dictionary.keys())
    if headers is None:
        headers = mheaders
    else:
        mheaders = [ header for header in mheaders if header not in headers  ]
        headers = list(headers)
        headers.extend(mheaders)
    matrix = [ [ k,] for k in dictionary[headers[0]] ]
    matrix.insert(0, headers)
    for c,key in enumerate(headers[1:]):
        column = dictionary[key]
        for r,cell in enumerate(column):
            matrix[r+1].append(cell)
    write_xls_from_matrix(fname, sheet_name, matrix)
    return matrix

    
def write_xls_from_dataframe(fname, sheet, keyname, headers, multiline=0):
    pass

def write_xls_from_dataset(fname, sheet, dataset, headers = None):    
    """Dataset Keys are ID"""
    mheaders = sorted(dataset.values()[0].keys())
    if headers is None:
        headers = mheaders
    else:
        mheaders = [ header for header in mheaders if header not in headers  ]
        headers = list(headers)
        headers.extend(mheaders)
    data = {}
    for key, dictionary in dataset.items():
        if len(key)==0:
            continue
        for column, values in dictionary.items():            
            if column not in data:
                data[column] = []
            for value in values:
                data[column].append(value)
    write_xls_from_dictionary(fname,sheet,data,headers)

def write_xls_from_dataset1(fname, sheet, dataset, headers = None ):
    dataset1 = {}
    for key, dictz in dataset.items():
        if key not in dataset1:
            dataset1[key] = {}
        for column, value in dictz.items():
            if column not in dataset1[key]:
                dataset1[key][column] = {}
            dataset1[key][column] = [ value, ]
    write_xls_from_dataset(fname, sheet, dataset1, headers )

