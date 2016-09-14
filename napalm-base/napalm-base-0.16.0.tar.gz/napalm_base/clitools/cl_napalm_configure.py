# -*- coding: utf-8 -*-
'''
NAPALM CLI Tools: configure
===========================

Deploy device config from the shell.
'''

from __future__ import print_function

import sys

import logging
logger = logging.getLogger('cl-napalm-config.py')

# import helpers
from napalm_base.clitools.helpers import build_help
from napalm_base.clitools.helpers import configure_logging
from napalm_base.clitools.helpers import parse_optional_args


def run(vendor, hostname, user, password, strategy, optional_args, config_file, dry_run):

    logger.debug('Getting driver for OS "{driver}"'.format(driver=vendor))
    driver = get_network_driver(vendor)

    optional_args = parse_optional_args(optional_args)

    logger.debug('Connecting to device "{device}" with user "{user}" and optional_args={optional_args}'.format(
                    device=hostname, user=user, optional_args=optional_args))
    with driver(hostname, user, password, optional_args=optional_args) as device:
        logger.debug('Strategy for loading configuration is "{strategy}"'.format(strategy=strategy))
        if strategy == 'replace':
            strategy_method = device.load_replace_candidate
        elif strategy == 'merge':
            strategy_method = device.load_merge_candidate

        logger.debug('Loading configuration file "{config}"'.format(config=config_file))
        strategy_method(filename=config_file)

        logger.debug('Comparing configuration')
        diff = device.compare_config()

        if dry_run:
            logger.debug('Dry-run. Discarding configuration.')
        else:
            logger.debug('Committing configuration')
            device.commit_config()
        logger.debug('Closing session')

        return diff


def main():
    args = build_help()
    configure_logging(logger, args.debug)

    print(run(args.vendor, args.hostname, args.user, args.password, args.strategy,
              args.optional_args, args.config_file, args.dry_run))
    sys.exit(0)


if __name__ == '__main__':
    main()
