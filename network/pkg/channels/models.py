# from django.db import models
# Create your models here.
import random
from network.pkg.node.finder import find_node_by_address

weights = (1, 2, 3, 4, 5, 7, 11, 12, 15, 17, 19, 24, 27, 28)
channels_types = ('duplex', 'halfduplex')


class Channel:
    def __init__(self, id, start_node_id, end_node_id, type=random.choice(channels_types)):
        self.id = id
        self.weight = random.choice(weights)
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
        """
        return node buffer
        :param id: node id
        :return: node_buffer
        """
        if id == self.start_node_id:
            return self.start_node_buffer
        else:
            return self.end_node_buffer

    def add_to_buffer(self, id, msg):
        """
        add to node buffer
        :param id: node id
        :param msg: what message you want to add
        :return: None
        """
        if id == self.start_node_id:
            self.start_node_buffer.append(msg)
        else:
            self.end_node_buffer.append(msg)

    def remove_from_buffer(self, id, msg):
        """
        remove message from buffer
        :param id: node id
        :param msg: what message you want to remove
        :return: None
        """
        if id == self.start_node_id:
            self.start_node_buffer.pop(self.start_node_buffer.index(msg))
        else:
            self.end_node_buffer.pop(self.end_node_buffer.index(msg))

    def can_send_message(self, id):
        """
        Check if you can send message,
        :param id: node id
        :return: boolean
        """
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

    def __put_message_to_channel(self, msg, id):
        """
        add message to channel buffer and remove from node buffer
        :param msg: what message
        :param id: node id
        :return: None
        """
        self.message_buffer[str(id)] = msg
        self.remove_from_buffer(id, msg)

    def try_send_from_node_buffer_to_channel(self, id):
        """
        send from node buffer to channel buffer with correct logic
        :param id: node id
        :return:
        """
        buffer = self.get_node_buffer(id)
        if self.can_send_message(id) and buffer:
                self.__put_message_to_channel(buffer[0], id)

    def send_from_channel_to_buffer(self):
        """
        add message to node buffer after delay and remove from channel buffer
        :return:
        """
        for key, msg in self.message_buffer.items():
            if msg:
                if msg.delay == 0:
                    self.__send_message(key, msg)
                    self.message_buffer[key] = 0
                else:
                    msg.delay -= 1

    # def send_from_buffer_to_channel(self, node_id):
    #     if self.can_send_message(node_id) and self.get_node_buffer(node_id):

    def __send_message(self, key, msg):
        """
        logic for adding message from channel buffer to node buffer
        :param key: node buffer key
        :param msg: message
        :return: None
        """
        if int(key) == self.end_node_id:
            self.start_node_buffer.append(msg)
        else:
            self.end_node_buffer.append(msg)

    # def get_message_from_channel(self, position):
    #     """
    #     remove from channel buffer message
    #     not working correct
    #     :param position:
    #     :return:
    #     """
    #     if self.message_buffer:
    #         tmp = self.message_buffer[position]
    #         self.message_buffer[position] = 0
    #         return tmp

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
