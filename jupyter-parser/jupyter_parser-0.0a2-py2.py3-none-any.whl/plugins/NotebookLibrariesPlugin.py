# import click

import re
from collections import Counter
# import matplotlib.pyplot as plt


class NotebookLibrariesPlugin(object):
    '''
    what libraries are found in the notebooks?
    '''
    def __init__(self):
        self.libraries_in_notebook = {}

    def parse_notebook(self, filename, notebook):
        if 'cells' not in notebook:
            # we don't handle v3 for now
            return
        # this pattern has gotten weaker from original
        pattern = r'^(?:from|import)\s+([\w.]*)\s+'
        cells = notebook['cells']
        execution_cells = [cell for cell in cells if cell['cell_type'] == 'code']
        modules = []
        for cell in execution_cells:
            # determine if any libraries have been used w/ regular expressions
            source = cell['source']
            source = ''.join(source)
            modules += re.findall(pattern, source)

        self.libraries_in_notebook[filename] = modules

    def summary(self):
        libraries_across_notebooks = []
        for (filename, libraries) in self.libraries_in_notebook.items():
            # print('\t%s : %s' %(libraries, filename))
            libraries_across_notebooks += libraries

        library_counter = Counter(libraries_across_notebooks)
        print('Overall Library Usage: %s' % (library_counter))
        # command line input
        # wants_histogram = click.prompt('would you like a histogram displayed of the top X libraries',
        #     type = bool, default = False)
        #
        # if not wants_histogram:
        #     return
        # num_libraries = click.prompt('how many libraries would you like to display?',
        #     type = int, default = 5)
        #
        # library_count_tuple_list = library_counter.most_common(num_libraries)
        # libraries = [library for library, _ in library_count_tuple_list]
        # counts = [count for _, count in library_count_tuple_list]
        #
        # x = range(len(libraries))
        # y = counts
        #
        # f = plt.figure()
        # ax = f.add_axes([0.1, 0.1, 0.8, 0.8])
        # ax.bar(x, y, align='center')
        # ax.set_xticks(x)
        # ax.set_xticklabels(libraries)
        # f.show()
