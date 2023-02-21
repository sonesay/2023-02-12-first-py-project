from oauthlib.oauth2 import BackendApplicationClient
import requests


class APIBrightcove:
    def __init__(self, client_id, client_secret, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = 'https://cms.api.brightcove.com/v1'

        self.client = BackendApplicationClient(client_id=self.client_id)

    def authorize(self):
        token_url = 'https://oauth.brightcove.com/v4/access_token'

        self.client.prepare_request_body()
        token_response = requests.post(token_url, auth=(self.client_id, self.client_secret),
                                       data=self.client.oauth2session.token)

        self.access_token = token_response.json()['access_token']

    def get_video(self, video_id):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(f'{self.base_url}/accounts/{self.client_id}/videos/{video_id}', headers=headers)
        return response.json()
