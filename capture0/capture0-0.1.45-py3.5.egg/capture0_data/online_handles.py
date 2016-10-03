import csv
import functools
import logging
import pprint
from typing import Set, Optional

from capture0_data.utils import csv_lines

HANDLES_URL = "https://docs.google.com/spreadsheets/d/103yky1HqNULD2awB4aZvzazSO8i-aVONWVa5C66XzBo/pub?gid=0&single=true&output=csv"

log = logging.getLogger(__name__)


class IndexCompany(object):
    def __init__(self, company: str, display_name: Optional[str], official_name: Optional[str],
                 handles: Optional[Set[str]]):
        self.company = company
        self.display_name = display_name
        self.handles = handles
        self.official_name = official_name

    @staticmethod
    def split_keywords(keyword_string: str) -> Set[str]:
        keywords = [k.strip() for k in keyword_string.split(";")]

        return {k for k in keywords if k}

    @classmethod
    def build_from_row(cls, row):
        handle_columns = {v for k, v in row.items() if (v and "twitter" in k.lower())}
        handles = {h.strip().lstrip("@") for hc in handle_columns for h in hc.split(" ")}
        return cls(
            company=row["company"],
            official_name=row["official_name"],
            display_name=row["display_name"],
            handles=handles
        )

    def __str__(self)->str:
        return "Company: {display_name} ({official_name})".format(**self.__dict__)

    def __repr__(self)->str:
        return "<%s.%s %s" % (self.__class__.__module__, self.__class__.__name__, str(self))





@functools.lru_cache(1)
def get_companies():
    log.warn("Cache has expired... fetching companies.")
    return list(get_companies_generator())



def get_companies_generator():
    reader = csv.DictReader(csv_lines(HANDLES_URL))
    for row in reader:
        yield (IndexCompany.build_from_row(row))


if __name__ == "__main__":
    import sys
    print(sys.version)
    for c in get_companies():
        pprint.pprint(c)

