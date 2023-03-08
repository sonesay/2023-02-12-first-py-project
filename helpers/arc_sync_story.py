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
from helpers.arc_iframe_parser import ArcIframeParser
from models.arc_author_ans import ArcAuthorANS
from models.arc_video_ans import ArcVideoANS
from models.circulate_ans import WebsiteSection, CirculateANS
from models.content_element_image import ContentElementImage
from models.promo_items import PromoItems
from models.arc_story_ans import Headlines, ArcStoryANS
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
        self._arc_story_ans = None

    @property
    def arc_story_ans(self):
        return self._arc_story_ans

    def process_article_body_and_sync_story(self, row, column_names):
        cursor = self.db_conn.conn.cursor()
        row_dict = {column_names[i]: value for i, value in enumerate(row)}
        NewsArticle = namedtuple('NewsArticle', column_names)
        news_article = NewsArticle(*row)
        bc_video_count = 0
        yt_video_count = 0

        arc_story_id = self.db_conn.get_arc_id_by_link(news_article.link)

        self._arc_story_ans = ArcStoryANS(news_article.title, arc_story_id)
        self.arc_story_ans.set_headlines(news_article.title)
        self.arc_story_ans.set_source_id(row_dict['link'])

        print(f"Arc Story ID: {arc_story_id}")
        print(f"Title: {news_article.title}")

        response_existing_arc_story = self.api_request.get_arc_story(self.arc_story_ans.get_id())
        response_existing_arc_story_json = json.loads(response_existing_arc_story)
        if 'id' in response_existing_arc_story_json:
            print(f"Skipping sync for existing Arc story with ID {response_existing_arc_story_json['id']}")
            return

        parser = Html2Ans()
        parser.insert_parser('h4', ArcIframeParser(), 0)
        full_article_soup = BeautifulSoup(row_dict['body'], 'html.parser')

        thumbnail_div = full_article_soup.find("div", class_="field-thumbnail-override")
        feature_media_url = thumbnail_div.find('img')['src'] if thumbnail_div else None
        arc_id_for_image = generate_arc_id(os.environ.get('API_KEY'), feature_media_url)

        if feature_media_url is not None:
            feature_media_upload_response = self.api_request.create_arc_image(arc_id_for_image, feature_media_url)
        if thumbnail_div:
            thumbnail_div.decompose()
            self.arc_story_ans.promo_items = PromoItems(arc_id_for_image).to_dict()

        field_video_div = full_article_soup.find("div", class_="field-video")

        public_interest_journalism = full_article_soup.find('img', alt=lambda
            x: x and 'Public Interest Journalism' in x) or None
        if public_interest_journalism:
            public_interest_journalism.decompose()

        mailto_tag = full_article_soup.find('a', href='mailto:openjustice@nzme.co.nz')
        img_tag = full_article_soup.find('img', src=lambda x: x and 'OPEN-JUSTICE_ONLINE.jpg' in x)
        if mailto_tag is not None:
            mailto_tag.decompose()
        if img_tag is not None:
            img_tag.decompose()

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

            video_ans = ArcVideoANS("sample", row_dict['title'], row_dict['category'], feature_media_url,
                                    highest_quality_url,
                                    video_extension, True)
            pprint(video_ans.to_dict())

            try:
                response_create_arc_video = self.api_request.create_arc_video(video_ans)
                response_create_arc_video_dict = json.loads(response_create_arc_video)
                print(f" CREATE VIDEO::: Created Arc Video with _id = {response_create_arc_video_dict['_id']}")
                bc_video_count = bc_video_count + 1
            except Exception as e:
                print(f" CREATE VIDEO::: Error: Error creating Arc Video: {e}")

            self.arc_story_ans.promo_items = PromoItems(video_ans.get_id(), 'lead_art', 'video').to_dict()

        iframe = full_article_soup.find('iframe', {'src': lambda s: 'youtube.com' in s})
        if iframe:
            print('Found YouTube video iframe:', iframe)
            yt_video_count = yt_video_count + 1
        else:
            print('No YouTube video iframe found')

        content_elements = parser.generate_ans(str(body_html))

        # Loop through the content elements and replace images with references to Arc
        for i in range(len(content_elements)):
            if content_elements[i]['type'] == 'image':
                image_url = content_elements[i]['url']
                arc_id_for_image = generate_arc_id(os.environ.get('API_KEY'), image_url)
                feature_media_upload_response = self.api_request.create_arc_image(arc_id_for_image, image_url)
                content_element_image = ContentElementImage(arc_id_for_image)
                content_elements[i] = content_element_image.__dict__

        self.process_tags_list(self.db_conn.get_tags_by_id(row_dict['id']))

        self.arc_story_ans.content_elements = content_elements;

        if not self.arc_story_ans.promo_items:
            del self.arc_story_ans.promo_items

        author_name = row_dict['author']
        if ' ' in author_name:
            first_name, last_name = author_name.split(' ')
        else:
            first_name, last_name = author_name, ''
        author_ans = ArcAuthorANS(first_name, last_name)

        self.arc_story_ans.add_credits_author(author_ans.get_id())

        # response_story_delete = self.api_request.delete_arc_story(self.arc_story_ans.get_id())
        response_create_arc_story = self.api_request.create_arc_story(self.arc_story_ans.to_dict())

        self.update_article_row_details(cursor, response_create_arc_story, row_dict, bc_video_count, yt_video_count)

        website_primary_section = WebsiteSection(row_dict['category']).to_dict()
        website_sections = []
        for section in self.db_conn.get_categories_by_link(row_dict['link']):
            website_sections.append(WebsiteSection(section).to_dict())

        circulate_ans = CirculateANS(self.arc_story_ans.get_id(), website_primary_section, website_sections)

        response_circulate = self.api_request.create_arc_circulation(self.arc_story_ans.get_id(), circulate_ans)

    def process_tags_list(self, tags_list):
        if tags_list is not None:
            self.arc_story_ans.set_seo_keywords(tags_list)
            for tag in tags_list:
                self.arc_story_ans.add_story_tag(tag)
                if tag == 'Open Justice':
                    self.arc_story_ans.set_subtype('Open Justice')
                elif tag == 'Public Interest Journalism':
                    self.arc_story_ans.set_subtype('Public Interest Journalism')
                elif tag == 'Te Rito':
                    self.arc_story_ans.set_subtype('Te Rito')

    def update_article_row_details(self, cursor, response_create_arc_story, row_dict, bc_video_count, yt_video_count):
        response_create_arc_story_data = json.loads(response_create_arc_story)
        if 'id' in response_create_arc_story_data:
            arc_id = response_create_arc_story_data['id']
            response_update = cursor.execute(
                "UPDATE news_article_syncs SET arc_id=?, bc_video_count=?, yt_video_count=? WHERE id=?",
                (arc_id, bc_video_count, yt_video_count, row_dict['id']))
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
            error_message = response_create_arc_story_data.get('message', 'Unknown error')
            print(f"Failed to create story: {error_message}")
