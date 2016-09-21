def why_v1(a1):
    for t1 in a1:
        if isinstance(t1,list):
           why_v1(t1)
        else:
           print(t1)
