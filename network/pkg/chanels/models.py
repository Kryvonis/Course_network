# from django.db import models
# Create your models here.


class Channel:
    def __init__(self, id, weight, from_x, to_x, from_y, to_y, snid, enid, chanel_type='Duplex'):
        self.id = id
        self.weight = weight
        self.fromX = from_x
        self.toX = to_x
        self.fromY = from_y
        self.toY = to_y
        self.type = chanel_type
        self.start_node_id = snid
        self.end_node_id = enid

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
