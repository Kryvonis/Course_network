import json
from network.pkg.node.models import Node
from network.pkg.routing.serializers import JSONRouteTableSerializer
from network.pkg.channels.serializers import JSONChanelSerializer


class JSONNodeSerializer:
    @classmethod
    def encode(cls, o):
        if isinstance(o, Node):
            attr = {'id': o.id,
                    'table': JSONRouteTableSerializer.encode(o.table),
                    'X': o.X,
                    'Y': o.Y,
                    'channels': JSONChanelSerializer.encode(o.channels),
                    'address': o.address,
                    }
            return attr
        if isinstance(o, list):
            nodes = []
            for node in o:
                nodes.append(JSONNodeSerializer.encode(node))
            return nodes

    @classmethod
    def decode(cls, o):
        if isinstance(o, dict):
            table = JSONRouteTableSerializer.decode(o['table'])
            channels = JSONChanelSerializer.decode(o['channels'])
            return Node(o['id'], channels, table, o['X'], o['Y'], address=o['address'])
        if isinstance(o, list):
            nodes = []
            for item in o:
                nodes.append(JSONNodeSerializer.decode(item))
            return nodes