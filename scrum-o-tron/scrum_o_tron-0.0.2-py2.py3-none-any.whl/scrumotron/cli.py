""" scrumotron

Slack BOT that implements a very simple standup.

Invite the scrumotron user to a channel.

Commands:

  !standup start - Starts the standup and clears out old standup data.
  !standup message - Adds message to the standup
  !standup - shows the current messaged in the standup

Environment Variables:

  SLACK_BOT_NAME=scrum-o-tron
  SLACK_BOT_TOKEN=xxx

Obtain the name and token from Slack by creating a new bot.
"""

import logging
import os
import time

from slackclient import SlackClient

logging.basicConfig(
    level=logging.DEBUG,
    format='%(relativeCreated)6d %(threadName)s %(message)s'
)
LOG = logging.getLogger()


class NotFoundException(Exception):
    """ Exception for data that cannot be found. """
    pass


class ScrumOTron():
    """ ScrumOTron
    Connects to Slack and waits for messages starting with !standup,
    processes and responds accordingly.
    """

    def __init__(self, name, slack_bot_token):
        self.slack = SlackClient(slack_bot_token)
        self.name = name
        self.user = self.find_user(name)
        LOG.debug("Configured for {} {}".format(self.name, self.user))

        self.exclude_users = [self.user]
        self.standup = []

    def start(self):
        """
            Connect to slack and start listening for messages.
        """
        if self.slack.rtm_connect():
            LOG.debug("Running..")
            while True:
                self.parse_slack_output(
                    self.slack.rtm_read(),
                    self.handle_command
                )
                time.sleep(1)
        else:
            LOG.error("Connection failed. Invalid Slack token or bot ID?")

    def find_user(self, name):
        """ find_user(name)
            Returns user id for the supplied user name.
            Raises NotFoundException if the user name cannot be found.
        """
        users = self.slack.api_call('users.list').get('members')
        for user in users:
            if 'name' in user and user.get('name') == name:
                return user.get('id')
        raise NotFoundException("Cannot find ID for name {}".format(name))

    def handle_command(self, user, channel, message):
        """
            Params: user, channel, message
            Process commands in message
            Sends messages back to the originating channel
        """
        if message.startswith('!standup'):
            user_name = self.slack.api_call('users.info', user=user)['user']['name']
            message = message.split('!standup', 1)[1].strip()
            if message == 'start':
                response = "{} has started the standup.".format(user_name)
                self.standup = [response]
            elif message:
                self.standup.append("{} is {}".format(user_name, message))
                response = "Thanks {}".format(user_name)
            else:
                response = "\n".join(self.standup)

            self.slack.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    def parse_slack_output(self, slack_rtm_output, command_handler):
        """
            Parse messages from slack.
            Exclude messages from self.exclude_users
            Calls command_handler method with (self, user, channel, message)
            Returns True if a message was handled.
        """
        if not slack_rtm_output:
            return
        for output in slack_rtm_output:
            if output and set(output.keys()).issuperset(('user', 'text', 'channel')):
                user = output['user']
                text = output['text'].strip()
                channel = output['channel']
                if user in self.exclude_users:
                    LOG.debug("Excluded {}".format(user))
                    return
                command_handler(user, channel, text)
                return True


def main():
    """
        Obtain config from environment
        Run an instance of ScrumOTron
    """
    name = os.environ.get("SLACK_BOT_NAME")
    if not name:
        raise RuntimeError('SLACK_BOT_NAME')
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise RuntimeError('SLACK_BOT_TOKEN')
    ScrumOTron(name, token).start()

if __name__ == "__main__":
    main()
