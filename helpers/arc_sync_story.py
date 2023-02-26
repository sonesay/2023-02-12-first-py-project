import json
import os
import re
import sys
from collections import namedtuple
from pprint import pprint

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

    def process_article_body_and_sync_story(self, row, column_names):
        cursor = self.db_conn.conn.cursor()
        row_dict = {column_names[i]: value for i, value in enumerate(row)}
        NewsArticle = namedtuple('NewsArticle', column_names)
        news_article = NewsArticle(*row)
        bc_video_count = 0
        yt_video_count = 0
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

        video_div = full_article_soup.find('video', {'class': 'video-js'}) or None
        if video_div:

            video_id = video_div['data-video-id']
            print(video_id)
            self.api_brightcove.authorize()
            video_detail = self.api_brightcove.get_video(video_id)
            video_name = re.sub(r'\W+', ' ', video_detail['name']).strip()
            video_name = re.sub(r'\s+', '_', video_name)

            video_data = self.api_brightcove.get_video_sources(video_id)
            mp4_data = [d for d in video_data if d.get('container') == 'MP4']
            sorted_mp4_data = sorted(mp4_data, key=lambda d: d.get('encoding_rate', 0), reverse=True)
            highest_quality_url = sorted_mp4_data[0]['src']
            video_extension = sorted_mp4_data[0]['container'].split('.')[-1]

            if feature_media_url is None:
                feature_media_url = news_article.featured_image

            video_ans = ArcVideoANS("sample", row_dict['title'], feature_media_url, highest_quality_url,
                                    video_extension, True)

            # self.api_request.get_arc_video('f3f68db5-2906-4195-bf35-4890a304c047')
            # print(vars(video_ans))
            # content_json = json.dumps(video_ans, default=lambda o: o.__dict__)
            # pretty_json = json.dumps(content_json, indent=4)
            # print(pretty_json)

            pprint(video_ans.to_dict())

            # sys.exit()

            response_create_arc_video = self.api_request.create_arc_video(video_ans)
            response_create_arc_video_dict = json.loads(response_create_arc_video)
            print(f"Created Arc Video with _id = {response_create_arc_video_dict['_id']}")
            bc_video_count = bc_video_count + 1

        # self.save_image_to_local_storage(highest_quality_url, video_name)

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
            response_update = cursor.execute("UPDATE news_article_syncs SET arc_id=?, bc_video_count=? WHERE id=?",
                                             (arc_id, bc_video_count, row_dict['id']))
            self.db_conn.conn.commit()
            if response_update.rowcount == 1:
                print("Update successful")
            else:
                print("Update failed")

            print(f"Story created successfully with ID {arc_id}")

            print(f"Row ID: {row_dict['id']}")
            print(f"Link: {row_dict['link']}")
            print(f"bc_video_count: {bc_video_count}")
        else:
            error_message = response_data.get('message', 'Unknown error')
            print(f"Failed to create story: {error_message}")

    def save_image_to_local_storage(self, highest_quality_url, video_name):
        response = requests.get(highest_quality_url)
        os.makedirs('./videos', exist_ok=True)
        with open(f'./videos/{video_name}', 'wb') as f:
            f.write(response.content)
