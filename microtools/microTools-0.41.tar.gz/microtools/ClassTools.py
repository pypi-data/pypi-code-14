def getVars(obj):
    """
    returns dictionary of all properties from class instance
    :param obj:
    :return:
    """
    dic={}
    for k in dir(obj):
        dic[k]=getattr(obj, k)
    return dic

