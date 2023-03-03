import html
import os

from helpers.arc_id_generator import generate_arc_id


class ArcStoryANS:
    def __init__(self, title):
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


class Headlines:
    def __init__(self, basic):
        self.basic = html.unescape(basic).replace('�', '')
