import json
import requests
import os
from dotenv import load_dotenv

from models.image import Image


class APIRequest:
    def __init__(self):
        load_dotenv()  # load the .env file
        self.api_key = os.environ.get('API_KEY')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
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

    def post_to_arc_image_endpoint(self, image_url):
        data = {
            "_id": "3GQNRROHMRH6PAFU63PT5APMEE",
            "address": {},
            # "auth": {
            #     "1": "6b31b88c572402432785896dfc8445408be2fd97b40de9a0961069a80620438a"
            # },
            # "created_date": "2023-02-16T06:27:48Z",
            # "credits": {
            #     "affiliation": []
            # },
            # "height": 1024,
            # "image_type": "photograph",
            # "last_updated_date": "2023-02-16T06:27:48Z",
            # "licensable": False,
            # "owner": {
            #     "id": "sandbox.whakaatamaori",
            #     "sponsored": False
            # },
            # "source": {
            #     "additional_properties": {
            #         "editor": "photo center"
            #     },
            #     "edit_url": "https://sandbox.whakaatamaori.arcpublishing.com/photo/3GQNRROHMRH6PAFU63PT5APMEM",
            #     "system": "photo center"
            # },
            "subtitle": "HEADLINE (IPTC RECORD IN ARC) 2",
            # "taxonomy": {
            #     "associated_tasks": []
            # },
            "type": "image",
            "url": image_url,
            "version": "0.10.3",
            # "width": 1024,
            # "syndication": {}
        }
        image = Image(image_url, data)
        end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/photo/api/v2/photos'
        content_json = json.dumps(image, default=lambda o: o.__dict__)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text
