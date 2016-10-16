def lol (nested_list):
  for a in nested_list:
    if isinstance(a, list) == True:
      lol(a)
    else:
      print(a)
