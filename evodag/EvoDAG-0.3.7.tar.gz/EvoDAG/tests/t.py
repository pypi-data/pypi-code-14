import sys
from test_root import X, cl
import gzip
import json
import numpy as np
from EvoDAG.command_line import params
np.seterr(all='raise')


fname = 'train.json.gz'
with gzip.open(fname, 'wb') as fpt:
    for x, y in zip(X, cl):
        a = {k: v for k, v in enumerate(x)}
        a['klass'] = int(y)
        a['num_terms'] = len(x)
        try:
            fpt.write(bytes(json.dumps(a) + '\n', encoding='utf-8'))
        except TypeError:
            fpt.write(json.dumps(a) + '\n')

sys.argv = ['EvoDAG', '-C', '-Poutput.evodag', '--json',
            '--multiple-outputs', '-r10', fname]
params()
