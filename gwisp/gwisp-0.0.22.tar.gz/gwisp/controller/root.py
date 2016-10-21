import pkg_resources


class RootCtl(object):
    '''
    Information of service. Read only resource
    '''

    def __init__(self):
        pass

    def on_get(self, req, res):
        '''
        Response: Essential information of service
        '''

        data = {
            'name': 'gwisp service',
            'notes': 'http programing interface of scheduler storage',
            'version': pkg_resources.get_distribution('gwisp').version,
            'source': 'https://github.com/kevin-leptons/gwisp',
            'pip': 'https://pypi.python.org/pypi/gwisp/0.0.4',
            'document_url': 'http://gwisp.readthedocs.io/en/latest/'
        }

        res.body = data
