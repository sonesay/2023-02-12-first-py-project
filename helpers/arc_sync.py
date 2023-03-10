import json
import sys
from collections import namedtuple

from bs4 import BeautifulSoup
from html2ans.default import Html2Ans
from helpers.api_request import APIRequest
from helpers.arc_sync_story import ArcSyncStory
from helpers.db_conn import DbConn
from models.arc_author_ans import ArcAuthorANS
from models.arc_story_ans import Headlines, ArcStoryANS


class ArcSync:
    def __init__(self):
        self.db_conn = DbConn()
        self.api_request = APIRequest()
        self.arc_sync_story = ArcSyncStory()

    def sync_stories_to_arc(self, test_urls=None):
        # test_urls = None
        cursor = self.db_conn.conn.cursor()
        if test_urls:
            url_clause = "WHERE link IN ({})".format(",".join([f"'{url}'" for url in test_urls]))
        else:
            url_clause = "WHERE body IS NOT NULL;"

        cursor.execute(f"SELECT * FROM news_article_syncs {url_clause}")
        rows = cursor.fetchall()
        column_names = [d[0] for d in cursor.description]
        for row in rows:
            self.arc_sync_story.process_article_body_and_sync_story(row, column_names)

    def sync_authors_to_arc(self):
        authors = self.db_conn.get_distinct_authors()
        for author in authors:
            if len(author.split(' ')) == 2:
                first_name, last_name = author.split(' ')
            else:
                first_name, last_name = author, ''
            author_ans = ArcAuthorANS(first_name, last_name)
            response_create_author = self.api_request.create_arc_author(author_ans)
            print(f"Response from creating author {author}: {response_create_author}")

    def delete_migration_test_images(self):
        migration_images = self.api_request.get_migration_test_images()
        images_data = json.loads(migration_images)
        ids = [_id['_id'] for _id in images_data]
        for image_id in ids:
            response = self.api_request.delete_arc_image(image_id)
            if response == '':
                print(f"Image with ID {image_id} has been successfully deleted.")
            else:
                print(f"Failed to delete image with ID {image_id}.")
                print(f"Response from API: {response}")

    def delete_migration_test_stories(self):
        migration_stories = self.api_request.get_migration_test_stories()
        stories_data = json.loads(migration_stories)
        ids = [_id['_id'] for _id in stories_data['content_elements']]
        for story_id in ids:
            response = self.api_request.delete_arc_story(story_id)
            if "error_message" not in response:
                print(f"DELETE::: Story with ID {story_id} has been successfully deleted.")
            else:
                print(f"DELETE::: Failed to delete Story with ID {story_id}.")
            print(f"DELETE::: Response from API: {response}")

    def test_get_site_sections(self):
        site_sections = self.api_request.get_site_sections()
        site_list = json.loads(site_sections)
        language_list = site_list.get('children', [])
        for language in language_list:
            print(f"{language.get('_id', '')}: {language.get('name', '')}")
            sections = language.get('children', [])
            for section in sections:
                print(f"  {section.get('_id', '')}: {section.get('name', '')}")
                sub_sections = section.get('children', [])
                for sub_section in sub_sections:
                    print(f"    {sub_section.get('_id', '')}: {sub_section.get('name', '')}")
