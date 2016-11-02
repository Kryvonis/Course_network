import json
from network.pkg.node.models import Node
from json import JSONEncoder
from network.pkg.routing.serializers import JSONRouteTableSerializer
from network.pkg.chanels.serializers import JSONChanelSerializer


class JSONNodeSerializer:
    @classmethod
    def encode(cls, o):
        attr = {'id': o.id,
                'table': JSONRouteTableSerializer.encode(o.table),
                'X': o.X,
                'Y': o.Y,
                'channels': JSONChanelSerializer.encode(o.channels),
                }
        return attr

    @classmethod
    def decode(cls, o):
        table = JSONRouteTableSerializer.decode(o['table'])
        channels = JSONChanelSerializer.decode(o['channels'])
        return Node(o['id'], channels, table, o['X'], o['Y'])


class JSONNetworkSerializer:
    @classmethod
    def encode(cls, o):
        attr = [JSONNodeSerializer.encode(node) for node in o]
        return attr

    @classmethod
    def decode(cls, o):
        network = []
        for item in o:
            network.append(JSONNodeSerializer.decode(item))
        return network
