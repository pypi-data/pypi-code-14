from glob2 import glob
import re

def epr_recursive_import(path):
    paths = glob(path + '/**/*.py')

    for path in paths:
        with open(path, 'r+') as f:
            content = f.read()
            match = re.search(r'\bepr\(', content)
            if match:
                f.seek(0, 0)
                f.write('from epr import epr\n' + content)
