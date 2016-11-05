class CollectionIndexError(Exception):
    '''
    Use to raise error if indexes of collection is invalid

    :param str message: Custom message related with error
    '''

    def __init__(self, message):
        self.message = message


class NotExistError(Exception):
    '''
    Use to raise error if resource is not exist

    :param str message: Custom message related with error
    '''

    def __init__(self, message):
        self.message = message


class EarlyExistError(Exception):
    '''
    Use to raise error if resource is early exist, and can not
    create same resource because resource is identitfy

    :param str message: Custom message related with error
    '''

    def __init__(self, message):
        self.message = message


class NotAllowError(Exception):
    '''
    Use to raise error if program perform update identify field of resource

    :param str message: Custom message related with error
    '''

    def __init__(self, message):
        self.message = message


class AuthenticateError(Exception):
    '''
    Use to raise error if program can not authenticate user

    :param str message: Custom message related with error
    '''

    def __init__(self, message):
        self.message = message


class AuthorizeError(Exception):
    '''
    Use to raise error if account have not enough permission to
    perform an operation

    :param str message: Custom message related with error
    '''

    def __init__(self, message):
        self.message = message
