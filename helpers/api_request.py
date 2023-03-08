import json
import requests
import os
from dotenv import load_dotenv

from models.image import Image


class APIRequest:
    def __init__(self):
        load_dotenv()  # load the .env file
        self.api_key = os.environ.get('API_KEY')
        self.api_host = os.environ.get('API_HOST')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def delete_arc_story(self, arc_id):
        end_point = f'{self.api_host}/draft/v1/story/{arc_id}'
        response = requests.delete(end_point, headers=self.headers, verify=True)
        return response.text

    def get_arc_story(self, arc_story_id):
        end_point = f'{self.api_host}/draft/v1/story/{arc_story_id}'
        response = requests.get(end_point, headers=self.headers, verify=True)
        return response.text

    def create_arc_story(self, content):
        end_point = f'{self.api_host}/draft/v1/story'
        content_json = json.dumps(content, default=lambda o: o.__dict__)
        # content_json = json.dumps(content)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        response_text = response.text
        print(f"Creating Arc Story response: {response_text}")
        return response.text

    def create_arc_image(self, arc_id, image_url):
        data = {
            "additional_properties": {
                "originalUrl": image_url,
                "keywords": [
                    "migration"
                ],
            },
        }
        image = Image(arc_id, data)
        end_point = f'{self.api_host}/photo/api/v2/photos/{image.get_id()}'
        content_json = json.dumps(image, default=lambda o: o.__dict__)
        try:
            response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
            response_json = response.json()
            if "error" in response_json:
                if response_json["error"] == "Conflict":
                    if response_json.get("errorKey") == "CREATE_PHOTO_WITH_ID_ALREADY_EXISTS":
                        print(f" CREATE IMAGE::: Error: {response_json['message']}")
                else:
                    print(f" CREATE IMAGE::: Error: {response_json['message']}")
            else:
                print(" CREATE IMAGE::: Success:")
            return response.text
        except requests.exceptions.RequestException as e:
            error_message = e.response.json().get('message', 'Unknown error occurred')
            invalid_ids = e.response.json().get('invalid_ids')
            if invalid_ids:
                print(f" CREATE IMAGE::: Error: Invalid IDs: {invalid_ids}")
            print(f" CREATE IMAGE::: Error: {error_message}")
        return response.text

    def delete_arc_image(self, image_id):
        end_point = f'{self.api_host}/photo/api/v2/photos/{image_id}'
        response = requests.delete(end_point, headers=self.headers, verify=True)
        return response.text

    def get_arc_video(self, arc_id):
        end_point = f'{self.api_host}/api/v1/ansvideos/{arc_id}'
        response = requests.get(end_point, headers=self.headers, verify=True)
        return response.text

    def create_arc_video(self, content):
        end_point = f"{self.api_host}/goldfish/video/v2/import/ans?encode=true"
        content_json = json.dumps(content, default=lambda o: o.__dict__)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text

    def create_arc_author(self, content):
        end_point = f'{self.api_host}/author/v2/author-service'
        content_json = json.dumps(content, default=lambda o: o.__dict__)
        response = requests.post(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text

    def create_arc_circulation(self, arc_story_id, content):
        website = os.environ.get('CANONICAL_WEBSITE')
        end_point = f'{self.api_host}/draft/v1/story/{arc_story_id}/circulation/{website}'
        content_json = json.dumps(content, default=lambda o: o.__dict__)
        response = requests.put(end_point, headers=self.headers, data=content_json, verify=True)
        return response.text

    def delete_arc_video(self, arc_id):
        end_point = f'{self.api_host}/draft/v1/video/{arc_id}'
        response = requests.delete(end_point, headers=self.headers, verify=True)
        return response.text

    def get_migration_test_images(self):
        end_point = f'{self.api_host}/photo/api/v2/photos?keywords=migration'
        response = requests.get(end_point, headers=self.headers, verify=True)
        return response.text

    def get_migration_test_stories(self):
        end_point = f"{self.api_host}/content/v4/search"
        params = {
            "website": "teaomaori",
            "q": 'type:"story" AND source.system:"Drupal"',
            "_sourceInclude": "_id"
        }
        response = requests.get(end_point, headers=self.headers, params=params, verify=True)
        return response.text

    def get_site_sections(self):
        end_point = f'{self.api_host}/site/v3/navigation/teaomaori'
        response = requests.get(end_point, headers=self.headers, verify=True)
        return response.text
