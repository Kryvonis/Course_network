import json
from network.pkg.node.models import Node
from json import JSONEncoder
from network.pkg.routing.serializers import JSONRouteTableSerializer
from network.pkg.chanels.serializers import JSONChanelSerializer


class JSONNodeSerializer(JSONEncoder):
    def encode(self, o):
        attr = {'id': o.id,
                'channels': json.loads(json.dumps(o.channels, cls=JSONChanelSerializer)),
                'table': json.loads(json.dumps(o.table, cls=JSONRouteTableSerializer)),
                'X': o.X,
                'Y': o.Y,
                }
        return json.dumps(attr)

    @classmethod
    def decode(cls, o):
        o = json.loads(o)
        table = JSONRouteTableSerializer.decode(o['table'])
        channels = JSONChanelSerializer.decode(o['channels'])
        return Node(o['id'], channels, table, o['X'], o['Y'])


class JSONNetworkSerializer(JSONEncoder):
    def encode(self, o):
        attr = [json.dumps(node, cls=JSONNodeSerializer) for node in o]
        return json.dumps(attr)

    @classmethod
    def decode(cls, o):
        o = json.loads(o)
        for item in o:
            JSONNodeSerializer.decode(item)