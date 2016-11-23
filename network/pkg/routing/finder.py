from network.pkg.node.creator import generate_randomly
from network.pkg.routing.models import RouteTable
from network.pkg.node.models import Node
from network.pkg.node.finder import find_node, find_node_by_address
from network.pkg.channels.finder import find_channel, channel_exist
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

    for i in range(len(nodes) - 1):

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
    main_node_1 = 0
    main_node_2 = 1
    for node in network:
        if node.address.split('.')[0] == '0':
            if node.address.split('.')[1] == '0':
                main_node_1 = node
            region1.append(node)
        if node.address.split('.')[0] == '1':
            if node.address.split('.')[1] == '0':
                main_node_2 = node
            region2.append(node)
    main_channel = find_channel(main_node_1.channels, main_node_1.id, main_node_2.id)
    t = region1[region1.index(main_node_1)].channels
    t.pop(t.index(main_channel))

    t = region2[region2.index(main_node_2)].channels
    t.pop(t.index(main_channel))
    for node in region1:
        if node.address == '0.0':
            continue
        dijkstra(region1, node.id, network)
    for node in region2:
        if node.address == '1.0':
            continue
        dijkstra(region2, node.id, network)
    t = region2[region2.index(main_node_2)].channels
    t.append(main_channel)

    t = region1[region1.index(main_node_1)].channels
    t.append(main_channel)

    dijkstra(region1, main_node_1.id, network)
    dijkstra(region2, main_node_2.id, network)
    network = region1 + region2
    # print(network)

