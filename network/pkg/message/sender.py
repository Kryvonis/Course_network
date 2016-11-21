from network.pkg.node.creator import generate_randomly
from network.pkg.message.creator import generate_message
from network.pkg.message.creator import split_messages_to_datagrams
from network.pkg.routing.finder import initialize
from network.pkg.node.finder import find_node_by_address, find_node
from network.pkg.channels.finder import channel_exist, find_channel


# 0.1 -> 1.2
# 0.1 -> 0.0
# 0.0 -> 1.0
# 1.0 -> 1.2
#

def get_next_node_path(from_node, to_node, current_node):
    if to_node == current_node:
        return 0
    # if from node and to node in different region

    if current_node.address.split('.')[0] != to_node.address.split('.')[0]:

        # check if node sender is main node. If not - need to send to main node and after that send to getter
        if current_node.address.split('.')[1] == '0':
            next_node = current_node.table.path[
                str(to_node.address.split('.')[0] + '.0')
            ].split(',')[1]
        else:
            next_node = current_node.table.path[
                from_node.address.split('.')[0] + '.0'].split(',')[1]
    else:
        next_node = current_node.table.path[to_node.address].split(',')[1]
    return next_node


def send_message_in_datagram(message, network):
    """
    need to send message and return all path of sending
    :param message: what message
    :param network: what network
    :return: path
    """
    node_sender = find_node_by_address(message.from_node, network)
    node_getter = find_node_by_address(message.to_node, network)
    # Node getter from other region
    next_node = get_next_node_path(node_sender, node_getter, node_sender)
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
            pass
            # channes_sender.put_message_to_channel(message, node_sender.id)


def send_message_in_connect(message, network):
    pass


if __name__ == '__main__':
    network, _ = generate_randomly(3, 2)
    initialize(network)
    message = generate_message('0.0', '0.2', 'data', 30, 10)
    send_message_in_datagram(message, network)
