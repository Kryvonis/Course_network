# from django.db import models
# Create your models here.
from network.pkg.message.creator import generate_error_message
from network.pkg.message.sender import statistic_table
import random
import datetime


class Channel:
    def __init__(self, id, start_node_id, end_node_id, weight,
                 type, start_node_buffer,
                 end_node_buffer, is_busy, message_buffer, error_prob):
        self.id = id
        self.weight = weight
        self.type = type
        self.error_prob = error_prob
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.message_buffer = message_buffer
        if self.type == 'duplex':
            self.message_buffer['{}'.format(self.start_node_id)] = 0
            self.message_buffer['{}'.format(self.end_node_id)] = 0
        else:
            self.message_buffer['0'] = 0
        self.start_node_buffer = start_node_buffer
        self.end_node_buffer = end_node_buffer
        self.is_busy = is_busy

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
            if 'response' in msg.type_message:
                self.start_node_buffer.insert(0, msg)
            else:
                self.start_node_buffer.append(msg)
        else:
            if 'response' in msg.type_message:
                self.end_node_buffer.insert(0, msg)
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

    def can_send_message(self, id, msg):
        """
        Check if you can send message,
        :param id: node id
        :return: boolean
        """
        if (self.is_busy == 1) and ('response' not in msg.type_message):
            return False
        if self.type == 'duplex':
            if self.message_buffer[str(id)]:
                return False
            return True
        if self.type == 'halfduplex':
            for key, msg in self.message_buffer.items():
                if self.message_buffer[key]:
                    return False
                return True

    def __put_message_to_channel(self, msg, id):
        """
        add message to channel buffer and remove from node buffer
        :param msg: what message
        :param id: node id which sending
        :return: None
        """
        # TODO Delay logic
        msg.delay = int(msg.info_size / 10)
        if self.type == 'duplex':
            self.message_buffer[str(id)] = msg
        else:
            self.message_buffer = {}
            self.message_buffer[str(id)] = msg
        self.remove_from_buffer(id, msg)

    def try_send_from_node_buffer_to_channel(self, id, msg):
        """
        send from node buffer to channel buffer with correct logic
        :param id: node id
        :return:
        """

        if self.can_send_message(id, msg):
            self.__put_message_to_channel(msg, id)
            return True
        return False

    def send_from_channel_to_buffer(self):
        """
        add message to node buffer after delay and remove from channel buffer
        :return:
        """
        for key, msg in self.message_buffer.items():
            if msg:
                if msg.delay <= 0:
                    if self.__send_message(key, msg):
                        self.add_to_buffer(key, generate_error_message(msg))
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
        if random.random() > self.error_prob:
            if int(key) == self.end_node_id:
                if 'response' in msg.type_message:
                    self.start_node_buffer.insert(0, msg)
                else:
                    self.start_node_buffer.append(msg)
            else:
                if 'response' in msg.type_message:
                    self.end_node_buffer.insert(0, msg)
                else:
                    self.end_node_buffer.append(msg)
            return False
        else:
            statistic_table.add_row('ERROR', msg.from_node, msg.to_node, datetime.datetime.now)
            print('DROPED')
            if msg.type_message == 'datagram':
                return False
            return True

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

    # def __str__(self, *args, **kwargs):
    #     return ','.join((str(value) for value in self.__dict__.values()))
    #
    # def __repr__(self, *args, **kwargs):
    #     cls = self.__class__.__name__
    #     attr = ('%s=%s' % item for item in self.__dict__.items())
    #
    #     return '%s(%s)' % (cls, ', '.join(attr))

    def __eq__(self, other):
        if not isinstance(other, Channel):
            return False
        if other.__dict__ != self.__dict__:
            return False
        return True
        # return super().__eq__(*args, **kwargs)
