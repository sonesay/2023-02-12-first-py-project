import json
import os
import sys
from collections import namedtuple
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from html2ans.default import Html2Ans

from helpers.api_brightcove import APIBrightcove
from helpers.arc_id_generator import generate_arc_id
from models.content_element_image import ContentElementImage
from models.promo_items import PromoItems
from models.story import Headlines, Story
from helpers.api_request import APIRequest
from helpers.db_conn import DbConn


class ArcSyncStory:
    def __init__(self):
        load_dotenv()
        self.db_conn = DbConn()
        self.api_request = APIRequest()
        self.api_brightcove = APIBrightcove(os.environ.get('BRIGHTCOVE_ACCOUNT_ID'),
                                            os.environ.get('BRIGHTCOVE_CLIENT_API_ID'),
                                            os.environ.get('BRIGHTCOVE_CLIENT_SECRET'))

    def sync_story(self, row, column_names):
        cursor = self.db_conn.conn.cursor()
        row_dict = {column_names[i]: value for i, value in enumerate(row)}
        NewsArticle = namedtuple('NewsArticle', column_names)
        news_article = NewsArticle(*row)

        headlines = Headlines(news_article.title)
        story = Story("story", "0.10.9", "teaomaori", headlines)

        parser = Html2Ans()
        full_article_soup = BeautifulSoup(row_dict['body'], 'html.parser')

        thumbnail_div = full_article_soup.find("div", class_="field-thumbnail-override")
        feature_media_url = thumbnail_div.find('img')['src'] if thumbnail_div else None
        arc_id_for_image = generate_arc_id(os.environ.get('API_KEY'), feature_media_url)
        feature_media_upload_response = self.api_request.save_arc_image(arc_id_for_image, feature_media_url)
        if thumbnail_div:
            thumbnail_div.decompose()
            story.promo_items = PromoItems(arc_id_for_image).to_dict()
        if not story.promo_items:
            del story.promo_items

        field_video_div = full_article_soup.find("div", class_="field-video")

        body_div = full_article_soup.find("div", class_="field-body", itemprop="articleBody")
        body_html = ''.join(str(c) for c in body_div.contents)

        # if field_video_div:
        #     field_video_html = str(field_video_div)
        #     body_html = field_video_html + body_html

        video_div = full_article_soup.find('video', {'class': 'video-js'})
        video_id = video_div['data-video-id']
        print(video_id)

        self.api_brightcove.authorize()

        video_json = self.api_brightcove.get_video(video_id)

        content_elements = parser.generate_ans(str(body_html))

        # Loop through the content elements and replace images with references to Arc
        for i in range(len(content_elements)):
            if content_elements[i]['type'] == 'image':
                image_url = content_elements[i]['url']
                arc_id_for_image = generate_arc_id(os.environ.get('API_KEY'), image_url)
                feature_media_upload_response = self.api_request.save_arc_image(arc_id_for_image, image_url)
                content_element_image = ContentElementImage(arc_id_for_image)
                content_elements[i] = content_element_image.__dict__

        response_delete = self.api_request.delete_arc_story(news_article)

        response_story_delete = self.api_request.delete_arc_story(story.get_id())

        story.content_elements = content_elements;
        response_post = self.api_request.create_arc_story(story)
        response_data = json.loads(response_post)

        if 'id' in response_data:
            arc_id = response_data['id']
            cursor.execute("UPDATE news_article_syncs SET arc_id=? WHERE id=?", (arc_id, row_dict['id']))
            print(f"Story created successfully with ID {arc_id}")
            print(f"Link: {row_dict['link']}")
        else:
            error_message = response_data.get('message', 'Unknown error')
            print(f"Failed to create story: {error_message}")
