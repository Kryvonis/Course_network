from network.pkg.routing.models import RouteTable
from network.pkg.channels.models import Channel
from network.pkg.node.models import Node
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.channels.serializers import JSONChanelSerializer
import random
import math

weights = (1, 2, 3, 4, 5, 6, 7)


def generate_randomly():
    """
    Create random network
    :return: network,nodes,channels
    """
    channels = []
    # n*(n+1)/2 = 4 * 3 / 2 = 6
    # Максимальное количество каналов это количетсво вершин(num_of_nodes) + sum(num_of_nodes_2 -> 2)
    nodes = []
    i = 0
    j = 0
    ##
    # TEST
    ##

    # for id in range(3):
    #     nodes.append(Node(id, [], [], 120 * i + 50, 120 * j + 50))
    #     i += 1
    #     if i == 4:
    #         j += 1
    #         i = 0
    #
    # for i in range(3):
    #     channel = Channel(id=i,
    #                         weight = weights[random.randint(0, len(weights) - 1)],
    #                         type = 'Duplex', start_node_id = i,
    #                         end_node_id = ((i + 1) % 3))
    #     channels.append(channel)
    #     nodes[i].channels.append(channel)
    #     nodes[(i + 1) % 3].channels.append(channel)
    #

    ##
    # PROD
    ##

    for id in range(12):
        nodes.append(Node(id, [], [], 120 * i + 50, 120 * j + 50))
        i += 1
        if i == 4:
            j += 1
            i = 0
    for i in range(12):
        channel = Channel(id=i,
                          weight=weights[random.randint(0, len(weights) - 1)],
                          type='Duplex', start_node_id=i,
                          end_node_id=((i + 1) % 12))
        channels.append(channel)
        nodes[i].channels.append(channel)
        nodes[(i + 1) % 12].channels.append(channel)
    i = 0
    j = 0
    for id in range(12, 24):
        nodes.append(Node(id, [], [], 120 * i + 600, 120 * j + 50))
        i += 1
        if i == 4:
            j += 1
            i = 0

    for i in range(12, 24):
        channel = Channel(id=i,
                          weight=weights[random.randint(0, len(weights) - 1)],
                          type='Duplex', start_node_id=i,
                          end_node_id=((i + 1) % 24))
        channels.append(channel)
        nodes[i].channels.append(channel)
        nodes[(i + 1) % 24].channels.append(channel)

    return JSONNodeSerializer.encode(nodes), JSONChanelSerializer.encode(channels)


def generate_node(id):
    return JSONNodeSerializer.encode(Node(id, [], [], 120 * id / 12, 120 * id / 12 + 50))


def generate_channel(id,start_node,end_node):
    return JSONChanelSerializer.encode(Channel(id=id,
                                               weight=weights[random.randint(0, len(weights) - 1)],
                                               type='Duplex',
                                               start_node_id=start_node,
                                               end_node_id=end_node))