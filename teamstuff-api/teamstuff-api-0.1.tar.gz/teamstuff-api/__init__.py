import pprint
import requests
import delorean

class APIInstance:

    def __init__(self):
        self.request_login_handle = None
        self.teamstuff_context = None
        self.teamstuff_login_data = None
        self.request_headers = dict()
        self.request_headers['Content-Type'] = "application/json"
        self.request_headers['Accept'] = "application/vnd.teamstuff.com.v12+json, application/json"
        self.request_headers['X-Requested-With'] = "XMLHttpRequest"
        self.request_headers['X-Teamstuff-Timezone'] = "Europe/London"
        self.request_headers['Accept-Encoding'] = "gzip, deflate, br"

    def login(self, api_username, api_password):
        login_url = 'https://coachstuff.com/data/sessions'
        payload_dict = dict()
        payload_dict['email'] = api_username
        payload_dict['password'] = api_password
        payload_dict['remember_me'] = True
        payload_dict['birthday'] = None
        payload_dict['out_of_action_start_date'] = None
        payload_dict['out_of_action_end_date'] = None

        self.request_login_handle = requests.Session()
        login_request = self.request_login_handle.post(login_url, headers=self.request_headers,
                                                                   json=payload_dict)
        self.teamstuff_login_data = login_request.json()
        teamstuff_context_request = self.request_login_handle.get('https://coachstuff.com/data/context',
                                                                  headers=self.request_headers)
        self.teamstuff_context = teamstuff_context_request.json()

    def get_training_sessions(self, season, team):
        sessions_params = {'season_id':season, 'team_id':team, 'member_id': self.teamstuff_login_data['id']}

        training_sessions_request = self.request_login_handle.get('https://coachstuff.com/data/trainings',
                                                         params=sessions_params, headers = self.request_headers)
        return training_sessions_request.json()['trainings']

    def get_training_plan(self, season, team, training_session):
        sessions_params = {'season_id':season, 'team_id':team, 'member_id': self.teamstuff_login_data['id'],                 'event_id': training_session}

        training_notes_request = self.request_login_handle.get('https://coachstuff.com/data/coach-notes',
                                                         params=sessions_params, headers = self.request_headers)
        pprint.pprint(training_notes_request.json())

        training_plan_request = self.request_login_handle.get('https://coachstuff.com/data/events/%s/event-plan' %
                                                               training_session, headers=self.request_headers)
        return training_plan_request.json()
