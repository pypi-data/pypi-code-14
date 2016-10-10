def modulocator(module_dir):
    """Finds the a specified dir in the current working dir and appends to the system path.
    """
    import os,sys
    nb_dir = os.path.split(os.getcwd())[0]
    for i in range(len(nb_dir.split("\\"))):
        if module_dir in nb_dir.split("\\")[i]:
            real_nb_dir = "\\".join(nb_dir.split("\\")[:i+1])
    if nb_dir not in sys.path:
        sys.path.append(real_nb_dir)
