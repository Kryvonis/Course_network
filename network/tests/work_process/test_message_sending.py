from network.pkg.node.creator import generate_randomly
from network.pkg.message.creator import generate_message
from network.pkg.message.models import Message
from network.pkg.message.creator import split_messages_to_datagrams
from network.pkg.routing.finder import initialize
from network.pkg.node.finder import find_node_by_address, find_node
from network.pkg.channels.finder import channel_exist, find_channel


def send_message_in_datagram(message, network):
    node_sender = find_node_by_address(message.from_node, network)
    node_getter = find_node_by_address(message.to_node, network)
    path = node_sender.table.path[node_getter.address].split(',')
    next_node = path[1]
    channes_sender = find_channel(node_sender.channels, node_sender.id,
                                  find_node_by_address(next_node, network).id)

    # added message to start buffer
    datagrams = split_messages_to_datagrams(message)
    for i in datagrams:
        channes_sender.add_to_buffer(node_sender.id, i)
        # check if can send
        if channes_sender.can_send_message(node_sender.id):
            # send to channel buffer
            channes_sender.put_message_to_channel(i, node_sender.id)

    # add to end buffer
    channes_sender.send_from_channel_to_buffer()

    # read message
    for channel in node_getter.channels:
        buffer = channel.get_node_buffer(node_getter.id)
        if buffer:
            print(buffer[0])

            # channes_sender.put_message_to_channel(message, node_sender.id)


if __name__ == '__main__':
    network, _ = generate_randomly(3, 2)
    initialize(network)
    message = generate_message('0.0', '0.2', 'data', 30, 10)
    send_message_in_datagram(message, network)
