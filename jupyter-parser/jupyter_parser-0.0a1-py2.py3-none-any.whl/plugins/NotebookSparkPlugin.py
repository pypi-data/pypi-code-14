import re


class NotebookSparkPlugin(object):
    '''
    is the notebook using a spark context, etc.
    '''

    # variables commonly used in spark notebooks
    # sc must match alone or used with .

    spark_variables = [
        'pyspark',
        # \b also matches on punctuation
        '\\bsc\\b',
        'spark',
        'sqlContext',
        'sqlCtx',
        'SQLContext',
        'SparkContext',
        'SparkSession'
    ]

    # TODO: cleanup
    def __init__(self):
        self.is_spark_notebook = {}

    def parse_notebook(self, filename, notebook):
        if 'cells' not in notebook:
            # we don't handle v3 for now
            # there is no way to see execution count
            return

        self.is_spark_notebook[filename] = False

        # update to with word boundary
        pattern = '|'.join(NotebookSparkPlugin.spark_variables)

        cells = notebook['cells']
        execution_cells = [cell for cell in cells if cell['cell_type'] == 'code']
        for cell in execution_cells:
            source = cell['source']
            source = ''.join(source)
            if re.search(pattern, source):
                self.is_spark_notebook[filename] = True

    def summary(self):
        spark_notebooks = sum(self.is_spark_notebook.values())
        total_notebooks = len(self.is_spark_notebook)

        print('Spark Notebooks: %s / %s' % (spark_notebooks, total_notebooks))
        # for (filename, is_spark) in self.is_spark_notebook.items():
        #     print('\t%s : %s' %(filename, is_spark))
