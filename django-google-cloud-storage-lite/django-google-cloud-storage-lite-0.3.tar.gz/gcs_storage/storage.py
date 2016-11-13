from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.conf import settings
from google.cloud import storage


class GoogleCloudStorage(Storage):
    def __init__(self):
        bucket = settings.GOOGLE_CLOUD_STORAGE_BUCKET
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket)
        self.base_url = "https://storage.googleapis.com/%s" % bucket

    def _open(self, name, mode):
        blob = self.bucket.get_blob(name)
        return ContentFile(blob.download_as_string())

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        blob.upload_from_file(content)

    def delete(self, name):
        self.bucket.delete_blob(name)

    def url(self, name):
        return self.base_url + "/" + name

    def exists(self, name):
        return self.bucket.exists()
