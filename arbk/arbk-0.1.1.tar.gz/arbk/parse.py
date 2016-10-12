import os
import lxml.html
from urllib.parse import urlsplit, parse_qs

def _html(response):
    return lxml.html.fromstring(response.content.decode('utf-8'))

def _page(url):
    return int(parse_qs(urlsplit(url).query)['page_b'][0])

def search(response):
    html = _html(response)

    page_hrefs = html.xpath('//div[@class="pagination"]//@href')
    if page_hrefs:
        pages = range(_page(page_hrefs[0]), _page(page_hrefs[-1]))
    else:
        pages = []

    xpath = '//div[@class="Business_table box-24-expand"]/table//@href'
    businesses = (os.path.basename(urlsplit(url).path) \
                  for url in html.xpath(xpath))
    return pages, businesses

def business(response):
    html = _html(response)
    data = dict((td.text_content().strip() for td in tr.xpath('td')) \
                 for tr in html.xpath('//tr[td]'))
    data['Emri i biznesit'] = html.xpath('//th/text()')[0].strip()
    return data
