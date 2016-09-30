import datetime
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from .settings import CLIENT_ID, CLIENT_SECRET
from .models import BibblioIDMap
from .importer import process_record

TOKEN_URL = "https://api.bibblio.org/token"


class BibblioAPI(object):
    """
    BibblioAPI
    """
    def __init__(self):
        self.client = BackendApplicationClient(client_id=CLIENT_ID)
        self.oauth = OAuth2Session(client=self.client)
        self._token = None

    @property
    def _token_is_expired(self):
        if self._token is None:
            return True
        expires_at = datetime.datetime.fromtimestamp(self._token['expires_at'])
        return datetime.datetime.now() > expires_at

    @property
    def token(self):
        if self._token is None or self._token_is_expired:
            data = {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            }
            self._token = self.oauth.fetch_token(TOKEN_URL, **data)

        return self._token

    def content_items(self, limit=10, page=1):
        data = {'limit': limit, 'page': page}
        bibblio = OAuth2Session(client_id=CLIENT_ID, token=self.token)
        response = bibblio.get("https://api.bibblio.org/content-items", params=data)
        response.raise_for_status()
        return response.json()

    def create_content_item(self, content_item):
        data = content_item.as_json()
        bibblio = OAuth2Session(client_id=CLIENT_ID, token=self.token)
        response = bibblio.post("https://api.bibblio.org/content-items", data=data)
        response.raise_for_status()

        response_dict = response.json()
        content_item.contentItemId = response_dict['contentItemId']
        if content_item.adapter is not None:
            bibblio_id_map = BibblioIDMap.objects.create(
                bibblio_id=response_dict['contentItemId'],
                content_type=content_item.adapter._content_type,
                object_id=content_item.adapter._pk)
            process_record(response_dict, bibblio_id_map)
        return content_item

    def get_content_item(self, content_item_id):
        bibblio = OAuth2Session(client_id=CLIENT_ID, token=self.token)
        response = bibblio.get("https://api.bibblio.org/content-items/%s" % content_item_id)
        response.raise_for_status()
        return response.json()
        # return ContentItem(**response.json())

    def update_content_item(self, content_item):
        data = content_item.as_json()
        bibblio = OAuth2Session(client_id=CLIENT_ID, token=self.token)
        response = bibblio.delete("https://api.bibblio.org/content-items", data=data)
        response.raise_for_status()

        response_dict = response.json()
        content_item.contentItemId = response_dict['contentItemId']
        if content_item.adapter is not None:
            bibblio_id_map = BibblioIDMap.objects.get(bibblio_id=response_dict['contentItemId'])
            process_record(response_dict, bibblio_id_map)
        return content_item

    def delete_content_item(self, content_item_id):
        bibblio = OAuth2Session(client_id=CLIENT_ID, token=self.token)
        response = bibblio.delete("https://api.bibblio.org/content-items/%s" % content_item_id)
        response.raise_for_status()
        try:
            BibblioIDMap.objects.get(bibblio_id=content_item_id).delete()
        except:
            pass

    def get_content_item_recommendations(self, content_item_id, limit=5, page=1, fields=None):
        """
        If fields=None, use all fields
        """
        bibblio = OAuth2Session(client_id=CLIENT_ID, token=self.token)
        url = "https://api.bibblio.org/content-items/%s/recommendations" % content_item_id
        params = {
            'limit': limit,
            'page': page,
        }
        if fields is not None:
            params['fields'] = fields
        response = bibblio.get(url, params=params)
        response.raise_for_status()
        return response.json()
