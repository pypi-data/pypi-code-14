import ZEO

for i in range(5000):
  print(i)
  a, s = ZEO.server(threaded=False)
  c = ZEO.connection(a)
  c.close()
  s()
