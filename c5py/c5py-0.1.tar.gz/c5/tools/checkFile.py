fpath = '/home/alex/C5/vol_studies/2011-12_ARBaseline/20111215_1330/BRIX_s1_2011-12-15 13:34:29.932287.log'
nr = 0
with open(fpath) as f:
  for line in f.readlines():
    print nr
    if nr > 0:
      line = line.replace(':',',')
      line_array = line.split(',')
      for i in line_array:
        x = int(i)
    nr += 1

