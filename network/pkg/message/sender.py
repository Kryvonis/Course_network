from network.pkg.message.creator import generate_message, split_messages_to_datagrams
from network.pkg.node.finder import find_node_by_address
from network.pkg.channels.finder import find_channel
from network.pkg.statistic.models import StatisticTable
import random
import datetime

CYCLE_COUNT = 200
statistic_table = StatisticTable()
iter_node = 0
MESSAGE_PROBABILITY = 0.5


def generate_new_message(network):
    prob = random.random()
    if prob > MESSAGE_PROBABILITY:
        from_node = random.choice(network)
        to_node = random.choice(network)
        while from_node == to_node:
            to_node = random.choice(network)
        data = '{} -> {}'.format(from_node.address, to_node.address)
        message = generate_message(from_node.address, to_node.address, data, 100, 20)
        add_message_in_datagram(message, network)


def step(i, network, network_channels):
    # generate_new_message(network)
    # ITER_NODE += 1
    #
    # if  == len(network):
    #     ITER_NODE = 0
    # else:
    #     ITER_NODE += 1
    current_node = network[i]

    for channel in current_node.channels:
        buffer = channel.get_node_buffer(current_node.id)
        if buffer:
            if buffer[0].to_node == current_node.address:
                statistic_table.add_row(
                    'read message [type:{};size:{};service size{};creating time:{};delivery time:{}]'.
                        format(buffer[0].type_message, buffer[0].info_size,
                               buffer[0].service_size, buffer[0].time,
                               (datetime.datetime.now() - buffer[0].time).microseconds),
                    buffer[0].from_node,
                    buffer[0].to_node,
                    datetime.datetime.now()
                )
                channel.remove_from_buffer(current_node.id, buffer[0])
                # return
            else:
                node_sender = find_node_by_address(buffer[0].from_node, network)
                node_getter = find_node_by_address(buffer[0].to_node, network)
                next_node = find_node_by_address(get_next_node_path(node_sender, node_getter, current_node),
                                                 network)
                channel_sender = find_channel(current_node.channels, current_node.id,
                                              next_node.id)
                if channel_sender != channel:
                    # get from one buffer and sent to another buffer on node
                    statistic_table.add_row('send from one buffer to another',
                                            current_node.address,
                                            next_node.address,
                                            datetime.datetime.now()
                                            )
                    channel_sender.add_to_buffer(current_node.id, buffer[0])
                    channel.remove_from_buffer(current_node.id, buffer[0])
                    if channel_sender.try_send_from_node_buffer_to_channel(current_node.id):
                        statistic_table.add_row('send message using channel between',
                                                current_node.address,
                                                next_node.address,
                                                datetime.datetime.now()
                                                )
                else:
                    if channel_sender.try_send_from_node_buffer_to_channel(current_node.id):
                        statistic_table.add_row('send message using channel between',
                                                current_node.address,
                                                next_node.address,
                                                datetime.datetime.now()
                                                )

    for channel in network_channels:
        channel.send_from_channel_to_buffer()


def get_next_node_path(from_node, to_node, current_node):
    """
    :param from_node: Node model
    :param to_node: Node model
    :param current_node: Node model
    :return:
    """
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


def message_delivered():
    pass


def add_message_in_datagram(message, network):
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

    message.time = datetime.datetime.now()
    datagrams = split_messages_to_datagrams(message)
    for i in datagrams:
        channes_sender.add_to_buffer(node_sender.id, i)
        statistic_table.add_row('create new message with data size {}'.format(i.info_size),
                                i.from_node,
                                i.to_node,
                                datetime.datetime.now()
                                )


def send_message_in_connect(message, network):
    pass
