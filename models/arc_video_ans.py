import os


class ArcVideoANS:
    def __init__(self, video_category, headline, promo_item_url, url):
        self.type = "video"
        self.version = "0.8.0"
        self.owner = {"id": os.environ.get('OWNER_ID')}
        self.streams = [{"url": url, "stream_type": "mp4"}]
        self.additional_properties = {"videoCategory": video_category}
        self.canonical_website = os.environ.get('CANONICAL_WEBSITE')
        self.websites = {os.environ.get('CANONICAL_WEBSITE'): {}}
        self.taxonomy = {
            "primary_section": {
                "type": "reference",
                "referent": {
                    "id": "/en/national",
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
