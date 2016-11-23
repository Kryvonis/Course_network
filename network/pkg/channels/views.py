from django.shortcuts import render, reverse
from network.pkg.node.views import network
from django.http import HttpResponsePermanentRedirect
from network.pkg.channels.creator import generate_channel
import json


# Create your views here.
def index(request):
    # obj = Chanel()
    return render(request, 'node/index.html')


def add_channel(request):
    req = json.loads(request.body.decode('utf-8'))
    if channel_exitst(int(req['start_node_id']), int(req['end_node_id'])):
        return HttpResponsePermanentRedirect(reverse('index-node'))
    channel_add = generate_channel(int(network['channels'][-1].id) + 1, int(req['start_node_id']),
                                   int(req['end_node_id']))
    network['channels'].append(channel_add)
    for node in network['nodes']:
        if node.id == int(req['start_node_id']):
            node.channels.append(channel_add)
        if node.id == int(req['end_node_id']):
            node.channels.append(channel_add)

    return HttpResponsePermanentRedirect(reverse('index-node'))


def channel_exitst(start_node, end_node):
    for _channel in network['channels']:
        if (_channel.start_node_id == start_node and _channel.end_node_id == end_node) or (
                        _channel.start_node_id == end_node and _channel.end_node_id == start_node):
            return True
    return False


def remove_channel(request):
    req = json.loads(request.body.decode('utf-8'))
    start_node_id = int(req['start_node_id'])
    end_node_id = int(req['end_node_id'])
    global_channels_remove_id = 0
    if not channel_exitst(start_node_id, end_node_id):
        return HttpResponsePermanentRedirect(reverse('index-node'))
    for node in network['nodes']:
        if node.id == start_node_id or node.id == end_node_id:
            for _channel in node.channels:
                if (_channel.start_node_id == start_node_id and _channel.end_node_id == end_node_id) \
                        or (_channel.start_node_id == end_node_id and _channel.end_node_id == start_node_id):
                    global_channels_remove_id = _channel
                    node.channels.remove(_channel)
                    break
    network['channels'].remove(global_channels_remove_id)

    return HttpResponsePermanentRedirect(reverse('index-node'))
