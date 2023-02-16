import base64
import hashlib
import json
import uuid
import six


def generate_arc_id(*args, **kwargs):
    uuid_object = uuid.UUID(
        bytes=hashlib.blake2b(
            json.dumps((args, kwargs), sort_keys=1, separators=(",", ":")).encode("utf-8"),
            digest_size=16,
        ).digest()
    )
    return six.text_type(base64.b32encode(uuid_object.bytes), encoding="utf-8").replace("=", "")  # to remove padding
