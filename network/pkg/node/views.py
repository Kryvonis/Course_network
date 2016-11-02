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
    # network,nodes,channels = generate_randomly()
    # generate objects randomly
    # rt0 = RouteTable(0, [0, 1], [0, 5], 0)
    # rt1 = RouteTable(1, [1, 0], [0, 5], 0)
    # chanel1 = Channel(0, 5, 0, 1)
    #
    # node0 = Node(0, [chanel1], rt0, 100, 100)
    # node1 = Node(1, [chanel1], rt1, 300, 300)
    #
    # network.append(node0)
    # network.append(node1)

    # context = {'network': JSONNetworkSerializer.encode(network),
    #            'nodes': JSONNetworkSerializer.encode(network),
    #            'channels': [JSONChanelSerializer.encode(chanel1)]}
    nodes, channels = generate_randomly(5)
    network['nodes'] = nodes
    network['channels'] = channels
    context = {'nodes': JSONNodeSerializer.encode(nodes),
               'channels': JSONChanelSerializer.encode(channels)}
    print(len(network))
    return render(request, 'node/index.html',
                  context={"network": context})
