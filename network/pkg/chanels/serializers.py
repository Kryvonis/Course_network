from network.pkg.chanels.models import Channel
import json
from json import JSONEncoder


class JSONChanelSerializer(JSONEncoder):
    def encode(self, o):
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
        return json.dumps(attr)

    @classmethod
    def decode(cls, o):
        o = json.loads(o)
        return Channel(o['id'], o['weight'], o['fromX'], o['toX'], o['fromY'], o['toY'], o['start_node_id'],
                       o['end_node_id'],
                       o['type'])
