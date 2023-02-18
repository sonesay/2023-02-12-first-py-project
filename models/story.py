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


class Headlines:
    def __init__(self, basic):
        self.basic = html.unescape(basic).replace('�', '')
