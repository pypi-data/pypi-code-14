import os

def build_path(root_path,category,raw_name,len_=-1):
    if len_ == -1:
        name = raw_name
    else:
        name = "%s.gz"%raw_name

    path = os.path.join(root_path, category.lower(), name.lower())
    return path