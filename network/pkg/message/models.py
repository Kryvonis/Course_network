from django.db import models


# Create your models here


class Message:
    __id = 0

    def __init__(self, time, from_node, to_node, type_message, info_size, service_size, delay):
        self.id = Message.__id
        Message.__id += 1
        self.time = time
        self.delay = delay
        self.from_node = from_node
        self.to_node = to_node
        self.type_message = type_message
        self.info_size = info_size
        self.service_size = service_size

    def set_id(self, id):
        self.id = id
        Message.__id -= 1

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return 'type:{}'.format(self.type_message)

    def __str__(self):
        return 'from_node:{};\n' \
               'to_node:{};\n' \
               'type_message:{};\n' \
               'info_size:{};\n' \
               'service_size:{};\n'.format(self.from_node, self.to_node,
                                           self.type_message, self.info_size,
                                           self.service_size)

        # def __repr__(self):
        #     return '{};{};{};{};{};'.format(self.from_node, self.to_node, self.type_message, self.info_size,
        #                                     self.service_size)
