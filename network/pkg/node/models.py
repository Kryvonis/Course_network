from django.db import models
from network.pkg.routing.models import RouteTable
from network.pkg.channels.models import Channel


# Create your models here.
class Node:
    def __init__(self, id, channels, table: RouteTable, X, Y, address=0,
                 shutdown=0):
        self.id = id
        self.channels = channels
        self.table = table
        self.X = X
        self.Y = Y
        self.address = address
        self.shutdown = shutdown

    def __str__(self, *args, **kwargs):
        return 'id:{};address:{};channels: {}table: {}\nX: {}\nY: {}'. \
            format(self.id, self.address, self.channels, self.table, self.X,
                   self.Y, )

    def __eq__(self, *args, **kwargs):
        if not isinstance(args[0], Node):
            return False
        if args[0].__dict__ != self.__dict__:
            return False
        return True
