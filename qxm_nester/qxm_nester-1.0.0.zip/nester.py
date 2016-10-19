def function(para):
    for obj in para:
        if isinstance(obj, list):
            function(obj)
        else:
            print(obj)
