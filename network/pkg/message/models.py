from django.db import models


# Create your models here


class Message:
    __id = 0

    def __init__(self, time, from_node, to_node, type_message, info_size, service_size):
        self.id = Message.__id
        Message.__id += 1
        self.time = time
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


if __name__ == '__main__':
    m1 = Message(0, 0, 0, 0, 0, 0)
    print(m1.__dict__)
    print(m1.service_size)
