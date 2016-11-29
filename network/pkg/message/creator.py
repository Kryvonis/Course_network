from network.pkg.message.models import Message
from network.pkg.node.finder import find_node_by_address
from network.pkg.message.serializers import JSONMessageSerializer
import random
import datetime

MESSAGE_PROBABILITY = 0.9


def generate_message(from_node, to_node, type_message, info_size, service_size=32):
    time = 0
    # service_size = 0
    delay = 0
    message = Message(time, from_node, to_node, type_message, info_size, service_size, delay)
    return message


# def generate_message(msg):
#     return Message(datetime.datetime.now(),
#                    msg.from_node,
#                    msg.to_node,
#                    'error',
#                    msg.info_size,
#                    msg.service_size,
#                    msg.delay)


def generate_message_json(from_node, to_node, type_message, info_size, service_size):
    message = generate_message(from_node, to_node, type_message, info_size, service_size)
    return JSONMessageSerializer.encode(message)


def generate_request_to_connect(message):
    return Message(datetime.datetime.now(),
                   message.from_node,
                   message.to_node,
                   'request',
                   0,
                   32,
                   1)


def generate_response_to_connect(message, response_type):
    return Message(datetime.datetime.now(),
                   message.to_node,
                   message.from_node,
                   'response' + response_type,
                   0,
                   32,
                   1)


def generate_new_message(network):
    prob = random.random()
    if prob > MESSAGE_PROBABILITY:
        from_node = random.choice(network['nodes'])
        to_node = random.choice(network['nodes'])
        while from_node == to_node:
            to_node = random.choice(network['nodes'])
        if random.random() > 0.3:
            data = 'connect'
        else:
            data = 'datagram'
        message = generate_message(from_node.address, to_node.address, data, random.randint(256, 512), 32)
        return message


def split_messages_to_datagrams(message):
    datagrams = []
    if message.info_size % 100 != 0:
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 'datagram',
                                 message.info_size % 100,
                                 message.service_size,
                                 message.delay))

    for i in range(int(message.info_size / 100)):
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 'datagram',
                                 100,
                                 message.service_size,
                                 message.delay))
    return datagrams
