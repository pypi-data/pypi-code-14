class CellsCorrectPlugin(object):
    '''
    are all the cells in the correct order?
    '''
    def __init__(self):
        self.is_notebook_cell_order_correct = {}

    def parse_notebook(self, filename, notebook):
        if 'cells' not in notebook:
            # we don't handle v3 for now
            # there is no way to see execution count
            return
        cells = notebook['cells']
        self.is_notebook_cell_order_correct[filename] = True
        # what if the notebook is previously versioned v4 vs v3
        execution_cells = [cell for cell in cells if cell['cell_type'] == 'code']
        for index, cell in enumerate(execution_cells, start=1):
            if index != cell['execution_count']:
                self.is_notebook_cell_order_correct[filename] = False
                return

    def summary(self):
        correct = sum(self.is_notebook_cell_order_correct.values())
        total = len(self.is_notebook_cell_order_correct)

        print('Notebooks With Cells In Correct Order: %s / %s' % (correct, total))
        # for (filename, correct) in self.is_notebook_cell_order_correct.items():
        #     print('\t%s : %s' %(correct, filename))
