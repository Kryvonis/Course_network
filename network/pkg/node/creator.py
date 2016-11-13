from network.pkg.routing.models import RouteTable
from network.pkg.channels.models import Channel
from network.pkg.node.models import Node
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.channels.serializers import JSONChanelSerializer
import random
import math


def is_avg_ok(nodes_num, avg_channels_num, channels_num):
    return channels_num <= avg_channels_num * nodes_num / 2


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
    if (avg_channels_num * num % 2 != 0) or (must_be_channels_num > max_channels) or (num > 40):
        raise ValueError
    one_channels = []
    two_channels = []

    for id in range(int(num)):
        nodes.append(Node(id, [], [], 130 * i + 50, 130 * j + 50, address="0.{}".format(id)))
        i += 1
        if i == 4:
            j += 1
            i = 0
    for i in range(int(num)):
        channel = Channel(id=i,
                          start_node_id=i,
                          end_node_id=((i + 1) % int(num)),
                          type='Duplex', )
        one_channels.append(channel)
        nodes[channel.start_node_id].channels.append(channel)
        nodes[channel.end_node_id].channels.append(channel)
    i = 0
    j = 0

    for id in range(int(num), int(num*2)):
        nodes.append(Node(id, [], [], 130 * i + 800, 130 * j + 50,address="1.{}".format(int(id % num))))
        i += 1
        if i == 4:
            j += 1
            i = 0

    for i in range(int(num), int(num*2)):
        channel = Channel(id=i,
                          type='Duplex',
                          start_node_id=i,
                          end_node_id=(int(num) if (i + 1) % int(num*2) == 0 else (i + 1)))
        two_channels.append(channel)
        nodes[channel.start_node_id].channels.append(channel)
        nodes[channel.end_node_id].channels.append(channel)

    i = two_channels[-1].id

    while len(one_channels) < must_be_channels_num:
        channel = Channel(id=i,
                          type='Duplex',
                          start_node_id=random.randint(0, (int(num) - 1)),
                          end_node_id=random.randint(0, (int(num) - 1))
                          )

        if not find_channel(one_channels, channel.start_node_id, channel.end_node_id):
            one_channels.append(channel)
            nodes[channel.start_node_id].channels.append(channel)
            nodes[channel.end_node_id].channels.append(channel)
            i += 1

    while len(two_channels) < must_be_channels_num:
        channel = Channel(id=i,
                          type='Duplex',
                          start_node_id=20 + random.randint(int(num), (int(num*2) - 1)),
                          end_node_id=20 + random.randint(int(num), (int(num*2) - 1))
                          )
        if not find_channel(two_channels, channel.start_node_id, channel.end_node_id):
            two_channels.append(channel)
            nodes[channel.start_node_id].channels.append(channel)
            nodes[channel.end_node_id].channels.append(channel)
            i += 1
    channel = Channel(id=i + 1,
                      type='Duplex',
                      start_node_id=0,
                      end_node_id=num
                      )
    two_channels.append(channel)
    nodes[channel.start_node_id].channels.append(channel)
    nodes[channel.end_node_id].channels.append(channel)
    return nodes, one_channels + two_channels


def generate_node(id,address):
    return JSONNodeSerializer.encode(Node(id, [], [], 120 * id / 12, 120 * id / 12 + 50,address=address))


def generate_channel(id, start_node, end_node):
    return JSONChanelSerializer.encode(Channel(id=id,
                                               type='Duplex',
                                               start_node_id=start_node,
                                               end_node_id=end_node))


def find_channel(channels, start_node, end_node):
    for i in channels:
        if (i.start_node_id == start_node and i.end_node_id == end_node) or \
                (i.start_node_id == end_node and i.end_node_id == start_node) or \
                (start_node == end_node):
            return True
    return False
