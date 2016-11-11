#!/usr/bin/env python

"""
Deploy components to production

Usage:
  deployer deploy [<component>...] [--conf=FILE] [--version-file=FILE]
  deployer -h | --help
  deployer --version

Options:
  -h --help              Show this screen.
  --version              Show version.
  --conf=FILE            Configuration file location [default: deployer.ini]
  --version-file=FILE    Deployment version def file [default: DEPLOY.txt]

"""

import sys

from docopt import docopt

from . import conf, deploy


def cli():
    print("This script will deploy everything to production for you")
    arguments = docopt(__doc__, version='1.0')

    explicit = arguments.get('<component>', [])
    version_file = arguments['--version-file']
    conf_file = arguments['--conf']

    deployer = deploy.Deployer(conf_file)
    deployments = deployer.configure()

    with open(version_file) as f:
        deployments = conf.get_deployments_from_versions(f, deployments)

    if explicit:
        deploy_seq = []
        for e in explicit:
            try:
                deploy_seq.append(deployments[e])
            except KeyError:
                print("Explicitly want to deploy {0}, but "
                      "not included in {1}".format(e, version_file))
                sys.exit(1)
    else:
        deploy_seq = deployments.values()

    if arguments['deploy']:
        deployer.deploy(deploy_seq)


if __name__ == '__main__':
    cli()
