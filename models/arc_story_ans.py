import html
import os
from datetime import datetime
import pytz

from helpers.arc_id_generator import generate_arc_id


class ArcStoryANS:
    def __init__(self, title, arc_story_id=None):
        if arc_story_id is not None:
            self._id = arc_story_id
        else:
            self._id = generate_arc_id(title, "story")
        self.type = "story"
        self.version = "0.10.9"
        self.canonical_website = os.environ.get('CANONICAL_WEBSITE')
        self.content_elements = []
        self.promo_items = []
        self.taxonomy = {}
        self.source = {"system": "Drupal"}
        self.credits = {"by": []}
        self.headlines = None
        self.subtype = None,
        self.display_date = None,

    def get_id(self):
        return self._id

    def set_seo_keywords(self, keywords):
        self.taxonomy['seo_keywords'] = keywords

    def add_story_tag(self, tag_text, tag_slug=None, tag_description=None):
        tag = {"text": tag_text}
        if tag_slug:
            tag["slug"] = tag_slug
        if tag_description:
            tag["description"] = tag_description
        if "tags" in self.taxonomy:
            self.taxonomy["tags"].append(tag)
        else:
            self.taxonomy["tags"] = [tag]

    def set_source_id(self, source_id):
        self.source["source_id"] = source_id

    def add_credits_author(self, author_id):
        self.credits["by"].append({
            "referent": {
                "id": author_id,
                "provider": "",
                "referent_properties": {},
                "type": "author"
            },
            "type": "reference"
        })

    def set_headlines(self, basic):
        self.headlines = Headlines(basic)

    def set_subtype(self, subtype):
        self.subtype = subtype

    def set_display_date(self, display_date):
        self.display_date = display_date

    def to_dict(self):
        result = {
            "_id": self._id,
            "type": self.type,
            "version": self.version,
            "canonical_website": self.canonical_website,
            "content_elements": self.content_elements,
            "promo_items": self.promo_items,
            "taxonomy": self.taxonomy,
            "source": self.source,
            "credits": self.credits,
            "headlines": self.headlines,
            "display_date": convert_date_string(self.display_date),
        }

        if self.subtype is not None:
            result["subtype"] = self.subtype

        return result


class Headlines:
    def __init__(self, basic):
        self.basic = html.unescape(basic).replace('�', '')


def convert_date_string(date_string):
    original_date_format = '%Y-%m-%d %H:%M:%S'
    desired_date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    original_date = datetime.strptime(date_string, original_date_format)
    utc_timezone = pytz.timezone('UTC')
    original_date_utc = utc_timezone.localize(original_date)
    desired_date_string = original_date_utc.strftime(desired_date_format)
    return desired_date_string
