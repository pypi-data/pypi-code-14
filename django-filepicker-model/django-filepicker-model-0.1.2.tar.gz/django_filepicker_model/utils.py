import mimetypes, json, requests, base64, hmac, hashlib, time

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from filepicker import FilepickerClient, FilepickerFile

try:
    EXPIRES_IN_SECONDS = settings.FILEPICKER_EXPIRES_IN_SECONDS
except:
    EXPIRES_IN_SECONDS = 60*60

EXPIRY = int(time.time() + EXPIRES_IN_SECONDS)


class CustomFPClient(FilepickerClient):
    def store_from_upload_file(self, file, filename, storage=None, policy_name=None, **kwargs):
        mimetype = mimetypes.guess_type(filename)
        files = {'fileUpload': (filename, file.read(), mimetype)}
        params = {}
        if policy_name:
            params.update(self.policies[policy_name].signature_params())
        if kwargs:
            params.update(kwargs)
        return self.__post(storage, files=files, params=params)

    def __post(self, storage, data=None, files=None, params=None):
        storage = storage or self.storage
        post_url = '{}/store/{}'.format(self.API_URL, storage)
        params['key'] = self.api_key

        response = requests.post(post_url, data=data, files=files,
                                 params=params, headers=self.HEADERS)
        try:
            response_dict = json.loads(response.text)
            return FilepickerFile(response_dict=response_dict,
                                  api_key=self.api_key,
                                  app_secret=self.app_secret,
                                  policies=self.policies)
        except ValueError:
            return response.raise_for_status()

def store_from_upload_file(file):
    client = CustomFPClient(api_key=settings.FILEPICKER_API_KEY, app_secret=settings.FILEPICKER_APP_SECRET)
    expiry = str(EXPIRY)
    client.add_policy(name='allow_storing',
                      policy={
                               'call': 'store',
                               'expiry': expiry
                              })

    response = client.store_from_upload_file(file, file.name, policy_name='allow_storing')
    if isinstance(response, FilepickerFile):
        return '{0}{1}'.format(response.FILE_API_URL, response.handle)
    return response

def store_from_url(url):
    client = CustomFPClient(api_key=settings.FILEPICKER_API_KEY, app_secret=settings.FILEPICKER_APP_SECRET)
    expiry = str(EXPIRY)
    client.add_policy(name='allow_storing',
                      policy={
                               'call': 'store',
                               'expiry': expiry
                              })

    response = client.store_from_url(url, policy_name='allow_storing')
    if isinstance(response, FilepickerFile):
        return '{0}{1}'.format(response.FILE_API_URL, response.handle)
    return response
