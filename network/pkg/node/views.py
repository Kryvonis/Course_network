from django.shortcuts import render
from django.http import HttpResponse
from network.pkg.node.models import Node
from network.pkg.chanels.models import Channel
from network.pkg.routing.models import RouteTable
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.chanels.serializers import JSONChanelSerializer
from network.pkg.node.creator import generate_randomly
import json

network = {}


# Create your views here.
def index(request):
    nodes, channels = generate_randomly(12)
    network['nodes'] = nodes
    network['channels'] = channels
    context = {'nodes': JSONNodeSerializer.encode(nodes),
               'channels': JSONChanelSerializer.encode(channels)}
    print(len(nodes))
    return render(request, 'node/index.html',
                  context={"network": context})


def add_node(request):
    pass


def remove_node(reqest, id):
    # nodes remmove
    for channel in network['nodes'][id].channels:
        network['channels'].pop(id)
    network['nodes'].pop(id)

    return
