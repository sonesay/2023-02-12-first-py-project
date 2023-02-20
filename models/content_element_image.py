class ContentElementImage:
    def __init__(self, arc_id):
        self.type = "reference"
        self._id = arc_id
        self.referent = {
            "type": "image",
            "id": arc_id
        }
