class PromoItems:
    def __init__(self, arc_id, promo_type='basic', media_type='image'):
        self.id = arc_id
        self.promo_type = promo_type
        self.type = "reference"
        self.referent = {
            "id": arc_id,
            "type": media_type,
            "provider": "",
            "referent_properties": {}
        }

    def to_dict(self):
        return {
            self.promo_type: {
                "_id": self.id,
                "type": self.type,
                "referent": self.referent
            }
        }
