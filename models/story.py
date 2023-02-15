import random
import string
import html

class Story:
    def __init__(self, type, version, canonical_website, headlines):
        self._id = self.generate_unique_id()
        self.type = type
        self.version = version
        self.canonical_website = canonical_website
        self.headlines = headlines
        self.content_elements = []

    def generate_unique_id(self):
        return ''.join(random.choices(string.ascii_uppercase, k=26))


class Headlines:
    def __init__(self, basic):
        self.basic = html.unescape(basic).replace('�', '')
