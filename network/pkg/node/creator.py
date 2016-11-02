from network.pkg.routing.models import RouteTable
from network.pkg.chanels.models import Channel
from network.pkg.node.models import Node
import random

weights = (1, 2, 3, 4, 5, 6, 7)


def generate_randomly(number_of_nodes):
    """
    Create random network
    :return: network,nodes,channels
    """
    # X -> 500, 625, 750, 625, 500, 375, 250, 375
    # Y -> 250, 375, 500, 625, 750, 625, 500, 375
    channels = []
    # n*(n+1)/2 = 4 * 3 / 2 = 6
    # Максимальное количество каналов это количетсво вершин(num_of_nodes) + sum(num_of_nodes_2 -> 2)
    nodes = []

    # if chanels_num > number_of_nodes*(number_of_nodes-1)/2:
    #     raise ValueError
    # make one region
    for i in range(number_of_nodes):
        nodes.append(Node(i, [], [], 250 + 50 * i, 250 + 50 * i))
    for i in range(number_of_nodes):
        channel = Channel(id=i,
                          weight=weights[random.randint(0, len(weights) - 1)],
                          type='Duplex', start_node_id=i,
                          end_node_id=((i + 1) % number_of_nodes))
        channels.append(channel)
        nodes[i].channels.append(channel)
        nodes[(i + 1) % number_of_nodes].channels.append(channel)

    return nodes, channels
    # for i in range(int(number_of_nodes * (number_of_nodes - 1) / 2)):
    #     Channel(i,
    #             weights[random.randint(0, len(weights) - 1)],
    #             type='Duplex',
    #             start_node_id=i,
    #             end_node_id=i + 1,
    #             )

    # for i in range(5):
    #     route_tables.append(RouteTable(i, [i, ], [0, ], i))

    for i in range(1, 5):
        RouteTable(i, [i, ], [0, ], i)
        Channel(i, weights[i - 1], 10 * i, 50 * i, 10 * i, 50 * i, i, i + 1)

        # Node(i,,,10*i,10*i)

    rt0 = RouteTable(0, [0, 1], [0, 5], 0)
    rt1 = RouteTable(1, [1, 0], [0, 5], 0)
    chanel1 = Channel(0, 5, 0, 50, 0, 50, 0, 1)

    node0 = Node(0, chanel1, rt0, 100, 100)
    node1 = Node(1, chanel1, rt1, 300, 300)

    nodes = [node0, node1]
    return nodes
