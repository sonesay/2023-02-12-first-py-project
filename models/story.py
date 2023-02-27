import html
from helpers.arc_id_generator import generate_arc_id


class Story:
    def __init__(self, ans_type, version, canonical_website, headlines):
        self._id = generate_arc_id(canonical_website, headlines.basic)
        self.type = ans_type
        self.version = version
        self.canonical_website = canonical_website
        self.headlines = headlines
        self.content_elements = []
        self.promo_items = []
        self.taxonomy = {}

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


class Headlines:
    def __init__(self, basic):
        self.basic = html.unescape(basic).replace('�', '')
