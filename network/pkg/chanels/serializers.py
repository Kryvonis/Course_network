from json import JSONEncoder, JSONDecoder
# from network.pkg.chanels.models import Chanel
import json


class ChanelSerializer:
    @staticmethod
    def encode(o):
        attr = {'id': o.id,
                'weight': o.weight,
                'fromX': o.fromX,
                'toX': o.toX,
                'fromY': o.fromY,
                'toY': o.toY,
                }
        return json.dumps(attr)

        # def decode(self, o):
        #     return Chanel()
