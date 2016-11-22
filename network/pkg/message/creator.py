from network.pkg.message.models import Message
from network.pkg.message.serializers import JSONMessageSerializer


def generate_message(from_node, to_node, type_message, info_size, service_size=0):
    # TODO add time logic and service_size
    time = 0
    # service_size = 0
    message = Message(time, from_node, to_node, type_message, info_size, service_size)
    return message


def generate_message_json(from_node, to_node, type_message, info_size, service_size):
    message = generate_message(from_node, to_node, type_message, info_size, service_size)
    return JSONMessageSerializer.encode(message)


def split_messages_to_datagrams(message):
    datagrams = []
    if message.info_size % 10 != 0:
        tmp_size = message.info_size % 10
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 message.type_message,
                                 tmp_size,
                                 message.service_size,
                                 ))
    for i in range(int(message.info_size / 10)):
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 message.type_message,
                                 message.info_size,
                                 message.service_size,
                                 ))
    return datagrams
