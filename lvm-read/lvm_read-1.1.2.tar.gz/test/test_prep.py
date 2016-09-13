import numpy as np
from lvm_read import read

#data = read('../data/short_new_line_end.lvm', read_from_pickle=False)
data = read('../data/with_empty_fields.lvm', read_from_pickle=False)
#data = read('../data/multi_time_column.lvm', read_from_pickle=False)
print(data)