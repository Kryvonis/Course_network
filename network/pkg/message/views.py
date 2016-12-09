from django.shortcuts import render
from django.http.response import HttpResponse

from network.pkg.message.creator import generate_message, generate_new_message
from network.pkg.message.sender import add_message_in_datagram, add_message_in_connect, step, set_statistic_table
from network.pkg.node.views import network
from network.pkg.statistic.models import StatisticTable
from network.settings.common import SPLITED_SIZE
import json
import math

iter_node = {'i': 0}
iter_number = 100000
statistic_table = {'0': StatisticTable()}
set_statistic_table(statistic_table['0'])


# STATISTIC_TABLE = StatisticTable()

# Create your views here.
def has_messages(channels):
    for channel in channels:
        if channel.end_node_buffer:
            return True
        if channel.start_node_buffer:
            return True
        for key, msg in channel.message_buffer.items():
            if msg:
                return True


def send_message_in_datagram(request):
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'datagram', int(req['info_size']))
    add_message_in_datagram(message, network['nodes'])

    while has_messages(network['channels']):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    return HttpResponse(200)


def add_send_message_in_datagram(request):
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'datagram', int(req['info_size']))
    add_message_in_datagram(message, network['nodes'])

    return HttpResponse(200)


def send_message_in_connect(request):
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    req = json.loads(request.body.decode('utf-8'))
    channels_dump = []
    for channel in network['channels']:
        channels_dump.append(channel.type)
        channel.type = 'halfduplex'
        channel.message_buffer['0'] = 0

    message = generate_message(req['start_node_address'], req['end_node_address'], 'connect', int(req['info_size']))
    add_message_in_connect(message, network['nodes'])
    # statistic_table.delivered_num
    while has_messages(network['channels']):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0

    for i, channel in enumerate(network['channels']):
        if channels_dump[i] == 'duplex':
            channel.message_buffer['{}'.format(channel.start_node_id)] = 0
            channel.message_buffer['{}'.format(channel.end_node_id)] = 0
        channel.type = channels_dump[i]

    return HttpResponse(200)


def add_send_message_in_connect(request):
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'connect', int(req['info_size']))
    add_message_in_connect(message, network['nodes'])
    # statistic_table.delivered_num
    return HttpResponse(200)


def next_iteration(request):
    for i in range(len(network['nodes'])):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    return HttpResponse(200)
    # statistic_table.show()


def run(request, type):
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    req = json.loads(request.body.decode('utf-8'))

    if type == 'datagram':
        while statistic_table['0'].created_data_num < int(req['need']) * math.ceil(
                        int(req['info_size']) / SPLITED_SIZE):

            message = generate_new_message(network, type, int(req['info_size']))
            if message and message.type_message == 'datagram':
                add_message_in_datagram(message, network['nodes'])
            if message and message.type_message == 'connect':
                add_message_in_connect(message, network['nodes'])

            step(iter_node['i'], network['nodes'], network['channels'])
            iter_node['i'] += 1
            if iter_node['i'] == len(network['nodes']):
                iter_node['i'] = 0
    if type == 'connect':

        channels_dump = []
        for channel in network['channels']:
            channels_dump.append(channel.type)
            channel.type = 'halfduplex'
            channel.message_buffer['0'] = 0

        while statistic_table['0'].message_connect_created_num() < int(req['need']):

            message = generate_new_message(network, type, int(req['info_size']))
            if message and message.type_message == 'datagram':
                add_message_in_datagram(message, network['nodes'])
            if message and message.type_message == 'connect':
                add_message_in_connect(message, network['nodes'])

            step(iter_node['i'], network['nodes'], network['channels'])
            iter_node['i'] += 1
            if iter_node['i'] == len(network['nodes']):
                iter_node['i'] = 0

        for i, channel in enumerate(network['channels']):
            if channels_dump[i] == 'duplex':
                channel.message_buffer['{}'.format(channel.start_node_id)] = 0
                channel.message_buffer['{}'.format(channel.end_node_id)] = 0
            channel.type = channels_dump[i]

    while has_messages(network['channels']):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0

    return HttpResponse(200)


def run_simul(request):
    while has_messages(network['channels']):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0

    return HttpResponse(200)
