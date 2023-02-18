class PromoItems:
    def __init__(self, arc_id):
        self.id = arc_id
        self.type = "reference"
        self.referent = {
            "id": arc_id,
            "type": "image",
            "provider": "",
            "referent_properties": {}
        }

    def to_dict(self):
        return {
            "basic": {
                "_id": self.id,
                "type": self.type,
                "referent": self.referent
            }
        }
