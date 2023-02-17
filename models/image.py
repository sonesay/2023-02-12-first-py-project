import os

from helpers.arc_id_generator import generate_arc_id


class Image:
    def __init__(self, file_name, data):
        self._id = generate_arc_id(os.environ.get('API_KEY'), file_name)
        self.type = "image"
        self.version = "0.10.7"

        if data.get('owner') is not None:
            self.auth = data.get('owner')

        if data.get('additional_properties') != {}:
            self.additional_properties = data.get('additional_properties')

    def get_id(self):
        return self._id
