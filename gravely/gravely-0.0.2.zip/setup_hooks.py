def numpy_include(cmd):
    '''Add numpy include dir for all extensions, see setup.cfg'''
    import numpy
    for extension in cmd.extensions:
        extension.include_dirs.append(numpy.get_include())
