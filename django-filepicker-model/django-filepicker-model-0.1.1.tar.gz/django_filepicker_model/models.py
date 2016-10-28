import mimetypes, json, requests, base64, hmac, hashlib, time

from django.conf import settings
from django.utils import timezone
from django.db import models
from django.core.files import File

from filepicker import FilepickerFile

from utils import store_from_upload_file, store_from_url

try:
    EXPIRES_IN_SECONDS = settings.FILEPICKER_EXPIRES_IN_SECONDS
except:
    EXPIRES_IN_SECONDS = 60*60

EXPIRY = int(time.time() + EXPIRES_IN_SECONDS)

class FilepickerField(models.URLField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 2000)
        super(models.URLField, self).__init__(verbose_name, name, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return get_signed_url(value)

    def to_python(self, value):
        return value

class UrlSignature(models.Model):
    file_handle = models.CharField(max_length=255)
    policy = models.CharField(max_length=255)
    signature = models.CharField(max_length=255)
    expires = models.DateTimeField(null=True, blank=True)

class FilepickerModel(models.Model):
    def save(self, *args, **kwargs):
        if not self.id:
            for field in self._meta.fields:
                if isinstance(field, FilepickerField):
                    if self.__getattribute__(field.name):
                        if isinstance(self.__getattribute__(field.name), File):
                            self.__setattr__(field.name, store_from_upload_file(self.__getattribute__(field.name)))
                        else:
                            self.__setattr__(field.name, store_from_url(self.__getattribute__(field.name)))
        super(FilepickerModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

def get_signed_url(url):
    if url is None or url == '':
        return

    now = timezone.now()

    fpfile = FilepickerFile(url=url)
    # remove existing query params
    base_url = fpfile.url.split('?')[0]

    sig = UrlSignature.objects.filter(file_handle=fpfile.handle, expires__gte=now).order_by('-expires').first()
    if sig:
        return '{0}?policy={1}&signature={2}'.format(base_url, sig.policy, sig.signature)

    expiry = str(EXPIRY)
    json_policy = '{"handle":"%s","expiry":%s}' % (fpfile.handle, expiry)

    policy = base64.urlsafe_b64encode(json_policy)
    signature = hmac.new(settings.FILEPICKER_APP_SECRET, policy, hashlib.sha256).hexdigest()

    new_sig = UrlSignature(file_handle=fpfile.handle, policy=policy, signature=signature, expires=now + timezone.timedelta(0, EXPIRES_IN_SECONDS))
    new_sig.save()

    return '{0}?policy={1}&signature={2}'.format(base_url, policy, signature)
