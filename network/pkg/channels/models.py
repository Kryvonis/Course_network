# from django.db import models
# Create your models here.
import random
from network.pkg.node.finder import find_node_by_address

weights = (1, 2, 3, 4, 5, 7, 11, 12, 15, 17, 19, 24, 27, 28)


class Channel:
    def __init__(self, id, start_node_id, end_node_id, type='duplex'):
        self.id = id
        self.weight = weights[random.randint(0, len(weights) - 1)]
        self.type = type
        self.error_prob = random.random()
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.message_buffer = {}
        if self.type == 'duplex':
            self.message_buffer['{}'.format(self.start_node_id)] = 0
            self.message_buffer['{}'.format(self.end_node_id)] = 0
        else:
            self.message_buffer['0'] = 0
        self.start_node_buffer = []
        self.end_node_buffer = []
        self.is_buisy = False

    def get_node_buffer(self, id):
        if id == self.start_node_id:
            return self.start_node_buffer
        else:
            return self.end_node_buffer

    def add_to_buffer(self, id, msg):
        if id == self.start_node_id:
            self.start_node_buffer.append(msg)
        else:
            self.end_node_buffer.append(msg)

    def remove_from_buffer(self, id, msg):
        if id == self.start_node_id:
            self.start_node_buffer.pop(self.start_node_buffer.index(msg))
        else:
            self.end_node_buffer.pop(self.end_node_buffer.index(msg))

    def can_send_message(self, id):
        if self.is_buisy:
            return False
        if self.type == 'duplex':
            if self.message_buffer[str(id)]:
                return False
            return True
        if self.type == 'halfduplex':
            for key, msg in self.message_buffer:
                if self.message_buffer[key]:
                    return False
                return True

    def put_message_to_channel(self, msg, position):
        self.message_buffer[str(position)] = msg
        if position == self.start_node_id:
            self.start_node_buffer.pop(self.start_node_buffer.index(msg))
        else:
            self.end_node_buffer.pop(self.end_node_buffer.index(msg))

    def send_from_channel_to_buffer(self):
        for key, msg in self.message_buffer.items():
            if msg:
                if msg.time == 0:
                    self.__send_message(key, msg)
                    self.message_buffer[key] = 0
                else:
                    msg.time -= 1

    def __send_message(self, key, msg):
        if int(key) == self.end_node_id:
            self.start_node_buffer.append(msg)
        else:
            self.end_node_buffer.append(msg)

    def get_message_from_channel(self, position):
        if self.message_buffer:
            tmp = self.message_buffer[position]
            self.message_buffer[position] = 0
            return tmp

    # def add_to_start_buffer

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
