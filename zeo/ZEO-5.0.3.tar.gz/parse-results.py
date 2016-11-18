import sys
import collections
ops = 'add update cached read prefetch'.split()
data = collections.defaultdict(list)
for l in sys.stdin:
    l = l.strip().split()
    if l and l[0] in ops:
        if len(l) == 2:
            data[l[0]].append(l[1])
        else:
            assert len(l) == 5
            data[l[0]].append(l[2])

for op in ops:
    if op in data:
        print(op, *data[op])
