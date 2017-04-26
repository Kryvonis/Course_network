from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.channels.serializers import JSONChanelSerializer
from network.pkg.node.finder import find_node_by_address
from network.pkg.node.creator import generate_randomly, generate_node
from network.pkg.routing.finder import initialize_short_path, send_tables, \
    initialize_node_path

import json
import os


network = {}

network['nodes'], network['channels'] = generate_randomly(12, 4)
network['type'] = 'path'

initialize_short_path(network['nodes'])


# send_tables(network)


@ensure_csrf_cookie
def index(request):
    return render(request, 'node/index.html',
                  context={"network": {
                      "nodes": JSONNodeSerializer.encode(network['nodes']),
                      "channels": JSONChanelSerializer.encode(
                          network['channels'])
                  }
                  }
                  )


def init_nodes(request, type):
    network['type'] = type
    if type == 'path':
        initialize_short_path(network['nodes'])
    else:
        initialize_node_path(network['nodes'], network['channels'])
    # send_tables(network)
    return HttpResponse(200)


def save_pos(request):
    req = json.loads(request.body.decode('utf-8'))
    network['nodes'] = JSONNodeSerializer.decode(req['nodes'])
    network['channels'] = JSONChanelSerializer.decode(req['channels'])
    for node in network['nodes']:
        node.channels = []
    for channel in network['channels']:
        network['nodes'][channel.start_node_id].channels.append(channel)
        network['nodes'][channel.end_node_id].channels.append(channel)

    return HttpResponse(200)


def add_node(request):
    req = json.loads(request.body.decode('utf-8'))

    network['nodes'].append(
        generate_node((network['nodes'][-1].id + 1), req['address'])
    )
    return HttpResponse(200)


def shutdown_node(request):
    req = json.loads(request.body.decode('utf-8'))
    if req['address'].split('.')[1] != '0':
        value = 1
        node = find_node_by_address(req['address'], network['nodes'], mode=1)
        if node.shutdown:
            value = 0
        for channel in node.channels:
            channel.shutdown = value
        node.shutdown = value
        if network['type'] == 'path':
            initialize_short_path(network['nodes'])
        else:
            initialize_node_path(network['nodes'], network['channels'])
        send_tables(network)
    else:
        return HttpResponse(400)
    return HttpResponse(200)


def regenerate(request):
    req = json.loads(request.body.decode('utf-8'))
    network['nodes'], network['channels'] = generate_randomly(
        int(req['node_nums']), int(req['average_nums']))
    if network['type'] == 'path':
        initialize_short_path(network['nodes'])
    else:
        initialize_node_path(network['nodes'], network['channels'])
    # initialize_short_path(network['nodes'])
    return HttpResponse(200)


def save(request):
    req = json.loads(request.body.decode('utf-8'))
    with open(os.path.join(settings.BASE_DIR, req['filename']), 'w') as f:
        json.dump({'nodes': JSONNodeSerializer.encode(network['nodes']),
                   'channels': JSONChanelSerializer.encode(
                       network['channels'])}, f)
    return HttpResponse(200)


def load(request):
    req = json.loads(request.body.decode('utf-8'))
    with open(os.path.join(settings.BASE_DIR, req['filename']), 'r') as f:
        load_dump = json.load(f)

        network['nodes'], network['channels'] = JSONNodeSerializer.decode(
            load_dump['nodes']), \
                                                JSONChanelSerializer.decode(
                                                    load_dump['channels'])
        for node in network['nodes']:
            node.channels = []
        for channel in network['channels']:
            network['nodes'][channel.start_node_id].channels.append(channel)
            network['nodes'][channel.end_node_id].channels.append(channel)
    return HttpResponse(200)


def remove_node(request, id):
    id = int(id)
    global_channels_remove_id = []

    for node in network['nodes']:
        channels_remove_id = []
        if id == node.id:
            continue
        for _channel in node.channels:
            if _channel.end_node_id == id or _channel.start_node_id == id:
                channels_remove_id.append(_channel)
                global_channels_remove_id.append(_channel)
        for rm_channel in channels_remove_id:
            node.channels.remove(rm_channel)
    for rm_channel in global_channels_remove_id:
        network['channels'].remove(rm_channel)
    # network['nodes']
    for node in network['nodes']:
        if id == node.id:
            network['nodes'].remove(node)

    return HttpResponse(204)
