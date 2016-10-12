import vlermv, requests
from . import urls

@vlermv.Vlermv.memoize('~/.arbk/business')
def business(id):
    return requests.get(urls.business(id))

@vlermv.Vlermv.memoize('~/.arbk/search')
def search(search_term, page):
    return requests.get(urls.search(search_term, page))
