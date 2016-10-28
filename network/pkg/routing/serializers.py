import json
from network.pkg.routing.models import RouteTable
from json import JSONEncoder


class JSONRouteTableSerializer(JSONEncoder):
    def encode(self, o):
        attr = {'node_id': o.node_id,
                'addresses': o.addresses,
                'metric': o.metric,
                'path': o.path,
                }
        return json.dumps(attr)

    @classmethod
    def decode(cls, o):
        o = json.loads(o)
        return RouteTable(o['node_id'], o['addresses'], o['metric'], o['path'], )
