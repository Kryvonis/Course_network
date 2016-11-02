from django.db import models


# Create your models here.
class RouteTable:
    def __init__(self, node_id, addresses, metric, path):
        self.node_id = node_id
        self.addresses = addresses
        self.metric = metric
        self.path = path

    def __str__(self, *args, **kwargs):
        return ','.join((str(value) for value in self.__dict__.values()))

    def __repr__(self, *args, **kwargs):
        cls = self.__class__.__name__
        attr = ('%s=%s' % item for item in self.__dict__.items())

        return '%s(%s)' % (cls, ', '.join(attr))

    def __eq__(self, *args, **kwargs):
        if not isinstance(args[0], RouteTable):
            return False
        if args[0].__dict__ != self.__dict__:
            return False
        return True
