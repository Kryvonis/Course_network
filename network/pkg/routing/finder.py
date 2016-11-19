from network.pkg.node.creator import generate_randomly
from network.pkg.routing.models import RouteTable
from network.pkg.node.models import Node
from network.pkg.channels.models import Channel
from math import inf
import random


def dijkstra(nodes, concrete_node, network):
    deleted_nodes = []
    nodes_weight = {}
    neibor_path = {}

    conc_node = find_node(concrete_node, network)
    marked_node = conc_node
    for node in nodes:
        nodes_weight[find_node(node.id, network).address] = inf
        neibor_path[find_node(node.id, network).address] = '{}'.format(find_node(concrete_node, network).address)
    nodes_weight[conc_node.address] = 0

    for i in range(len(nodes)):

        # print('node id = {}'.format(node_i))
        # neibors = []
        for channel in conc_node.channels:
            if channel.start_node_id != conc_node.id:
                neibor_id = channel.start_node_id
            else:
                neibor_id = channel.end_node_id

            if neibor_id in deleted_nodes:
                continue
            if find_node(neibor_id, network).address.split('.')[0] != conc_node.address.split('.')[0]:
                neibor_path[find_node(neibor_id, network).address] = \
                    neibor_path[conc_node.address] + ',' + str(find_node(neibor_id, network).address)
                nodes_weight[find_node(neibor_id, network).address] = \
                    channel.weight + nodes_weight[conc_node.address]
                continue
            # neibors.append(neibor_id)

            if (channel.weight + nodes_weight[conc_node.address]) < nodes_weight[find_node(neibor_id, network).address]:
                neibor_path[find_node(neibor_id, network).address] = \
                    neibor_path[conc_node.address] + ',' + str(find_node(neibor_id, network).address)
                nodes_weight[find_node(neibor_id, network).address] = \
                    channel.weight + nodes_weight[conc_node.address]
                # print('channel id = {}'.format(neibor_id))
                # print('channel_weight = {}'.format(channel.weight))
                # print('nodes_weight = {}'.format(nodes_weight))
                # print('neibor_path = {}'.format(neibor_path))

        # print('neibors = {}'.format(neibors))
        min = inf

        # print('deleted_nodes = {}'.format(deleted_nodes))
        deleted_nodes.append(conc_node.address)

        for key, value in nodes_weight.items():
            if (value < min) and (key not in deleted_nodes) and (
                        key.split('.')[0] == marked_node.address.split('.')[0]):
                conc_node = find_node_by_address(key, network)
                min = value

                # print('=====')
    neibor_path[marked_node.address] = '-'
    table = RouteTable(nodes_weight, neibor_path)
    # print(nodes_weight)
    marked_node.table = table
    # print('neibor_path = {}'.format(neibor_path))


def initialize(network):
    region1 = []
    region2 = []
    for node in network:
        ad = node.address.split('.')[0]
        if node.address.split('.')[0] == '0':
            region1.append(node)
        if node.address.split('.')[0] == '1':
            region2.append(node)
    for node in region1:
        dijkstra(region1, node.id, network)
    for node in region2:
        dijkstra(region2, node.id, network)
    network = region1 + region2
    # print(network)


def find_node(id, network):
    for i in network:
        if i.id == id:
            return i
    return None


def find_node_by_address(addr, network):
    for i in network:
        if i.address == addr:
            return i
    return None


def if_channel_exist(channels, start_node, end_node):
    for i in channels:
        if (i.start_node_id == start_node and i.end_node_id == end_node) or \
                (i.start_node_id == end_node and i.end_node_id == start_node) or \
                (start_node == end_node):
            return True
    return False


if __name__ == '__main__':
    channels = []
    network = []
    i = 0
    j = 0
    for id in range(5):
        network.append(Node(id, [], [], 130 * i + 50, 130 * j + 50, address="0.{}".format(id)))
        i += 1
        if i == 4:
            j += 1
            i = 0
    for i in range(5):
        channel = Channel(id=i,
                          start_node_id=i,
                          end_node_id=((i + 1) % 5),
                          type='Duplex', )
        channels.append(channel)
        network[channel.start_node_id].channels.append(channel)
        network[channel.end_node_id].channels.append(channel)
    for i in range(1000):
        channel = Channel(id=i,
                          type='Duplex',
                          start_node_id=random.randint(0, (int(5) - 1)),
                          end_node_id=random.randint(0, (int(5) - 1))
                          )

    if not if_channel_exist(channels, channel.start_node_id, channel.end_node_id):
        channels.append(channel)
        network[channel.start_node_id].channels.append(channel)
        network[channel.end_node_id].channels.append(channel)
        i += 1
    network, _ = generate_randomly(3, 2)
    # dijkstra(network,0)
    initialize(network)
    print()
    print()
    print(network)
