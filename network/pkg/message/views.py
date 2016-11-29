from django.shortcuts import render
from django.http.response import HttpResponse

from network.pkg.message.creator import generate_message, generate_new_message
from network.pkg.message.sender import add_message_in_datagram, add_message_in_connect, step, set_statistic_table
from network.pkg.node.views import network
from network.pkg.statistic.models import StatisticTable

import json

iter_node = {'i': 0}
iter_number = 100000
statistic_table = {'0': StatisticTable()}
set_statistic_table(statistic_table['0'])


# STATISTIC_TABLE = StatisticTable()

# Create your views here.

def send_message_in_datagram(request):
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'datagram', int(req['info_size']))
    add_message_in_datagram(message, network['nodes'])

    while statistic_table['0'].delivered_num < statistic_table['0'].created_num:
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    return HttpResponse(200)


def send_message_in_connect(request):
    statistic_table['0'] = StatisticTable()
    set_statistic_table(statistic_table['0'])
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'connect', int(req['info_size']))
    add_message_in_connect(message, network['nodes'])
    # statistic_table.delivered_num
    while statistic_table['0'].delivered_data_num < statistic_table['0'].created_num:
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    return HttpResponse(200)


def next_iteration(request):
    step(iter_node['i'], network['nodes'], network['channels'])
    iter_node['i'] += 1
    if iter_node['i'] == len(network['nodes']):
        iter_node['i'] = 0
    return HttpResponse(200)
    # statistic_table.show()


def run(request):
    req = json.loads(request.body.decode('utf-8'))
    for i in range(int(req['need'])):
        # generate randomly new message
        message = generate_new_message(network)
        if message and message.type_message == 'datagram':
            add_message_in_datagram(message, network['nodes'])
        if message and message.type_message == 'connect':
            add_message_in_connect(message, network['nodes'])
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    return HttpResponse(200)
