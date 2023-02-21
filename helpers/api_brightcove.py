from oauthlib.oauth2 import WebApplicationClient
import requests
import urllib.parse


class APIBrightcove:
    def __init__(self, client_id, client_secret, access_token=None, redirect_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = 'https://cms.api.brightcove.com/v1'
        self.redirect_uri = redirect_uri or 'urn:ietf:wg:oauth:2.0:oob'

        self.client = WebApplicationClient(self.client_id)

    def authorize(self):
        authorization_url, state = self.client.prepare_authorization_request(
            'https://oauth.brightcove.com/v4/auth', redirect_uri=self.redirect_uri)

        # Redirect the user to the authorization URL
        # After the user grants permission, they will be redirected back to the redirect URI with an authorization code
        response = requests.get(authorization_url)

        # Extract the authorization code from the redirect URI
        code = self.extract_authorization_code(response.url)

        # Exchange the authorization code for an access token
        token_url = 'https://oauth.brightcove.com/v4/access_token'
        self.client.prepare_token_request(token_url=token_url, authorization_response=response.url,
                                          redirect_uri=self.redirect_uri)
        token_response = self.client.send_token_request(token_url, auth=(self.client_id, self.client_secret),
                                                        redirect_uri=self.redirect_uri)

        self.access_token = token_response['access_token']

    def extract_authorization_code(self, url):
        # Extract the query parameters from the URL
        query_params = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)

        # Extract the authorization code from the query parameters
        return query_params.get('code', [None])[0]

    def get_video(self, video_id):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(f'{self.base_url}/accounts/{self.client_id}/videos/{video_id}', headers=headers)
        return response.json()
