import random
from typing import List

from capture0_data.online_handles import get_companies, IndexCompany


def get_random_company_names() -> List[IndexCompany]:
    raw_companies = get_companies()
    random.shuffle(raw_companies)
    random_companies = raw_companies[:20]

    return random_companies
