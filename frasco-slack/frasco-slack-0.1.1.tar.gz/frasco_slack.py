from frasco import Feature, flash, url_for, lazy_translate, Blueprint, redirect, request, abort, signal, current_app
from frasco_users import current_user
from frasco_models import transaction
import requests
import json


def create_blueprint(app):
    bp = Blueprint("slack", __name__)

    feature = app.features.slack
    users = app.features.users

    @bp.route('/slack/authorize')
    def login():
        callback_url = url_for('.login_callback', next=request.args.get('next'), _external=True)
        return feature.api.authorize(callback=callback_url)

    @bp.route('/slack/authorize/callback')
    def login_callback():
        resp = feature.api.authorized_response()
        if resp is None:
            flash(feature.options["user_denied_login_message"], "error")
            return redirect(url_for("users.login"))

        with transaction():
            users.current.slack_access_token = resp['access_token']
            users.current.slack_team_name = resp['team_name']
            users.current.slack_team_id = resp['team_id']
            if 'incoming_webhook' in resp:
                users.current.slack_incoming_webhook_url = resp['incoming_webhook']['url']
                users.current.slack_incoming_webhook_channel = resp['incoming_webhook']['channel']

        return redirect(request.args.get('next') or feature.options['default_redirect'])

    @bp.route('/slack/command', methods=['POST'])
    def command_callback():
        r = feature.command_received_signal.send(feature,
            token=request.form.get('token'),
            team_id=request.form['team_id'],
            team_domain=request.form.get('team_domain'),
            channel_id=request.form.get('channel_id'),
            channel_name=request.form.get('channel_name'),
            user_id=request.form.get('user_id'),
            user_name=request.form.get('user_name'),
            command=request.form.get('command'),
            text=request.form['text'],
            response_url=request.form.get('response_url'))
        if len(r) > 0 and r[0][1]:
            data = r[0][1]
            if not isinstance(data, (str, unicode)):
                return json.dumps(data), {"Content-Type": "application/json"}
            return data
        return ""

    return bp


class SlackFeature(Feature):
    name = "slack"
    requires = ["users"]
    blueprints = [create_blueprint]
    defaults = {"scope": "incoming-webhook,commands",
                "user_denied_login_message": lazy_translate("Slack authorization was denied"),
                "default_redirect": "index",
                "use_user_model": True}

    command_received_signal = signal('slack_command_received')

    def init_app(self, app):
        self.app = app
        self.api = app.features.users.create_oauth_app("slack",
            base_url='https://slack.com/api/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://slack.com/api/oauth.access',
            authorize_url='https://slack.com/oauth/authorize',
            consumer_key=self.options["client_id"],
            consumer_secret=self.options["client_secret"],
            request_token_params={'scope': self.options['scope']},
            access_token_params={'client_id': self.options['client_id']})

        if self.options['use_user_model']:
            self.model = app.features.models.ensure_model(app.features.users.model,
                slack_access_token=str,
                slack_incoming_webhook_url=str,
                slack_incoming_webhook_channel=str,
                slack_team_name=str,
                slack_team_id=dict(type=str, index=True))

    def post_message(self, incoming_webhook_url, text, attachments=None, channel=None):
        data = {"text": text}
        if attachments:
            data['attachments'] = attachments
        for key in ("username", "icon_url", "icon_emoji"):
            if key in self.options:
                data[key] = self.options[key]
        if channel:
            data["channel"] = channel
        return requests.post(incoming_webhook_url, json=data)

    def respond_to_command(self, response_url, text, attachments=None, response_type=None):
        return requests.post(response_url, json=self.format_command_response(text, attachments, response_type))

    def format_command_response(self, text, attachments=None, response_type=None):
        data = {"text": text}
        if attachments:
            data['attachments'] = attachments
        if response_type:
            data["response_type"] = response_type
        return data

    def parse_command(self, text, subcommand=True):
        command = None
        args = []
        cur = 0
        while cur < len(text):
            if text[cur:cur+1] == '"':
                next_cur = text.find('"', cur+1)
                if next_cur == -1:
                    next_cur = None
                next = text[cur+1:next_cur]
            else:
                next_cur = text.find(' ', cur)
                if next_cur == -1:
                    next_cur = None
                next = text[cur:next_cur]
            if subcommand and command is None:
                command = next
            else:
                args.append(next)
            if next_cur is None:
                break
            cur = next_cur + 1
        return (command, args)