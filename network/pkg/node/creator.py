from network.pkg.routing.models import RouteTable
from network.pkg.channels.models import Channel
from network.pkg.channels.creator import generate_channel
from network.pkg.node.models import Node
from network.pkg.node.serializers import JSONNodeSerializer
import random


def generate_randomly(num, avg_channels_num):
    """
    Create random network
    :return: network,nodes,channels
    """
    max_channels = int(int(num) * (int(num) - 1) / 2)
    nodes = []
    i = 0
    j = 0
    must_be_channels_num = int((avg_channels_num * num) / 2)
    if (avg_channels_num * num % 2 != 0) or (
        must_be_channels_num > max_channels) or (num > 40):
        raise ValueError
    one_channels = []
    two_channels = []

    for id in range(int(num)):
        nodes.append(Node(id, [], [], 130 * i + 50, 130 * j + 50,
                          address="0.{}".format(id)))
        i += 1
        if i == 4:
            j += 1
            i = 0
    for i in range(int(num - 1)):
        channel = generate_channel(id=i, start_node=i,
                                   end_node=((i + 1) % int(num)))
        one_channels.append(channel)
        nodes[channel.start_node_id].channels.append(channel)
        nodes[channel.end_node_id].channels.append(channel)
    i = 0
    j = 0

    for id in range(int(num), int(num * 2)):
        nodes.append(Node(id, [], [], 130 * i + 800, 130 * j + 50,
                          address="1.{}".format(int(id % num))))
        i += 1
        if i == 4:
            j += 1
            i = 0

    for i in range(int(num), int(num * 2 - 1)):
        channel = generate_channel(id=i,
                                   start_node=i,
                                   end_node=(int(num) if (i + 1) % int(
                                       num * 2) == 0 else (i + 1)))
        two_channels.append(channel)
        nodes[channel.start_node_id].channels.append(channel)
        nodes[channel.end_node_id].channels.append(channel)

    i = two_channels[-1].id

    while len(one_channels) < must_be_channels_num:
        channel = generate_channel(id=i,
                                   start_node=random.randint(0,
                                                             (int(num) - 1)),
                                   end_node=random.randint(0, (int(num) - 1)))

        if not find_channel(one_channels, channel.start_node_id,
                            channel.end_node_id):
            one_channels.append(channel)
            nodes[channel.start_node_id].channels.append(channel)
            nodes[channel.end_node_id].channels.append(channel)
            i += 1

    while len(two_channels) < must_be_channels_num:
        channel = generate_channel(id=i,
                                   start_node=random.randint(int(num), (
                                   int(num * 2) - 1)),
                                   end_node=random.randint(int(num),
                                                           (int(num * 2) - 1)))
        if not find_channel(two_channels, channel.start_node_id,
                            channel.end_node_id):
            two_channels.append(channel)
            nodes[channel.start_node_id].channels.append(channel)
            nodes[channel.end_node_id].channels.append(channel)
            i += 1
    channel = generate_channel(id=i + 1,
                               start_node=0,
                               end_node=num)
    two_channels.append(channel)
    nodes[channel.start_node_id].channels.append(channel)
    nodes[channel.end_node_id].channels.append(channel)
    return nodes, one_channels + two_channels


def generate_node(id, address):
    # Node(id, [], [], 120 * id / 12, 120 * id / 12 + 50, address=address)
    return Node(id, [], [], 120 * id / 12, 120 * id / 12 + 50, address=address)


def find_channel(channels, start_node, end_node):
    for i in channels:
        if (i.start_node_id == start_node and i.end_node_id == end_node) or \
                (
                        i.start_node_id == end_node and i.end_node_id == start_node) or \
                (start_node == end_node):
            return True
    return False
