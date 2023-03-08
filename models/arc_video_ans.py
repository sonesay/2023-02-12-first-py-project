import os
from datetime import datetime

from helpers.arc_id_generator import generate_arc_id


class ArcVideoANS:
    def __init__(self, video_category, headline, primary_section_id, promo_item_url, url, video_extension="mp4",
                 published=False):
        self._id = generate_arc_id(os.environ.get('CANONICAL_WEBSITE'), headline)
        self.type = "video"
        self.version = "0.8.0"
        self.owner = {"id": os.environ.get('OWNER_ID')}
        self.streams = [{"url": url, "stream_type": video_extension}]
        self.additional_properties = {"videoCategory": video_category}
        self.canonical_website = os.environ.get('CANONICAL_WEBSITE')
        self.websites = {os.environ.get('CANONICAL_WEBSITE'): {}}
        self.taxonomy = {
            "primary_section": {
                "type": "reference",
                "referent": {
                    "id": primary_section_id,
                    "type": "section",
                    "website": os.environ.get('CANONICAL_WEBSITE')
                }
            }
        }
        self.headlines = {"basic": headline}
        self.promo_items = {
            "basic": {
                "type": "image",
                "url": promo_item_url,
                "version": "0.8.0"
            }
        }
        self.revision = {"published": published}
        try:
            if published:
                current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                self.display_date = current_time
                self.publish_date = current_time
        except Exception as e:
            print(f"An error occurred while setting the date: {e}")

    def to_dict(self):
        video_dict = {
            "type": self.type,
            "version": self.version,
            "owner": self.owner,
            "streams": self.streams,
            "additional_properties": self.additional_properties,
            "canonical_website": self.canonical_website,
            "websites": self.websites,
            "taxonomy": self.taxonomy,
            "headlines": self.headlines,
            "promo_items": self.promo_items,
            "revision": self.revision
        }
        if hasattr(self, "display_date"):
            video_dict["display_date"] = self.display_date
        if hasattr(self, "publish_date"):
            video_dict["publish_date"] = self.publish_date
        return video_dict

    def get_id(self):
        return self._id

# Add source property
# "source": {
#     "system": "brightcove",
#     "source_id": "123456889"
#   },
