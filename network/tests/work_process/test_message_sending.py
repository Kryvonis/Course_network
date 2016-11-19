from network.pkg.node.creator import generate_randomly
from network.pkg.message.creator import generate_message
from network.pkg.message.models import Message
from network.pkg.node.finder import find_node_by_address, find_node
from network.pkg.channels.finder import channel_exist, find_channel


def split_messages(message):
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


def send_message_in_datagram(message, network):
    node_sender = find_node_by_address(message.from_node, network)
    channes_sender = find_channel(node_sender.channels, message.from_node, message.to_node)
    datagrams = split_messages(message)


if __name__ == '__main__':
    network, _ = generate_randomly(2, 1)
    message = generate_message('0.0', '0.1', 'data', 100, 10)
    send_message_in_datagram(message, network)
