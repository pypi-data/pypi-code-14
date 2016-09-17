
from .entity import Entities, Entity

import json

class Leads(Entities):

    def get(self, phone_number):
        lead = self.get_contact(phone_number)
    
        if 'company_id' in lead:
            comp_id = lead['company_id']
            company = self.get_company(comp_id)

            if 'latest_ads' in company:
                ids = list(company['latest_ads'].keys())
                ads = self.get_ads(ids)
                latest_ads = {}
                for ad_id, ad in ads.items():
                    latest_ads[ad_id] = Entity(ad)
                company['latest_ads'] = latest_ads

            lead['company'] = Entity(company)

        if 'last_ad_id' in lead:
            ad_id = lead['last_ad_id']
            ad = self.get_ad(ad_id)
            lead['last_ad'] = Entity(ad)

        return Entity(lead)

    def get_v2(self, phone_number):
        lead = self.get_contact_by_id(phone_number)
        return Entity(lead)
