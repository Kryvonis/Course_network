from network.pkg.channels.models import Channel
import json

class JSONChanelSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            chanels = []
            for o in obj:
                chanels.append(o.__dict__)
            return chanels
        if isinstance(obj, Channel):
            return obj.__dict__

    @classmethod
    def decode(cls, ojb):
        if isinstance(ojb, list):
            chanels = []
            for o in ojb:
                chanels.append(Channel(**o))
            return chanels
        if isinstance(ojb, dict):
            return Channel(**ojb)
