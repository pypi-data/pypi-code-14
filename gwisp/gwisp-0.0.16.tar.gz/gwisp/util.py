class Selector(object):
    '''
    Contains informations which is use to search item from resource

    :param keyword: string:
        Search item which is match with keyword
    :type keyword: string
    :param page_index:
        Index of page, start from 1
    :type page_index: int
    :param page_size:
        Max items in one page
    :type page_size: int
    '''
    def __init__(self, keyword=None, page_index=1, page_size=16):
        self.keyword = keyword          #: Get and set keyword
        self.page_index = page_index    #: Get and set page_index
        self.page_size = page_size      #: Get and set page_size

    @property
    def skip(self):
        '''
        :return: Number of item to skip to start of first item to get
        :rtype: int
        '''
        return (self.page_index - 1) * self.page_size


def parse_selector(req):
    '''
    Parse request and return selector. If parameters is not specify in url,
    set it to default

    :param falcon.Request req: Falcon request object
    :return: Instance of selector
    :rtype: gwisp.Selector
    '''

    selector = Selector()

    if 'keyword' in req.params:
        selector.keyword = req.params['keyword']
    if 'page_size' in req.params:
        selector.page_size = req.params['page_size']
    if 'page_index' in req.params:
        selector.page_index = req.params['page_index']

    return selector


class AuthInfo(object):
    '''
    Contains authenticating and account information after authenticate

    :param bson.objectid.ObjectId acc_id: Identity of account
    :param dict token: Token attribute
    :param dict acc: Account attribute
    '''

    def __init__(self, acc_id, token, acc=None):
        self._account_id = acc_id
        self._token = token
        self._account = acc

    @property
    def account_id(self):
        '''
        :return: Account identity
        :rtype: bson.objectid.ObjectId
        '''
        return self._account_id

    @property
    def token(self):
        '''
        :return: Token attribute
        :rtype: dict
        '''
        return self._token

    @property
    def account(self):
        '''
        :return: Account attribute
        :rtype: dict
        '''
        return self._account
