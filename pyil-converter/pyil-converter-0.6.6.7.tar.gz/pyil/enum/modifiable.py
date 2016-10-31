import pickle as _pickle

def write_to_binary(obj, file):
    """using pickle.dump to convert to binary file.
    If you want to change the method, do:
    write_to_binary=your_function
    make sure your the order of the parameter of your function
    is same as this one."""
    _pickle.dump(obj, file)


def read_binary_file(file):
    """Uses pickle.load() to extract the string from
    the binary file, use read_binary=your_function to
    modify it. It will accept 1 parameter which the
    file object it's going to get the information."""
    return _pickle.load(file)

def divide(l:list, interval:int=4):
    """Yield successive n-sized chunks from l. If you
    modify it, please make sure it receives the same
    arguments in the same order and return a list or
    generator."""
    for i in range(0, len(l), interval):
        yield l[i:i + interval]

