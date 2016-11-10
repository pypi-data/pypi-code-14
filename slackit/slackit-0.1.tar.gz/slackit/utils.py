import json
import os
import requests
import sys


class Slack(object):
    SETTINGS_FILE_NAME = '.slackit'
    API_TOKEN = None

    def create_settings_file(self):
        name = None
        while not (self.API_TOKEN or name):
            self.API_TOKEN = raw_input('Enter your Slack API Token (see https://api.slack.com/docs/oauth-test-tokens): ').strip()
            name = raw_input('Enter your Slack name: ').strip().replace('@', '')

        user_id = self.get_user_id(name)

        with open(self.SETTINGS_FILE_NAME, 'w+') as f:
            f.write(json.dumps(dict(
                SLACK_API_TOKEN=self.API_TOKEN,
                SLACK_USER_ID=user_id,
            )))
            print('Slackit config file written to ./{}'.format(f.name))

    def load_config(self):
        wd_path = self.SETTINGS_FILE_NAME
        home_path = os.path.join(os.path.expanduser('~'), self.SETTINGS_FILE_NAME)
        if os.path.isfile(wd_path):
            path = wd_path
        elif os.path.isfile(home_path):
            path = home_path
        else:
            print('Config file not found.  Please create one with `slackit --init`')
            sys.exit(1)

        with open(path) as f:
            config = json.loads(f.read())
            self.API_TOKEN = config['SLACK_API_TOKEN']
            self.USER_ID = config['SLACK_USER_ID']

    def get_user_id(self, name):
        response = requests.get(
            'https://slack.com/api/users.list',
            params=dict(
                token=self.API_TOKEN,
            )
        )
        r = response.json()
        for member in r['members']:
            if member['name'] == name:
                return member['id']
        raise Exception('Name {} not found in user list'.format(name))

    def get_user_channel_id(self):
        response = requests.get(
            'https://slack.com/api/im.open',
            params=dict(
                token=self.API_TOKEN,
                user=self.USER_ID
            )
        )
        r = response.json()
        if not r['ok']:
            print(r)
        else:
            return response.json()['channel']['id']

    def write_to_channel(self, channel_id, message):
        for chunk in chunks(message, n=4000):
            # send a direct message to the user with the test results
            requests.post(
                'https://slack.com/api/chat.postMessage',
                data=dict(
                    token=self.API_TOKEN,
                    channel=channel_id,
                    text="```{}```".format(chunk),
                    mrkdwn=True,
                )
            )


def chunks(l, n=25):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
