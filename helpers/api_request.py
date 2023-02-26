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

    def create_arc_story(self, content):
        end_point = "https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story"
        content_json = json.dumps(content, default=lambda o: o.__dict__)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text

    def save_arc_image(self, arc_id, image_url):
        data = {
            "additional_properties": {
                "originalUrl": image_url,
                "keywords": [
                    "migration"
                ],
            },
        }
        image = Image(arc_id, data)
        end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/photo/api/v2/photos/{image.get_id()}'
        content_json = json.dumps(image, default=lambda o: o.__dict__)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text

    def delete_arc_image(self, image_id):
        end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/photo/api/v2/photos/{image_id}'
        response = requests.delete(end_point, headers=self.headers, verify=True)
        return response.text

    def delete_arc_story(self, arc_id):
        end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story/{arc_id}'
        response = requests.delete(end_point, headers=self.headers, verify=True)
        return response.text

    def get_arc_video(self, arc_id):
        end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/api/v1/ansvideos/{arc_id}'
        response = requests.get(end_point, headers=self.headers, verify=True)
        return response.text

    def create_arc_video(self, content):
        end_point = "https://api.sandbox.whakaatamaori.arcpublishing.com/goldfish/video/v2/import/ans?encode=true"
        content_json = json.dumps(content, default=lambda o: o.__dict__)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text

    def delete_arc_video(self, arc_id):
        end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/video/{arc_id}'
        response = requests.delete(end_point, headers=self.headers, verify=True)
        return response.text

    def get_migration_test_images(self):
        end_point = f'https://api.sandbox.whakaatamaori.arcpublishing.com/photo/api/v2/photos?keywords=migration'
        response = requests.get(end_point, headers=self.headers, verify=True)
        return response.text
