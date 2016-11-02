import json
from network.pkg.routing.models import RouteTable
from json import JSONEncoder


class JSONRouteTableSerializer:
    @classmethod
    def encode(cls, o):
        attr = {'node_id': o.node_id,
                'addresses': o.addresses,
                'metric': o.metric,
                'path': o.path,
                }
        return attr

    @classmethod
    def decode(cls, o):
        return RouteTable(**o)
