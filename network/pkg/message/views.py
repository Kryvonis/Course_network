from django.shortcuts import render
from django.http.response import HttpResponse

from network.pkg.message.creator import generate_message
from network.pkg.message.sender import add_message_in_datagram, add_message_in_connect, step, statistic_table
from network.pkg.node.views import network

import json

iter_node = {'i': 0}
iter_number = 1000


# STATISTIC_TABLE = StatisticTable()

# Create your views here.

def send_message_in_datagram(request):
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'datagram', int(req['info_size']))
    add_message_in_datagram(message, network['nodes'])
    # main_loop(network, channels)
    for i in range(iter_number):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    return HttpResponse(200)


def send_message_in_connect(request):
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'connect', int(req['info_size']))
    add_message_in_connect(message, network['nodes'])
    for i in range(iter_number):
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
    for i in range(iter_number):
        step(iter_node['i'], network['nodes'], network['channels'])
        iter_node['i'] += 1
        if iter_node['i'] == len(network['nodes']):
            iter_node['i'] = 0
    return HttpResponse(200)
