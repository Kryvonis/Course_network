from django.db import models


# Create your models here.
class RouteTable:
    def __init__(self, metric, path):
        self.metric = metric
        self.path = path

    # def __repr__(self, *args, **kwargs):
    #     cls = self.__class__.__name__
    #     attr = ('%s=%s' % item for item in self.__dict__.items())
    #
    #     return '%s(%s)' % (cls, ', '.join(attr))

    def __eq__(self, *args, **kwargs):
        if not isinstance(args[0], RouteTable):
            return False
        if args[0].__dict__ != self.__dict__:
            return False
        return True
