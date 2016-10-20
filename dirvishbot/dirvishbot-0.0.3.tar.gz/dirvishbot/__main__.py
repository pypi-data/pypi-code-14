#!/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import datetime
import random
import signal
import string

from telegram.bot import Bot
from telegram.ext import Updater, CommandHandler
from telegram.parsemode import ParseMode

from dirvishbot.lib.config import *
from dirvishbot.lib.dirvish import *

logging.basicConfig(filename='/var/log/dirvishbot/dirvishbot.log')
logger = logging.getLogger(__name__)

PID_FILE = "/var/run/dirvishbot.pid"


class DirvishBot:
    """
    The main class of this bot.
    """
    TOKEN_REGEX = re.compile('^/register ([a-zA-Z0-9]{6})$')
    _tokens = {}

    def __init__(self):
        """
        :param str token: The telegram bot api-token.
        """
        logger.debug('Load config ...')
        self._config = Config()
        self._check_first_run()
        self._api_token = self._config.get('api_token')
        if self._api_token is None:
            message = 'Failed to get "api_token" from config "/etc/dirvishbot/config.json".'
            print(message)
            logger.debug(message)
            sys.exit(1)
        self._pid = os.getpid()

        logger.debug('Loading dirvish ...')
        self._dirvish = Dirvish()

        logger.debug('Initialize telegram bot api ...')
        self._updater = Updater(self._api_token)
        self._bot = Bot(self._api_token)

        # Telegram bot routes
        logger.debug('Register commands...')
        self._updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self._updater.dispatcher.add_handler(CommandHandler('register', self.register))
        self._updater.dispatcher.add_handler(CommandHandler('adduser', self.add_user))
        self._updater.dispatcher.add_handler(CommandHandler('subscribe', self.subscribe))
        self._updater.dispatcher.add_handler(CommandHandler('unsubscribe', self.unsubscribe))
        self._updater.dispatcher.add_handler(CommandHandler('status', self.status))

        # Signals
        # Backup finished
        signal.signal(signal.SIGUSR1, self._handle_signal)

        self._write_pid()
        logger.debug('Initialization complete.')

    def _write_pid(self):
        """
        Write PID.

        :return:
        """
        with open(PID_FILE, 'w') as f:
            f.write('%d' % self._pid)

    def _check_first_run(self):
        """
        Checks for the first run to initialize the admin user.

        :return:
        """
        admins = self._config.get('administrators')
        if admins is None or len(admins) == 0:
            token = self._new_token(ttl=3600)
            with open('/etc/dirvishbot/register', 'w') as f:
                f.write("This is your first start of the Bot. \n")
                f.write("Please register your admin-user within the next hour by sending the following to this Bot:\n")
                f.write('    /register %s\n' % token)

    def run(self):
        """
        Start the main loop.

        :return:
        """
        self._updater.start_polling()
        self._updater.idle()

    def stop(self):
        """
        Stop and quit.

        :return:
        """
        logger.debug('Stopping ...')
        self._updater.stop()
        logger.debug('Bye!')

    def _status_to_emoji(self, status):
        """
        Convert status enum to emoji.

        :param int status:
        :return:
        """
        if status == DIRVISH_SUCCESS:
            return '✅'
        elif status == DIRVISH_RUNNING:
            return '❓'
        return '❌'

    def _disk_usage(self, path):
        """
        Get the current disk stats.

        :param path:
        :return:
        """
        statvfs = os.statvfs(path)

        size = float(statvfs.f_frsize * statvfs.f_blocks) / (1024 * 1024 * 1024 * 1024)
        free = float(statvfs.f_frsize * statvfs.f_bavail) / (1024 * 1024 * 1024 * 1024)
        used = size - free

        disk_usage = '\n*Disk stats:*\n'
        disk_usage += '`Used: %.1fG`\n' % round(used, 2)
        disk_usage += '`Free: %.1fG`\n' % round(free, 2)

        return disk_usage

    def _new_token(self, ttl=86400):
        """
        Creates a random token to register a new user.

        :param int ttl: Seconds until the tokem will expire.
        :return str:
        """
        invalidates = datetime.datetime.now() + datetime.timedelta(seconds=ttl)
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self._tokens[token] = invalidates
        return token

    def _handle_signal(self, signum, stack):
        """
        Signalhandler. Notify admins / subscribers about failed backups.

        :param int signum:
        :param stack:
        :return:
        """
        logger.debug('Received signal %d.' % signum)
        if signum == signal.SIGUSR1:
            failed = []
            self._dirvish.refresh()
            for bank, vaults in self._dirvish.get().items():
                for vault in vaults:
                    latest = sorted(vault['backups'], reverse=True)[0]
                    status = vault['backups'][latest]['status']
                    logger.info(status)
                    if status != DIRVISH_SUCCESS:
                        failed.append(latest)
            message = "❌ Failed Backup(s):\n"
            for backup in failed:
                message += "  `%s`\n" % backup

            if len(failed) > 0:
                subscribers = self._config.get('subscribers')
                if subscribers is not None:
                    for subscriber in subscribers:
                        self._bot.sendMessage(chat_id=subscriber, text=message, parse_mode=ParseMode.MARKDOWN)
                else:
                    admins = self._config.get('administrators')
                    if admins is not None:
                        for admin in admins:
                            self._bot.sendMessage(chat_id=admin, text=message, parse_mode=ParseMode.MARKDOWN)

    def is_admin(self, user_id):
        """
        Checks if the user_id is owned by an admin.

        :param int user_id:
        :return bool:
        """
        try:
            admins = self._config.get('administrators')
            if user_id in admins:
                return True
        except:
            pass
        return False

    def is_registered(self, user_id):
        """
        Checks if the user_id is registered.

        :param int user_id:
        :return bool:
        """
        if self.is_admin(user_id):
            return True
        try:
            users = self._config.get('users')
            if user_id in users:
                return True
        except:
            pass
        return False

    def start(self, bot, update):
        message = "*Welcome to the dirvish telegram bot!*\n\n"
        message += "To get status messages or get notified about failed backups you have to register with this bot.\n\n"
        message += "To register you need a token from an administrator and send\n"
        message += "    `/register <TOKEN>`\n\n"
        message += "If you already registered you can enable the notification by sending:\n"
        message += "    `/subscribe`\n\n"
        message += "If you want to disable notification, send the following:\n"
        message += "    `/unsubscribe`\n\n"
        message += "Have a nice day!"
        update.message.reply_text('%s' % message, parse_mode=ParseMode.MARKDOWN)

    def register(self, bot, update):
        """
        Registers a user with his user_id and a given token.

        :param bot:
        :param update:
        :return:
        """
        user_id = update.message.from_user.id
        token = self.TOKEN_REGEX.match(update.message.text)
        if token:
            try:
                token = token.group(1).upper()
                if len(token) > 0 and token in self._tokens:
                    invalidate = self._tokens[token]
                    del self._tokens[token]
                    if datetime.datetime.now() > invalidate:
                        update.message.reply_text('Your token has expired')
                        return

                    admins = self._config.get('administrators')
                    if admins is None:
                        self._config.set('administrators', [user_id])
                        update.message.reply_text('Successfully registered as admin.')
                        return

                    users = self._config.get('users')
                    if users is None:
                        self._config.set('users', [user_id])
                    elif isinstance(users, list):
                        if user_id in users:
                            update.message.reply_text('Already registered!')
                            return
                        users.append(user_id)
                        self._config.set('users', users)
                    update.message.reply_text('Successfully registered.')
                    return
            except Exception as e:
                logger.error('Failed to register user.', exc_info=True)
        update.message.reply_text('Register failed.')

    def add_user(self, bot, update):
        """
        Create a token for a new user. Only callable by admins.

        :param bot:
        :param update:
        :return:
        """
        user_id = update.message.from_user.id
        if self.is_admin(user_id):
            token = self._new_token()
            message = 'Please forward this message to your contact.\n\n'
            message += 'Send the following to @%s within the next 24 hours:\n\n' % bot.getMe()['username']
            message += '/register %s' % token
            update.message.reply_text(message)

    def subscribe(self, bot, update):
        """
        Notify the user of failed backups.

        :param bot:
        :param update:
        :return:
        """
        user_id = update.message.from_user.id
        if self.is_registered(user_id):
            subscribers = self._config.get('subscribers')
            if isinstance(subscribers, list):
                if user_id not in subscribers:
                    subscribers.append(user_id)
                    self._config.set('subscribers', subscribers)
            else:
                self._config.set('subscribers', [user_id])
            update.message.reply_text('Notification enabled.')

    def unsubscribe(self, bot, update):
        """
        Do not notify the user of failed backups.

        :param bot:
        :param update:
        :return:
        """
        user_id = update.message.from_user.id
        if self.is_registered(user_id):
            subscribers = self._config.get('subscribers')
            if isinstance(subscribers, list):
                if user_id in subscribers:
                    del subscribers[subscribers.index(user_id)]
                    self._config.set('subscribers', subscribers)
            update.message.reply_text('Notification disabled.')

    def status(self, bot, update):
        """
        Show the current status of all backups.

        :param bot:
        :param update:
        :return:
        """
        try:
            if self.is_registered(update.message.from_user.id):
                self._dirvish.refresh()
                message = "*Backup status:*\n"
                for bank, vaults in self._dirvish.get().items():
                    message += '  %s/\n' % bank
                    for vault in vaults:
                        vault_name = vault['path'].split('/')[-1]
                        message += '    %s/\n' % vault_name
                        for backup in sorted(vault['backups'], reverse=True):
                            backup_name = backup.split('/')[-1]
                            expires = vault['backups'][backup]['expires']
                            message += '      `%s`: %s\n' % (
                            backup_name, self._status_to_emoji(vault['backups'][backup]['status']))
                            if expires:
                                message += '        `expires: %s`\n' % expires
                    message += self._disk_usage(bank)
                update.message.reply_text('%s' % message, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error('Failed to call /status.', exc_info=True)


def clean():
    """
    Cleanup

    :return:
    """
    if os.path.isfile(PID_FILE):
        os.remove(PID_FILE)


def main():
    atexit.register(clean)
    bot = DirvishBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.stop()


if __name__ == '__main__':
    main()
