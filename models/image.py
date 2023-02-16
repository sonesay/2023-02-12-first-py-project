import os

from helpers.arc_id_generator import generate_arc_id


class Image:
    def __init__(self, file_name, data):
        self._id = generate_arc_id(os.environ.get('API_KEY'), file_name)
        
        if data.get('additional_properties') != {}:
            self.additional_properties = data.get('additional_properties')

        if data.get('address') != {}:
            self.address = data.get('address')

        if data.get('auth') is not None:
            self.auth = data.get('auth')

        if data.get('created_date') is not None:
            self.created_date = data.get('created_date')

        if data.get('credits') != {}:
            self.credits = data.get('credits')

        if data.get('height') is not None:
            self.height = data.get('height')

        if data.get('image_type') is not None:
            self.image_type = data.get('image_type')

        if data.get('last_updated_date') is not None:
            self.last_updated_date = data.get('last_updated_date')

        if data.get('licensable') is not None:
            self.licensable = data.get('licensable')

        if data.get('owner') != {}:
            self.owner = data.get('owner')

        if data.get('source') != {}:
            self.source = data.get('source')

        if data.get('subtitle') is not None:
            self.subtitle = data.get('subtitle')

        if data.get('taxonomy') != {}:
            self.taxonomy = data.get('taxonomy')

        if data.get('type') is not None:
            self.type = data.get('type')

        if data.get('url') is not None:
            self.url = data.get('url')

        if data.get('version') is not None:
            self.version = data.get('version')

        if data.get('width') is not None:
            self.width = data.get('width')

        if data.get('syndication') != {}:
            self.syndication = data.get('syndication')
