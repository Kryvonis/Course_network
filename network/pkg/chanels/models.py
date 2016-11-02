# from django.db import models
# Create your models here.


class Channel:
    def __init__(self, id, weight, fromX, toX, fromY, toY, start_node_id, end_node_id, type='Duplex'):
        self.id = id
        self.weight = weight
        self.fromX = fromX
        self.toX = toX
        self.fromY = fromY
        self.toY = toY
        self.type = type
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id

    def __str__(self, *args, **kwargs):
        return ','.join((str(value) for value in self.__dict__.values()))

    def __repr__(self, *args, **kwargs):
        cls = self.__class__.__name__
        attr = ('%s=%s' % item for item in self.__dict__.items())

        return '%s(%s)' % (cls, ', '.join(attr))

    def __eq__(self, *args, **kwargs):
        if not isinstance(args[0], Channel):
            return False
        if args[0].__dict__ != self.__dict__:
            return False
        return True
        # return super().__eq__(*args, **kwargs)
