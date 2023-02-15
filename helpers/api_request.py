import json
import requests


class APIRequest:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def delete_arc_story(self, news_article):
        if news_article.arc_id is not None:
            end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story/{news_article.arc_id}'
            response = requests.delete(end_point, headers=self.headers, verify=True)
            return response.text
        else:
            # Handle the case where arc_id is None
            return False

    def post_to_arc_migration_content(self, end_point, content):
        content_json = json.dumps(content, default=lambda o: o.__dict__)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text
