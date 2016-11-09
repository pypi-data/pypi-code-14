import pandas as pd
import numpy as np
import random
df1 = pd.read_csv('test.csv')
print(df1)
print(df1.dtypes)

import feather
feather.write_dataframe(df1, "a.df")
