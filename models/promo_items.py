class PromoItems:
    def __init__(self, id):
        self.id = id
        self.type = "reference"
        self.referent = {
            "id": id,
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
