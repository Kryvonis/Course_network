from network.pkg.chanels.models import Chanel
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
                'type': o.type
                }
        return json.dumps(attr)

    @classmethod
    def decode(cls, o):
        o = json.loads(o)
        return Chanel(o['id'], o['weight'], o['fromX'], o['toX'], o['fromY'], o['toY'], o['type'])
