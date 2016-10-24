import requests as R
import base64
import sys
import json
import copy

class TogglApi:


    #TODO : exception handling and input validation for the interfaces of this class
    #named params {api_token, btype{project || workspace}, bid}
    def __init__(self, **params):
        if(params.get('api_token')):
            self.set_account(params.get('api_token'))
        self.set_business(params)
        self.current = None
        self.str_btype = None
        self.time_entry_template = {"time_entry":{
                                "description":None,
                                "tags":[],
                                "created_with" : "gouravs_cli_pytool"
                             }
                          }

    def set_business(self, params):
        self.bid = params.get("bid")
        if(params.get("btype") == "project"):
            self.btype = "pid"
        if(params.get("btype") == "workspace"):
            self.btype = "wid"

    def set_account(self, api_token):
        token  = api_token + ':api_token'
        self.auth_header = base64.b64encode(token.encode('ascii'))
        self.HEADERS = {
                "Content-Type": "application/json",
                "Authorization": "Basic " + self.auth_header.decode('ascii')
            }




    def start(self, description):
        url = 'https://www.toggl.com/api/v8/time_entries/start'
        data = copy.deepcopy(self.time_entry_template);
        data["time_entry"]["description"] = description
        data["time_entry"][self.btype] = self.bid
        new_time_entry = R.post(url,data=json.dumps(data), headers=self.HEADERS)
        self.current = new_time_entry.json().get('data')
        return new_time_entry

    def get_current(self):
        url = 'https://www.toggl.com/api/v8/time_entries/current'
        running_time = R.get(url, headers=self.HEADERS)
        self.current = running_time.json().get('data')
        return running_time

    def stop(self):
        self.get_current()
        if(self.current == None):
            return print("Nothing to stop")
        time_entry_id = self.current.get('id')
        if(time_entry_id > 0):
            url = 'https://www.toggl.com/api/v8/time_entries/'+str(time_entry_id)   +'/stop'
            entry = R.put(url, headers=self.HEADERS)
            return entry.json().get('data').get('id')
