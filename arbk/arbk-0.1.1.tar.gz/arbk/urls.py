from urllib.parse import urlsplit, parse_qs

def business(id, search='hotdog'):
    '''
    Get a business url from a business id.
    '''
    return 'http://arbk.org/sq/Rezultatet-e-Bizneseve/' + id + '?part=business_list&code=%2020,0,url_b%20plotesohet%20ne%20ajax%20%20,0,0,' + search + ',0,0,0,0'

def business_from_ajax(url):
    '''
    Convert the thing in the AJAX response
    (http://arbk.org/sq/Rezultatet-e-Bizneseve/71018482?part=business_list&code=%2020,0,url_b%20plotesohet%20ne%20ajax%20%20,0,0,h,0,0,0,0)
    to the thing that you see in when the thing is rendered
    (http://arbk.org/sq/Rezultatet-e-Bizneseve/71018482?nb=0&eb=h&la=0&lp=0&main_acitivity=0&other_acitivity=0&page_b=0).

    :param url: The url in the AJAX response
    :returns: The url that you should download
    '''
    s = urlsplit(url)
    id = os.path.basename(s.path)
    search = parse_qs(s.query)['eb'][0]
    return 'http://arbk.org/sq/Rezultatet-e-Bizneseve/' + id + '?part=business_list&code=%2020,0,url_b%20plotesohet%20ne%20ajax%20%20,0,0,' + search + ',0,0,0,0'

def search(search_term, page):
    '''
    :param int page: Page number, starting at zero
    '''
    args = {
        'search_term': search_term,
        'page': page,
    }
    return ('http://arbk.org/sq/Rezultatet-e-Bizneseve?part=business_list&code= 20,0,url_b plotesohet ne ajax  ,%(page)d,0,%(search_term)s,0,0,0,0' % args).replace(' ', '%20')
