"""Command line interface / runner."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()  # NOQA

import sys
import argparse
import json

import requests

from . import jsonshim
from . import lsstsw
from . import jenkinsenv
from .schemas import validate


def run_post_qa():
    """CLI entrypoint for the ``post-qa`` command."""
    args = parse_args()

    job_json = build_job_json(args.qa_json_path, args.lsstsw_dirname)

    upload_json(job_json, api_url=args.api_url,
                api_user=args.api_user, api_password=args.api_password)


def parse_args():
    parser = argparse.ArgumentParser(
        description="""Upload JSON from validate_drp to the SQuaSH API's
job ingest endpoint, usually ``/api/jobs/``.

This script is meant to be run from a Jenkins CI environment
and uses the following environment variables:

- ``BUILD_ID`` : ID in the ci system
- ``BUILD_URL``: ci page with information about the build
- ``PRODUCT``: the name of the product built, in this case 'validate_drp'
- ``dataset``: the name of the dataset processed by validate_drp
- ``label`` : the name of the platform where it runs
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--lsstsw',
        dest='lsstsw_dirname',
        required=True,
        help='Path of lsstsw directory')
    parser.add_argument(
        '--qa-json',
        dest='qa_json_path',
        required=True,
        help='Filename of QA JSON output file')
    parser.add_argument(
        '--api-url',
        dest='api_url',
        required=True,
        help='URL of SQuaSH API endpoint for job submission')
    parser.add_argument(
        '--api-user',
        dest='api_user',
        required=True,
        help='Username for SQuaSH API')
    parser.add_argument(
        '--api-password',
        dest='api_password',
        required=True,
        help='Password for SQuaSH API')
    return parser.parse_args()


def build_job_json(qa_json_path, lsstsw_dirname):
    """Build a json message for SQUASH's /api/jobs endpoint from
    validate_drp-type JSON data.
    """
    # Shim validate_drp's JSON to SQuaSH measurements format
    with open(qa_json_path) as f:
        qa_json = json.load(f, encoding='utf-8')
    job_json = jsonshim.shim_validate_drp(qa_json)

    # Add 'packages' sub-document
    lsstsw_install = lsstsw.Lsstsw(lsstsw_dirname)
    job_json.update(lsstsw_install.json)

    # Add metadata from the CI environment
    jenkins = jenkinsenv.JenkinsEnv()
    job_json.update(jenkins.json)

    # Validate
    validate(job_json)

    return job_json


def upload_json(job_json, api_url, api_user, api_password):
    """Upload Job json document to SQuaSH through POST /api/jobs/ endpoint."""
    r = requests.post(api_url, auth=(api_user, api_password), json=job_json)
    print(r.status_code)
    if r.status_code != 201:
        print(r.json())
        sys.exit(1)
