from network.pkg.chanels.models import Channel
import json
from json import JSONEncoder


class JSONChanelSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            chanels = []
            for o in obj:
                attr = {'id': o.id,
                        'weight': o.weight,
                        'fromX': o.fromX,
                        'toX': o.toX,
                        'fromY': o.fromY,
                        'toY': o.toY,
                        'start_node_id': o.start_node_id,
                        'end_node_id': o.end_node_id,
                        'type': o.type
                        }
                chanels.append(attr)
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
