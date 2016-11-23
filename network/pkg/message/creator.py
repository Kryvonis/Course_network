from network.pkg.message.models import Message
from network.pkg.message.serializers import JSONMessageSerializer


def generate_message(from_node, to_node, type_message, info_size, service_size=0):
    # TODO add time logic and service_size
    time = 0
    # service_size = 0
    delay = 0
    message = Message(time, from_node, to_node, type_message, info_size, service_size, delay)
    return message


def generate_message_json(from_node, to_node, type_message, info_size, service_size):
    message = generate_message(from_node, to_node, type_message, info_size, service_size)
    return JSONMessageSerializer.encode(message)


def split_messages_to_datagrams(message):
    datagrams = []
    if message.info_size % 10 != 0:
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 message.type_message,
                                 message.info_size % 10,
                                 message.service_size,
                                 message.delay))

    for i in range(int(message.info_size / 10)):
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 message.type_message,
                                 10,
                                 message.service_size,
                                 message.delay))
    return datagrams
