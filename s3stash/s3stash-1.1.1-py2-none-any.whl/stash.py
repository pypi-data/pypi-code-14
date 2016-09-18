# pylint: disable=missing-docstring

from datetime import date
from hashlib import sha1
from io import BytesIO

from s3stash.util import make_date_prefix, make_s3_client


def make_key(content):
    """Make an S3 key string.

    Format:
        YYYY/MM-Month/DD/<sha1 hash of contents>

    Example:
        2016/09-September/15/a97bf80abf4e78560e0f153088f3686680d10f56

    """
    hsh = sha1(content).hexdigest()
    return make_date_prefix(date.today()) + hsh


class Stash(object):
    """Simple S3 file stash.

    credentials: an orgtup.AwsCredentials object

    bucket: name of an S3 bucket

    s3_client: used in unit tests to mock the S3 API

    """
    def __init__(self, credentials, bucket, s3_client=None):
        self.credentials = credentials
        self.bucket = bucket
        self.s3_client = s3_client or make_s3_client(credentials)
        self.make_key = make_key

    def stash_string(self, content):
        """Upload content as a string."""
        key = self.make_key(content)

        with BytesIO(content) as bfile:
            self.s3_client.upload_fileobj(bfile, self.bucket, key)
