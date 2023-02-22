import json
import os
import re
import sys
from collections import namedtuple

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from html2ans.default import Html2Ans

from helpers.api_brightcove import APIBrightcove
from helpers.arc_id_generator import generate_arc_id
from models.arc_video_ans import ArcVideoANS
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

        video_div = full_article_soup.find('video', {'class': 'video-js'})
        video_id = video_div['data-video-id']
        print(video_id)

        self.api_brightcove.authorize()

        video_detail = self.api_brightcove.get_video(video_id)
        # video_name = video_detail['name']
        video_name = re.sub(r'\W+', ' ', video_detail['name']).strip()
        video_name = re.sub(r'\s+', '_', video_name)

        video_data = self.api_brightcove.get_video_sources(video_id)

        mp4_data = [d for d in video_data if d.get('container') == 'MP4']

        sorted_mp4_data = sorted(mp4_data, key=lambda d: d.get('encoding_rate', 0), reverse=True)

        highest_quality_url = sorted_mp4_data[0]['src']

        video_ans = ArcVideoANS("sample", "test headline", feature_media_url, highest_quality_url)

        self.api_request.get_arc_video('f3f68db5-2906-4195-bf35-4890a304c047')
        self.api_request.create_arc_video(video_ans)

        response = requests.get(highest_quality_url)
        os.makedirs('./videos', exist_ok=True)

        with open(f'./videos/{video_name}', 'wb') as f:
            f.write(response.content)

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
