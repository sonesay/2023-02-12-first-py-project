from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests


class APIBrightcove:
    def __init__(self, account_id, client_id, client_secret, access_token=None):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = 'https://cms.api.brightcove.com/v1'

        self.client = BackendApplicationClient(client_id=self.client_id)
        self.oauth_session = OAuth2Session(client=self.client)

    def authorize(self):
        token_url = 'https://oauth.brightcove.com/v4/access_token'

        token = self.oauth_session.fetch_token(token_url, auth=(self.client_id, self.client_secret))

        self.access_token = token['access_token']

    def get_video(self, video_id):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(f'{self.base_url}/accounts/{self.account_id}/videos/{video_id}', headers=headers)
        return response.json()

    def get_video_sources(self, video_id):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(f'{self.base_url}/accounts/{self.account_id}/videos/{video_id}/sources',
                                headers=headers)
        return response.json()
