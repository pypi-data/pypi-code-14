import sys
import csv

def clear(filename):
    """Clear the CSV file."""
    try:
        with open(filename, 'w+'):
            pass
    except FileNotFoundError as e:
        sys.exit('%s. Make sure that the .csv file is in the same folder.' % e)
        
def count_rows(filename):
    """Return the number of rows present in the CSV file, 0 if none."""
    return len(get_rows(filename))

def print_rows(filename):
    """Print all the rows contained in the CSV file."""
    rows = get_rows(filename)
    for row in rows:
        print(row)

def get_rows(filename):
    """Return a list containing all the rows of the CSV file."""
    rows = []
    try:
        with open(filename, 'rt') as f:
            try:
                reader = csv.reader(f)
                rows = list(reader)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    except FileNotFoundError as e:
        sys.exit('%s. Make sure that the .csv file is in the same folder.' % e)
    return rows

def get_row(filename, row_index):
    """Return the row at row_index, from zero-index."""
    return get_rows(filename)[row_index]

def get_row_value(filename, row_index, value_index):
    """Return the value at value_index from the row at row_index, from zero-index."""
    return get_row(filename, row_index)[value_index]
    
def get_row_values(filename, row_index, values_indexes):
    """Return the values at value_indexes from the row at row_index, from zero-index."""
    row = get_row(filename, row_index)
    values = []
    for i in values_indexes:
        values.append(row[i])
    return values

def get_rows_value(filename, value_index):
    """Return all the values at value_index from each row, from zero-index."""
    values = []
    for row in get_rows(filename):
        values.append(row[value_index])
    return values        

def get_rows_with_value(filename, value_index, value_target):
    """Return a list containing all the rows that have value_target at value_index, from zero-index."""
    rows = []
    for row in get_rows(filename):
        if row[value_index] == value_target:
            rows.append(row)
    return rows

def get_rows_with_values(filename, targets):
    """Return a list of lists, each containing the rows that match the targets, from zero-index.
    targets: [ [value1_index, value1_target], [value2_index, value2_target], ... ]
    output: [ [rows with value1 ], [rows with value2], ... ]
    """
    rows_with_values = []                                           # initialise parent list    
    n = len(targets)
    for i in range(0, n):
        rows_with_values.append([])                                 # initialise children lists      
    for row in get_rows(filename):
        for i in range(0, n):                                       # check row for all targets
            if row[targets[i][0]] == targets[i][1]:
                rows_with_values[i].append(row)                     # add row to child list                
    return rows_with_values 
        
def append_row(filename, row):
    """Append a row at the end of CSV file."""
    try:
        with open(filename, 'a', newline='') as f:
            try:
                writer = csv.writer(f)
                writer.writerow(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, writer.line_num, e))
    except FileNotFoundError as e:
        sys.exit()
        
def write_row(filename, row):
    """Clear the CSV file and write a single row."""
    try:
        with open(filename, 'w', newline='') as f:
            try:
                writer = csv.writer(f)
                writer.writerow(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, writer.line_num, e))
    except FileNotFoundError as e:
        sys.exit()        
        
def overwrite_row(filename, row_index, new_row):
    """Overwrite the row at row_index with the new_row, from zero-index."""
    rows = get_rows(filename)
    try:
        rows[row_index] = new_row
        clear(filename)
        for row in rows:
            append_row(filename, row)
    except IndexError as e:
        sys.exit('file %s: %s' % (filename, e))