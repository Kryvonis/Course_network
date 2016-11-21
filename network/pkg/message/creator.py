from network.pkg.message.models import Message
from network.pkg.message.serializers import JSONMessageSerializer


def generate_message(from_node, to_node, type_message, info_size, service_size):
    # TODO add time logic
    time = 0
    message = Message(time, from_node, to_node, type_message, info_size, service_size)
    return message


def generate_message_json(from_node, to_node, type_message, info_size, service_size):
    message = generate_message(from_node, to_node, type_message, info_size, service_size)
    return JSONMessageSerializer.encode(message)
