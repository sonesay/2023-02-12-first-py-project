import os
import re

from helpers.arc_id_generator import generate_arc_id


class ArcAuthorANS:
    def __init__(self, first_name, last_name):
        self._id = generate_arc_id(os.environ.get('CANONICAL_WEBSITE'), f"{first_name} {last_name}")
        self.firstName = first_name
        self.lastName = last_name
        self.byline = f"{first_name} {last_name}"
        self.slug = re.sub(r'[^\w\s-]', '', self.byline.strip().lower().replace(' ', '-'))
        self.image = ""
        self.expertise = ""
        self.location = ""
        self.role = ""
        self.author_type = ""
        self.email = ""
        self.books = []
        self.awards = []
        self.education = []
        self.podcasts = []
        self.twitter = ""
        self.facebook = ""
        self.rss = ""
        self.gplus = ""
        self.linkedin = ""
        self.bio_page = ""
        self.bio = ""
        self.longBio = ""
        self.last_updated_date = ""

    def get_id(self):
        return self._id

    def to_dict(self):
        return {
            "_id": self._id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "byline": self.byline,
            "slug": self.slug,
            "image": self.image,
            "expertise": self.expertise,
            "location": self.location,
            "role": self.role,
            "author_type": self.author_type,
            "email": self.email,
            "books": self.books,
            "awards": self.awards,
            "education": self.education,
            "podcasts": self.podcasts,
            "twitter": self.twitter,
            "facebook": self.facebook,
            "rss": self.rss,
            "gplus": self.gplus,
            "linkedin": self.linkedin,
            "bio_page": self.bio_page,
            "bio": self.bio,
            "longBio": self.longBio,
            "last_updated_date": self.last_updated_date
        }
