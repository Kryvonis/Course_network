from json import JSONEncoder, JSONDecoder
# from network.pkg.chanels.models import Chanel
import json


class ChanelSerializer:
    def encode(self,o):
        attr = {'id': o.id,
                'weight': o.weight,
                'fromX': o.fromX,
                'toX': o.toX,
                'fromY': o.fromY,
                'toY': o.toY,
                'type': o.type
                }
        return json.loads(json.dumps(attr))
