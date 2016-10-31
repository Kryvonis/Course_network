from django.db import models
from network.pkg.routing.models import RouteTable


# Create your models here.
class Node:
    def __init__(self, id, channels, table: RouteTable, X, Y):
        self.id = id
        self.channels = channels
        self.table = table
        self.X = X
        self.Y = Y

    def __str__(self, *args, **kwargs):
        return ','.join((str(value) for value in self.__dict__.values()))

    def __repr__(self, *args, **kwargs):
        cls = self.__class__.__name__
        attr = ('%s=%s' % item for item in self.__dict__.items())

        return '%s(%s)' % (cls, ', '.join(attr))

    def __eq__(self, *args, **kwargs):
        if not isinstance(args[0], Node):
            return False
        if args[0].__dict__ != self.__dict__:
            return False
        return True
