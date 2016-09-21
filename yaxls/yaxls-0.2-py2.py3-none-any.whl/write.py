import xlwt


def fill_sheet_from_matrix(ws, matrix, justify = True, styles = None):
    transpose = zip(*matrix)
    for c,col in enumerate(transpose):
        maxlen = 0
        for r,cell in enumerate(col):            
            value = cell
            if isinstance(cell,(tuple,list)):
                if cell[0]==0:
                    value = cell[1]
                    style = cell[2]
                elif cell[0]==1:
                    value = cell[1].value
                    style = cell[1].xf_index
                ws.write(r, c, value, styles[style])
            else:
                ws.write(r, c, value)
            maxlen = max(maxlen,len(unicode(value)))
        ws.col(c).width = 256 * (maxlen + 2) 
    return ws

def add_sheet_from_matrix(wb, sheet_name, matrix, justify = True, styles = None):
    ws = wb.add_sheet(sheet_name)    
    ws = fill_sheet_from_matrix(ws,matrix, justify, styles)
    return ws

def write_xls_from_matrix(fname, sheet_name, matrix, justify=True, styles = None):
    wb = xlwt.Workbook()
    ws = add_sheet_from_matrix(wb,sheet_name,matrix, justify, styles)
    wb.save(fname)

def write_xls_from_dictionary(fname, sheet_name, dictionary, headers = None, justify=True, styles = None):
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
    write_xls_from_matrix(fname, sheet_name, matrix, justify, styles)
    return matrix

    
def write_xls_from_dataframe(fname, sheet, keyname, headers, multiline=0):
    pass

def write_xls_from_dataset(fname, sheet, dataset, headers = None, justify=True, styles = None):    
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
    write_xls_from_dictionary(fname,sheet,data,headers, justify, styles)

def write_xls_from_dataset1(fname, sheet, dataset, headers = None, justify=True, styles = None):
    dataset1 = {}
    for key, dictz in dataset.items():
        if key not in dataset1:
            dataset1[key] = {}
        for column, value in dictz.items():
            if column not in dataset1[key]:
                dataset1[key][column] = {}
            dataset1[key][column] = [ value, ]
    write_xls_from_dataset(fname, sheet, dataset1, headers, justify, styles )

