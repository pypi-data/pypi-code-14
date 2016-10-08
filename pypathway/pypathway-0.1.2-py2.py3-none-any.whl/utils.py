# Common Objects
# We define the Visualize Attribute, Interactive Event, Interactive Option and Visualization Option here


def environment():
    '''
    To identify the current environment, a IPython notebook environment or a command-line environment
    We highly recommend you use a IPython notebook with the package
    :return:
    '''
    try:
        env = __IPYTHON__
        return 1
    except NameError:
        return 0


class IDNotFoundInPathwayTree(Exception):
    def __init__(self):
        pass


class PathwayDataInstanceContainNoValidDataException(Exception):
    def __init__(self):
        pass


class FormatNotFoundINPathwayDataInstanceException(Exception):
    def __init__(self):
        pass


class PaxtoolExecuteException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class GPMLCorrespondeNodeNotFound(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class OptionProcessException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class SBGNParseException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)