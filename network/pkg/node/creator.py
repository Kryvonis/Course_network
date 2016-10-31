from network.pkg.routing.models import RouteTable
from network.pkg.chanels.models import Channel
from network.pkg.node.models import Node
weights = (1,2,3,4,5,6,7)


def generate_randomly():
    """
    Create random network
    :return: network,nodes,channels
    """
    channels = []

    for i in range(5):
        channels.append(Channel(i,weights[i],))
    for i in range(5):
        route_tables.append(RouteTable(i, [i, ], [0, ], i))

    for i in range(1,5):

        RouteTable(i, [i, ], [0, ], i)
        Channel(i,weights[i-1],10*i,50*i,10*i,50*i,i,i+1)

        # Node(i,,,10*i,10*i)

    rt0 = RouteTable(0, [0, 1], [0, 5], 0)
    rt1 = RouteTable(1, [1, 0], [0, 5], 0)
    chanel1 = Channel(0, 5, 0, 50, 0, 50, 0, 1)

    node0 = Node(0, chanel1, rt0, 100, 100)
    node1 = Node(1, chanel1, rt1, 300, 300)

    network = [node0, node1]
    return network