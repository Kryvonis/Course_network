from network.pkg.message.models import Message
from network.pkg.node.finder import find_node_by_address
from network.pkg.message.serializers import JSONMessageSerializer
from network.settings.common import SPLITED_SIZE, SERVICE_SIZE
import random
import datetime


MESSAGE_PROBABILITY = 0.5


def generate_message(from_node, to_node, type_message, info_size,
                     service_size=SERVICE_SIZE):
    time = datetime.datetime.now()

    delay = 0
    message = Message(time, from_node, to_node, type_message, info_size,
                      service_size, delay)
    return message


def generate_message_json(from_node, to_node, type_message, info_size,
                          service_size):
    message = generate_message(from_node, to_node, type_message, info_size,
                               service_size)
    return JSONMessageSerializer.encode(message)


def generate_request_to_connect(message):
    return Message(datetime.datetime.now(),
                   message.from_node,
                   message.to_node,
                   'request',
                   0,
                   SERVICE_SIZE,
                   1)


def generate_response_to_connect(message, response_type):
    return Message(datetime.datetime.now(),
                   message.to_node,
                   message.from_node,
                   'response' + response_type,
                   0,
                   SERVICE_SIZE,
                   1)


def generate_response_to_datagram(message, response_type):
    return Message(datetime.datetime.now(),
                   message.to_node,
                   message.from_node,
                   response_type,
                   0,
                   SERVICE_SIZE,
                   1)


def generate_new_message(network, type, size):
    prob = random.random() + 0.1
    if prob > MESSAGE_PROBABILITY:
        from_node = random.choice(network['nodes'])
        to_node = random.choice(network['nodes'])
        while from_node.address == to_node.address:
            to_node = random.choice(network['nodes'])
        message = generate_message(from_node.address, to_node.address, type,
                                   size, SERVICE_SIZE)
        return message


def generate_same_message(msg):
    return Message(msg.time,
                   msg.from_node,
                   msg.to_node,
                   msg.type_message,
                   msg.info_size,
                   msg.service_size,
                   msg.delay)


def split_messages_to_datagrams(message, message_type):
    datagrams = []
    if message.info_size % SPLITED_SIZE != 0:
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 message_type,
                                 message.info_size % SPLITED_SIZE,
                                 message.service_size,
                                 message.delay))

    for i in range(int(message.info_size / SPLITED_SIZE)):
        datagrams.append(Message(message.time,
                                 message.from_node,
                                 message.to_node,
                                 message_type,
                                 SPLITED_SIZE,
                                 message.service_size,
                                 message.delay))
    return datagrams
