import os


class CirculateANS:
    def __init__(self, document_id, website_primary_section, website_sections):
        self.document_id = document_id
        self.website_id = os.environ.get('CANONICAL_WEBSITE')
        # self.website_url = os.environ.get('WEBSITE_URL')
        # self.website_url = '/en'
        self.website_primary_section = website_primary_section
        self.website_sections = website_sections

    def to_dict(self):
        return {
            "document_id": self.document_id,
            "website_id": self.website_id,
            # "website_url": self.website_url,
            "website_primary_section": self.website_primary_section,
            "website_sections": self.website_sections
        }


class WebsiteSection:
    def __init__(self, section_id):
        self.type = "reference"
        self.referent = {
            "id": section_id,
            "type": "section",
            "website": os.environ.get('CANONICAL_WEBSITE')
        }

    def to_dict(self):
        return {
            "type": self.type,
            "referent": self.referent
        }

# # Set up example data
# document_id = "ZHXE3Y6OJVAUFDJIM3M43AV5KM"
# website_primary_section = WebsiteSection('/news').to_dict()
# website_sections = [
#     WebsiteSection('/news').to_dict(),
#     WebsiteSection('/the-city').to_dict()
# ]
#
# # Create a new CirculateANS object
# circulate_ans = CirculateANS(document_id, website_primary_section, website_sections)
#
# # Convert the CirculateANS object to a dictionary and print it out
# circulate_dict = circulate_ans.to_dict()
# print(circulate_dict)
