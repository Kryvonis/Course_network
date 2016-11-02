import json
from network.pkg.routing.models import RouteTable
from json import JSONEncoder


class JSONRouteTableSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            routes = []
            for o in obj:
                routes.append(o.__dict__)
            return routes
        if isinstance(obj, RouteTable):
            return obj.__dict__

    @classmethod
    def decode(cls, ojb):
        if isinstance(ojb, list):
            routes = []
            for o in ojb:
                routes.append(RouteTable(**o))
            return routes
        if isinstance(ojb, dict):
            return RouteTable(**ojb)
