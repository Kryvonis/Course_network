from network.pkg.node.creator import generate_randomly
from network.pkg.message.creator import generate_message, generate_new_message
from network.pkg.message.sender import add_message_in_connect, add_message_in_datagram, step, set_statistic_table
from network.pkg.message.views import run
from network.pkg.routing.finder import initialize_short_path
from network.pkg.message.views import has_messages
from network.pkg.statistic.models import StatisticTable
from network.settings import SERVICE_SIZE
iter_node = {'i': 0}
statistic_table = {'0': StatisticTable()}
set_statistic_table(statistic_table['0'])

if __name__ == '__main__':
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    network = {}
    network['nodes'], network['channels'] = generate_randomly(2, 1)
    initialize_short_path(network['nodes'])

    # message = generate_message('0.0', '0.1', 'connect', 10000, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])

    # message = generate_message('1.1', '1.0', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    # #
    # message = generate_message('1.1', '0.0', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    # #
    # message = generate_message('1.0', '0.1', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    #
    # message = generate_message('0.0', '0.1', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    # #
    # message = generate_message('1.0', '0.1', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    #
    # message = generate_message('0.0', '0.1', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    #
    # message = generate_message('1.1', '1.0', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    #
    # message = generate_message('1.1', '0.1', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])
    # #
    # message = generate_message('1.0', '0.1', 'connect', 100, SERVICE_SIZE)
    # add_message_in_connect(message, network['nodes'])

    while statistic_table['0'].message_connect_created_num() < 10:

        message = generate_new_message(network, 'connect', 1000000)
        if message and message.type_message == 'datagram':
            add_message_in_datagram(message, network['nodes'])
        if message and message.type_message == 'connect':
            add_message_in_connect(message, network['nodes'])

        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0

    while has_messages(network['channels']):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    statistic_table['0'].get_statistic()
    print('BP')
    # i = 0
    # while has_messages(network['channels']):
    #     step(iter_node['i'], network['nodes'], network['channels'])
    #     iter_node['i'] += 1
    #     if iter_node['i'] == len(network['nodes']):
    #         iter_node['i'] = 0
