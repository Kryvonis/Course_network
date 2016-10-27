from django.db import models
import json
from network.pkg.chanels.serializers import ChanelSerializer


# Create your models here.
class Chanel:
    def __init__(self, id=0, weight=0, fromX=0, toX=1, fromY=0, toY=1, type='duplex'):
        self.id = id
        self.weight = weight
        self.fromX = fromX
        self.toX = toX
        self.fromY = fromY
        self.toY = toY
        self.type = type

    def __str__(self, *args, **kwargs):
        return ','.join((str(value) for value in self.__dict__.values()))

    def __repr__(self, *args, **kwargs):
        cls = self.__class__.__name__
        attr = ('%s=%s' % item for item in self.__dict__.items())

        return '%s(%s)' % (cls, ', '.join(attr))

    def to_json(self):
        return ChanelSerializer().encode(self)


if __name__ == '__main__':
    c = Chanel()

    print(c.__repr__())
    lol = c.to_json()
    print(type(lol))
    print(lol)
    print(ChanelSerializer().encode(c))
    # t = Chanel().from_json(json.loads(lol))
    # print(t.__repr__())

    # print(lol['id'])
    # t = Chanel().deserialize(lol)
    # print(t.__repr__())
