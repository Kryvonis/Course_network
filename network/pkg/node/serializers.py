import json
from network.pkg.node.models import Node
from json import JSONEncoder
from network.pkg.routing.serializers import JSONRouteTableSerializer


class JSONNodeSerializer(JSONEncoder):
    def encode(self, o):
        attr = {'id': o.id,
                'chanels': o.chanels,
                'table': json.dumps(o.table, cls=JSONRouteTableSerializer),
                'X': o.X,
                'Y': o.Y,
                }
        return json.dumps(attr)

    @classmethod
    def decode(cls, o):
        o = json.loads(o)
        table = JSONRouteTableSerializer.decode(o['table'])
        return Node(o['id'], o['chanels'], table, o['X'], o['Y'])
