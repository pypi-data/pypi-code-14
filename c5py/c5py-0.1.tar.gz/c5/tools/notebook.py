import io
import nbformat

def execute_notebook(nbfile):
    with io.open(nbfile, encoding='utf-8') as f:
        nb = nbformat.read(f, nbformat.current_nbformat)
    ip = get_ipython()
    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        ip.run_cell(cell.source)