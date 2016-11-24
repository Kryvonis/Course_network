from network.pkg.channels.models import Channel


class JSONChanelSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            channels = []
            for o in obj:
                channels.append(JSONChanelSerializer.encode(o))
            return channels
        if isinstance(obj, Channel):
            return obj.__dict__

    @classmethod
    def decode(cls, ojb):
        if isinstance(ojb, list):
            channels = []
            for o in ojb:
                channels.append(Channel(**o))
            return channels
        if isinstance(ojb, dict):
            return Channel(**ojb)
