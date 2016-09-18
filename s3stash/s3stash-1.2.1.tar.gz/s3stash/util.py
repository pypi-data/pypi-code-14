"""Functions used by the default implementation of the Stash class."""

from boto3 import client


def make_date_prefix(date):
    """Make an S3 key prefix from a date.

    Format a date as:

        YYYY/MM-Month/DD/

    For example:

        2016/09-September/15/

    """
    return date.strftime('%Y/%m-%B/%d/')


def make_s3_client(credentials):
    """Make a client for uploading to S3.

    credentials: an orgtup.AwsCredentials object
    """
    return client(
        's3',
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key)
