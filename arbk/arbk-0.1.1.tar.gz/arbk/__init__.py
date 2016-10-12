from string import ascii_lowercase
from functools import wraps
from . import urls, download, parse

def arbk(*search_terms):
    '''
    Download and parse data from Agjensioni i regjistrimit te bizneseve
    në Kosovë.

    :param search_terms: Terms to search for, defaults to all ASCII
        lowercase letters
    '''
    if not search_terms:
        search_terms = ascii_lowercase

    done = set()
    for search_term in search_terms:
        pages, _ = parse.search(download.search(search_term, 0))
        for page in pages:
            _, businesses = parse.search(download.search(search_term, page))
            for business in businesses:
                if business not in done:
                    r = download.business(business)
                    row = parse.business(r)
                    row['URL'] = r.url

                    yield row
                    done.add(business)

FIELDNAMES = [
    'URL',

    'Emri i biznesit',
    '*KTA_CertificateNumber',
    'Adresa',
    'Aktivitet/et',
    'Data e aplikimit',
    'Data e konstituimit',
    'Kapitali',
    'Lloji i biznesit',
    'Numri fiskal',
    'Numri i puntorëve',
    'Numri i regjistrimit',
    'Persona fizik',
    'Pronarë',
    'Statusi në ATK',
    'Telefoni',
    'Web',
    'E-mail',
    'Drejtor',
    'Statusi i biznesit',
]

@wraps(arbk)
def _arbk_csv(*search_terms):
    import csv, sys
    w = csv.DictWriter(sys.stdout, fieldnames=FIELDNAMES)
    w.writeheader()
    w.writerows(arbk(*search_terms))
    sys.stdout.close()

def cli():
    import horetu
    horetu.cli({
        'convert-url': urls.business_from_ajax,
        'scrape': _arbk_csv,
    })
