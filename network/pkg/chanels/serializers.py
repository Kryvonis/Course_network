from network.pkg.chanels.models import Channel
import json
from json import JSONEncoder


class JSONChanelSerializer(JSONEncoder):
    def encode(self, obj):
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
            return json.dumps(chanels)
        if isinstance(obj, Channel):
            attr = {'id': obj.id,
                    'weight': obj.weight,
                    'fromX': obj.fromX,
                    'toX': obj.toX,
                    'fromY': obj.fromY,
                    'toY': obj.toY,
                    'start_node_id': obj.start_node_id,
                    'end_node_id': obj.end_node_id,
                    'type': obj.type
                    }
        return json.dumps(attr)

    @classmethod
    def decode(cls, obj):
        o = json.loads(obj)
        if isinstance(o, list):
            chanels = []
            for _ in o:
                chanels.append(
                    Channel(_['id'],
                            _['weight'],
                            _['fromX'],
                            _['toX'],
                            _['fromY'],
                            _['toY'],
                            _['start_node_id'],
                            _['end_node_id'],
                            _['type']))
            return chanels
        if isinstance(o,dict):
            return Channel(o['id'],
                           o['weight'],
                           o['fromX'],
                           o['toX'],
                           o['fromY'],
                           o['toY'],
                           o['start_node_id'],
                           o['end_node_id'],
                           o['type'])
