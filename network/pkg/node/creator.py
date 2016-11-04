from network.pkg.routing.models import RouteTable
from network.pkg.chanels.models import Channel
from network.pkg.node.models import Node
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.chanels.serializers import JSONChanelSerializer
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
    # if chanels_num > number_of_nodes*(number_of_nodes-1)/2:
    #     raise ValueError
    # make one region
    i = 0
    j = 0
    for id in range(12):
        nodes.append(Node(id, [], [], 120 * i + 50, 120 * j + 50))
        i +=1
        if i == 4:
            j +=1
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
    for id in range(12,24):
        nodes.append(Node(id, [], [], 120 * i + 600, 120 * j + 50))
        i += 1
        if i == 4:
            j += 1
            i = 0

    for i in range(12,24):
        channel = Channel(id=i,
                          weight=weights[random.randint(0, len(weights) - 1)],
                          type='Duplex', start_node_id=i,
                          end_node_id=((i + 1) % 24))
        channels.append(channel)
        nodes[i].channels.append(channel)
        nodes[(i + 1) % 24].channels.append(channel)

    return JSONNodeSerializer.encode(nodes), JSONChanelSerializer.encode(channels)
