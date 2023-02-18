import json
import sys
from collections import namedtuple

from bs4 import BeautifulSoup
from html2ans.default import Html2Ans
from helpers.api_request import APIRequest
from helpers.db_conn import DbConn
from models.story import Headlines, Story


class ArcSync:
    def __init__(self):
        self.db_conn = DbConn()
        self.api_request = APIRequest()

    def sync_to_arc(self):
        cursor = self.db_conn.conn.cursor()
        # cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NOT NULL AND arc_id IS NULL")
        cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NOT NULL")
        rows = cursor.fetchall()
        column_names = [d[0] for d in cursor.description]

        for row in rows:
            row_dict = {column_names[i]: value for i, value in enumerate(row)}
            parser = Html2Ans()
            full_article_soup = BeautifulSoup(row_dict['body'], 'html.parser')
            
            thumbnail_div = full_article_soup.find("div", class_="field-thumbnail-override")
            feature_media_url = thumbnail_div.find('img')['src'] if thumbnail_div else None
            feature_media_upload_response = self.api_request.post_to_arc_image_endpoint(feature_media_url);
            # Remove the feature media div from the body
            if thumbnail_div:
                thumbnail_div.decompose()

            body_div = full_article_soup.find("div", class_="field-body", itemprop="articleBody")
            body_html = ''.join(str(c) for c in body_div.contents)
            content_elements = parser.generate_ans(str(body_html))
            content_elements = [elem for elem in content_elements if elem['type'] != 'image']
            NewsArticle = namedtuple('NewsArticle', column_names)
            news_article = NewsArticle(*row)

            # Delete any existing arc stories with matching id
            response_delete = self.api_request.delete_arc_story(news_article)

            headlines = Headlines(news_article.title)
            story = Story("story", "0.10.9", "teaomaori", headlines)
            story.content_elements = content_elements;
            response_post = self.api_request.create_arc_story(story)
            response_data = json.loads(response_post)
            if 'id' in response_data:
                arc_id = response_data['id']
                cursor.execute("UPDATE news_article_syncs SET arc_id=? WHERE id=?", (arc_id, row_dict['id']))
                print(f"Story created successfully with ID {arc_id}")
                print(f"Link: {row_dict['link']}")
            else:
                # handle the case where 'id' is not present in response_data
                error_message = response_data.get('message', 'Unknown error')
                print(f"Failed to create story: {error_message}")
            sys.exit

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
