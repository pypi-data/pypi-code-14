from __future__ import division

from . import settings
from . import utils
from datetime import datetime

import click
import enum
import os
import requests
import time


class InvalidAppKeyError(Exception):
    """SDK enabled application app key was invalid."""


class InvalidCustomerKeyError(Exception):
    """Provided customer auth key was invalid."""


EXTENSION_TO_PLATFORM = {
    'apk': 'android',
    'ipa': 'ios'
}


def filename_to_platform(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lstrip('.')

    if ext not in EXTENSION_TO_PLATFORM.keys():
        raise ValueError("Unrecognized file extension: {}".format(ext))

    return EXTENSION_TO_PLATFORM[ext], ext


AIS_SETTINGS = {
    'report_on_shake': "true",
    'mach_exceptions': "false",
    'with_utest': "false",
    'screenshots_from_gallery': "false",
    'patch_bundle_name': "false",
    'sign_only': "false",
    'instrument_only': "true",
}


class ProcessingState(enum.Enum):
    """
    Valid build processing state for AIS service.
    """
    pending = 'pending'
    success = 'success'
    error = 'error'


class ApplauseAIS(object):
    """
    Applause AIS API wrapper.
    """
    # Naming scheme for instrumentation output files.
    DEFAULT_OUTPUT_FILE = 'instrumented-app-{date}.{extension}'

    # Max number of times instrumentation process will poll for results.
    MAX_STATUS_CHECKS = 30

    # Delay before each status check
    STATUS_CHECK_DELAY = 2

    # File download chunk size
    FILE_CHUNK_SIZE = 1024 * 1024

    def __init__(self, session, customer_key):
        self.session = session
        self.customer_key = customer_key
        self.platform = None
        self.output = None

    def instrument(self, input_path, app_key, output_path):
        self.platform, extension = filename_to_platform(input_path)
        self.output = output_path or self.DEFAULT_OUTPUT_FILE.format(
            date=datetime.now().isoformat(),
            extension=extension)

        # Combined with is not supported on Python 2.6
        with open(input_path, 'rb') as input_file:
            with open(self.output, 'wb') as output_file:
                return self.process(input_file, app_key, output_file)

    def process(self, *args, **kwargs):
        try:
            return self.run_instrument(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise InvalidCustomerKeyError()
            raise

    def run_instrument(self, input_file, app_key, output_file):
        """
        Runs input file through the SDK injection service (AIS).
        """
        click.echo("Starting SDK injection process...")
        click.echo("Submitting file...")

        build_url, _ = self.upload(input_file)

        click.echo("Scheduling injection task...")
        token, _ = self.schedule(app_key, self.platform, build_url)

        click.echo("Waiting for results...", nl=False)
        for status, data in self.poll_status(token, max_tries=self.MAX_STATUS_CHECKS):
            click.echo(".", nl=False)
            time.sleep(self.STATUS_CHECK_DELAY)

        click.echo("")

        if status == ProcessingState.pending.name:
            click.echo("Service is too busy to process your request. Please try at later time.")
            return

        if status == ProcessingState.error.name:
            click.echo("Instrumentation failed: {}".format(data))
            return

        if 'title' in data:
            click.echo(data['title'])
        else:
            click.echo("Instrumentation finished!")

        click.echo("Downloading file...")

        resource_url = data['processed_url']
        for _ in utils.download(resource_url, output_file, chunk_size=self.FILE_CHUNK_SIZE):
            click.echo('.', nl=False)

        click.echo("")
        return self.output

    def _get_upload_data(self):
        """
        Returns payload needed to push file to AIS servers.
        """
        response = self.session.get(settings.AIS_UPLOAD_DATA_URL, params={'apikey': self.customer_key})
        response.raise_for_status()
        return response.json()

    def upload(self, input_file):
        """
        Uploads build for AIS processing.
        """
        upload_data = self._get_upload_data()

        # Post to a generated storage url (temporary access token included). self.session must not be used.
        storage_response = requests.post(
            upload_data['action'],
            upload_data['fields'],
            files={'file': input_file},
            stream=True
        )

        storage_response.raise_for_status()
        return upload_data['upload_url'], upload_data

    def schedule(self, app_key, platform, build_url):
        """
        Schedules build file processing.
        """
        form_data = {
            # Must be publicly available, we have a special upload / hosting service if you need to use one.
            'app_url': build_url,
            'platform': platform,
            'app_key': app_key,
            'server_url': settings.MBM_ROOT_URL.rstrip('/'),
        }

        form_data.update(AIS_SETTINGS)

        response = self.session.post(settings.AIS_INSTRUMENT_URL, data=form_data, params={'apikey': self.customer_key})

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise InvalidAppKeyError(e.response.json())
            raise

        data = response.json()
        return data['token'], data

    def get_status(self, token):
        status_url = settings.urljoin(settings.AIS_STATUS_URL, token)
        response = self.session.get(status_url, params={'apikey': self.customer_key})
        response.raise_for_status()

        data = response.json()
        return data['status'], data

    def poll_status(self, token, max_tries=1):
        while max_tries > 0:
            max_tries -= 1

            status, data = self.get_status(token)
            yield status, data

            if status in [ProcessingState.success.name, ProcessingState.error.name]:
                break
