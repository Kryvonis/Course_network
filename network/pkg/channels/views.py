from django.shortcuts import render,reverse
from network.pkg.node.views import network
from network.pkg.channels.serializers import JSONChanelSerializer
from network.pkg.node.creator import generate_channel
import json


# Create your views here.
def index(request):
    # obj = Chanel()
    return render(request, 'node/index.html')


def add_channel(request):
    req = json.loads(request.body.decode('utf-8'))

    print(reverse('channel:index'))
    channel_add = generate_channel(network['channels'][-1]+1,req['start_node'],req['end_node'])
    network['channels'].append(channel_add)
    return HttpResponsePermanentRedirect(reverse('index-node'))


def remove_channel(request, id):
    id = int(id)
    tmp_node = network
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

    return HttpResponsePermanentRedirect(reverse('index-node'))