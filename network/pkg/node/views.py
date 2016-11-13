from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.channels.serializers import JSONChanelSerializer
from network.pkg.node.creator import generate_randomly, generate_node
from network.pkg.routing.finder import initialize
import json
import os

network = {}
# nodes,channels = generate_randomly(8, 2)
# network['nodes'], network['channels'] = JSONNodeSerializer.encode(nodes),JSONChanelSerializer.encode(channels)
# create_rounting_table(nodes)

@ensure_csrf_cookie
def index(request):
    return render(request, 'node/index.html',
                  context={"network": network})


def save_pos(request):
    req = json.loads(request.body.decode('utf-8'))
    network['nodes'] = req['nodes']
    network['channels'] = req['channels']
    return HttpResponse(200)


def add_node(request):
    print(reverse('index-node'))
    network['nodes'].append(generate_node((network['nodes'][-1]['id'] + 1)))
    return HttpResponse(200)


def regenerate(request):
    req = json.loads(request.body.decode('utf-8'))
    network['nodes'], network['channels'] = generate_randomly(int(req['node_nums']), int(req['average_nums']))
    return HttpResponse(200)


def save(request):
    req = json.loads(request.body.decode('utf-8'))
    with open(os.path.join(settings.BASE_DIR, req['filename']), 'w') as f:
        json.dump(network, f)
    return HttpResponse(200)


def load(request):
    req = json.loads(request.body.decode('utf-8'))
    with open(os.path.join(settings.BASE_DIR, req['filename']), 'r') as f:
        load_dump = json.load(f)
        network['nodes'], network['channels'] = load_dump['nodes'], load_dump['channels']
    return HttpResponse(200)


def remove_node(request, id):
    id = int(id)
    global_channels_remove_id = []

    for node in network['nodes']:
        channels_remove_id = []
        if id == node['id']:
            continue
        for _channel in node['channels']:
            if _channel['end_node_id'] == id or _channel['start_node_id'] == id:
                channels_remove_id.append(_channel)
                global_channels_remove_id.append(_channel)
        for rm_channel in channels_remove_id:
            node['channels'].remove(rm_channel)
    for rm_channel in global_channels_remove_id:
        network['channels'].remove(rm_channel)
    # network['nodes']
    for node in network['nodes']:
        if id == node['id']:
            network['nodes'].remove(node)

    for _ in network['nodes']:
        print(_)
    for _ in network['channels']:
        print(_)

    return HttpResponse(204)
