class ContextBean(object):
    name = ""
    object = None  # type: object
    postConstruct = None
    preDestroy = None
    lazy = False