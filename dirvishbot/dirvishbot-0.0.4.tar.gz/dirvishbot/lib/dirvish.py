# -*- coding: utf-8 -*-

import os
import re
import logging

from glob import glob

DIRVISH_RUNNING = -1
DIRVISH_SUCCESS = 0
DIRVISH_ERROR = 1

logger = logging.getLogger(__name__)

# install
# config ändern (token setzen)
# systemctl start dirvishbot


class Dirvish:
    """
    Class to collect information of your backups based on your dirvish master.conf.
    """
    def __init__(self, masterconf_path='/etc/dirvish/master.conf'):
        """
        :param str masterconf_path: Path to your dirvish master.conf
        """
        if not os.path.isfile(masterconf_path):
            message = 'Failed to open dirvish master.conf file: "%s". \n\nSeems that dirvish is not installed on your system?' % masterconf_path
            logger.fatal(message)
            raise IOError(message)
        self._masterconf_path = masterconf_path
        self._banks = {}

    def refresh(self):
        """
        Reinit self._banks with all contents.

        :return:
        """
        self.init_banks()
        self.init_vaults()
        self.init_backups()

    def get(self):
        """
        :return dict:
        """
        return self._banks

    def init_banks(self):
        """
        Get all banks from master.conf and saves it to self._banks.

        :return:
        """
        logger.debug("Load banks from master.conf")
        bank_start = re.compile("^bank:$")
        bank_stop = re.compile(".*:$")
        start = False
        with open(self._masterconf_path, 'r') as f:
            for line in f:
                if bank_start.match(line):
                    start = True
                    continue
                if bank_stop.match(line):
                    break
                if start:
                    current_bank = line.strip()
                    if len(current_bank) > 0:
                        if os.path.isdir(current_bank):
                            self._banks[current_bank] = []

    def init_vaults(self):
        """
        Get all vaults based on a bank and assign it to the bank in self._banks.

        :return:
        """
        logger.debug("Load vaults from banks")
        for bank in self._banks.keys():
            vaults = glob('%s/*' % bank)
            if '%s/lost+found' % bank in vaults:
                del vaults[vaults.index('%s/lost+found' % bank)]
            for vault in vaults:
                self._banks[bank].append({'path': vault})

    def init_backups(self):
        """
        Get all Backups based on a vault and assign it to the vault in self._banks.

        :return:
        """
        try:
            logger.debug("Load backups from vaults")
            backup_regex = re.compile('^Backup-complete:.*')
            status_regex = re.compile('^Status: success.*')
            expire_regex = re.compile('^Expire: .* == (.*) .*\n$')
            for bank, vaults in self._banks.items():
                for vault in vaults:
                    vault['backups'] = {}
                    backups = glob('%s/*' % vault['path'])
                    if '%s/dirvish' % vault['path'] in backups:
                        del backups[backups.index('%s/dirvish' % vault['path'])]
                    for backup in backups:
                        summary = '%s/summary' % backup
                        vault['backups'][backup] = {}
                        vault['backups'][backup]['status'] = DIRVISH_ERROR
                        if os.path.isfile(summary):
                            with open(summary, 'r') as summary_file:
                                content = summary_file.readlines()
                                if filter(backup_regex.match, content):
                                    if filter(status_regex.match, content):
                                        vault['backups'][backup]['status'] = DIRVISH_SUCCESS
                                else:
                                    vault['backups'][backup]['status'] = DIRVISH_RUNNING
                                expire = list(filter(expire_regex.match, content))
                                if len(expire) > 0:
                                    vault['backups'][backup]['expires'] = expire_regex.match(expire[0]).group(1)
        except Exception as e:
            logger.error('Failed to get backups.', exc_info=True)
