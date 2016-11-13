from django.db import models
from network.pkg.routing.models import RouteTable
from network.pkg.channels.models import Channel

# Create your models here.
class Node:
    def __init__(self, id, channels, table: RouteTable, X, Y, address = 0):
        self.id = id
        self.channels = channels
        self.table = table
        self.X = X
        self.Y = Y
        self.address = address

    def __str__(self, *args, **kwargs):
        return '==========\nid : {}\ntable: {}\nX: {}\nY: {}\naddress:{}\nchannels: {}\n==========\n'. \
            format(self.id, self.table, self.X, self.Y, self.address, self.channels)

    def __repr__(self, *args, **kwargs):
        return '==========\nid : {}\ntable: {}\nX: {}\nY: {}\naddress:{}\nChannels: {}\n==========\n\n'. \
            format(self.id, self.table, self.X, self.Y, self.address, self.channels)

    def __eq__(self, *args, **kwargs):
        if not isinstance(args[0], Node):
            return False
        if args[0].__dict__ != self.__dict__:
            return False
        return True
