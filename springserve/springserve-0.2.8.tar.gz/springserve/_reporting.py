
from . import _VDAPIService, _VDAPIResponse, _VDAPIMultiResponse

from datetime import datetime

import pandas

class _ReportingResponse(_VDAPIMultiResponse):
    
    def to_dataframe(self):
        return pandas.DataFrame(self.raw)

class _ReportingAPI(_VDAPIService):

    __API__ = "report"
    __RESPONSES_OBJECT__ = _ReportingResponse
    
    INTERVALS = ("hour", "day", "cumulative")

    def _format_date(self, date):
        
        if isinstance(date, datetime):
            return date.strftime("%Y-%m-%d")
        return date
    
    def run(self, start_date=None, end_date=None, interval=None, dimensions=None,
            account_id=None, **kwargs):
        """
        parameter     options (if applicable)  notes
        ===================================================
        start_date:  "2015-12-01 00:00:00" or "2015-12-01"    
        end_date:    "2015-12-02 00:00:00" or "2015-12-01"    
        interval:    "hour", "day", "cumulative"  
        timezone:    "UTC", "America/New_York"   defaults to America/New_York
        date_range:  Today, Yesterday, Last 7 Days   date_range takes precedence over start_date/end_date
        dimensions:  supply_tag_id, demand_tag_id, detected_domain, declared_domain, demand_type, supply_type, supply_partner_id, demand_partner_id, supply_group  domain is only available when using date_range of Today, Yesterday, or Last 7 Days

        the following parameters act as filters; pass an array of values (usually IDs)
        =================================================================================

        supply_tag_ids:  [22423,22375, 25463]
        demand_tag_ids:  [22423,22375, 25463]     
        detected_domains:         ["nytimes.com", "weather.com"]   
        declared_domains:         ["nytimes.com", "weather.com"]   
        supply_types     ["Syndicated","Third-Party"]     
        supply_partner_ids:  [30,42,41]   
        supply_group_ids:    [13,15,81]   
        demand_partner_ids:  [3,10,81]    
        demand_types:    ["Vast Only","FLASH"]    
        """
        payload = {
            'start_date': self._format_date(start_date),
            'end_date': self._format_date(end_date),
        }

        if interval:
            if interval not in self.INTERVALS:
                raise Exception("not a valid interval")
            payload['interval'] = interval

        if dimensions:
            payload['dimensions'] = dimensions

        if account_id:
            payload['account_id'] = account_id
        
        if kwargs:
            payload.update(kwargs)

        return self.post(data=payload)


class _TrafficQualityReport(_ReportingAPI):

    __API__ = "traffic_quality_reports"
    __RESPONSES_OBJECT__ = _ReportingResponse
    


