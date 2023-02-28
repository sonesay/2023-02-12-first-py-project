import json
import sys
from collections import namedtuple

from bs4 import BeautifulSoup
from html2ans.default import Html2Ans
from helpers.api_request import APIRequest
from helpers.arc_sync_story import ArcSyncStory
from helpers.db_conn import DbConn
from models.story import Headlines, Story


class ArcSync:
    def __init__(self):
        self.db_conn = DbConn()
        self.api_request = APIRequest()
        self.arc_sync_story = ArcSyncStory()

    def sync_stories_to_arc(self):
        cursor = self.db_conn.conn.cursor()
        # cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NOT NULL AND arc_id IS NULL")
        cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NOT NULL LIMIT 1")
        # cursor.execute(
        #     "SELECT * FROM news_article_syncs WHERE link = 'https://www.teaomaori.news/karekare-welfare-mission-include-trauma-counselling'")

        rows = cursor.fetchall()
        column_names = [d[0] for d in cursor.description]
        for row in rows:
            self.arc_sync_story.process_article_body_and_sync_story(row, column_names)

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
