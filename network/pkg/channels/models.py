# from django.db import models
# Create your models here.
import random

weights = (1, 2, 3, 4, 5, 7, 11, 12, 15, 17, 19, 24, 27, 28)


class Channel:
    def __init__(self, id, start_node_id, end_node_id, type='duplex'):
        self.id = id
        self.weight = weights[random.randint(0, len(weights) - 1)]
        self.type = type
        self.error_prob = random.random()
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.message_buffer = []
        self.start_node_buffer = []
        self.end_node_buffer = []
        self.is_buisy = False

    def __can_put_message(self):
        if self.is_buisy:
            return False
        if self.type == 'duplex':
            return len(self.message_buffer) < 2
        if self.type == 'halfduplex':
            return len(self.message_buffer) < 1

    def put_message(self, msg):
        if self.__can_put_message():
            self.message_buffer.append(msg)
            return
        raise BufferError


    def __str__(self, *args, **kwargs):
        return ','.join((str(value) for value in self.__dict__.values()))

    def __repr__(self, *args, **kwargs):
        cls = self.__class__.__name__
        attr = ('%s=%s' % item for item in self.__dict__.items())

        return '%s(%s)' % (cls, ', '.join(attr))

    def __eq__(self, other):
        if not isinstance(other, Channel):
            return False
        if other.__dict__ != self.__dict__:
            return False
        return True
        # return super().__eq__(*args, **kwargs)
