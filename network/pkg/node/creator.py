from network.pkg.routing.models import RouteTable
from network.pkg.chanels.models import Channel
from network.pkg.node.models import Node
import random
import math

weights = (1, 2, 3, 4, 5, 6, 7)


def generate_randomly(number_of_nodes):
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
    for i in range(number_of_nodes):
        nodes.append(Node(i, [], [], 500 - random.randint(0,500), 500 - random.randint(0,250)))
    for i in range(number_of_nodes):
        channel = Channel(id=i,
                          weight=weights[random.randint(0, len(weights) - 1)],
                          type='Duplex', start_node_id=i,
                          end_node_id=((i + 1) % number_of_nodes))
        channels.append(channel)
        nodes[i].channels.append(channel)
        nodes[(i + 1) % number_of_nodes].channels.append(channel)

    return nodes, channels
