# from django.db import models
# Create your models here.


class Chanel:
    def __init__(self, id=0, weight=0, from_x=0, to_x=1, from_y=0, to_y=1, chanel_type='Duplex'):
        self.id = id
        self.weight = weight
        self.fromX = from_x
        self.toX = to_x
        self.fromY = from_y
        self.toY = to_y
        self.type = chanel_type

    def __str__(self, *args, **kwargs):
        return ','.join((str(value) for value in self.__dict__.values()))

    def __repr__(self, *args, **kwargs):
        cls = self.__class__.__name__
        attr = ('%s=%s' % item for item in self.__dict__.items())

        return '%s(%s)' % (cls, ', '.join(attr))

    def __eq__(self, *args, **kwargs):
        if not isinstance(args[0], Chanel):
            return False
        if args[0].__dict__ != self.__dict__:
            return False
        return True
        # return super().__eq__(*args, **kwargs)
