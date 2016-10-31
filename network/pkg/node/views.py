from django.shortcuts import render
from django.http import HttpResponse
from network.pkg.node.models import Node
from network.pkg.chanels.models import Channel
from network.pkg.routing.models import RouteTable
from network.pkg.node.serializers import JSONNodeSerializer,JSONNetworkSerializer
from network.pkg.chanels.serializers import JSONChanelSerializer
from network.pkg.node.creator import generate_randomly
import json


# Create your views here.
def index(request):
    network,nodes,channels = generate_randomly()
    # generate objects randomly
    rt0 = RouteTable(0, [0, 1], [0, 5], 0)
    rt1 = RouteTable(1, [1, 0], [0, 5], 0)
    chanel1 = Channel(0, 5, 0, 50, 0, 50, 0, 1)

    node0 = Node(0, chanel1, rt0, 100, 100)
    node1 = Node(1, chanel1, rt1, 300, 300)

    network = [node0, node1]
    context = {'network':json.loads(json.dumps(network, cls=JSONNetworkSerializer)),
               'nodes':[json.loads(json.dumps(node0,cls=JSONNodeSerializer)),
                        json.loads(json.dumps(node1, cls=JSONNodeSerializer))],
               'channels':[json.loads(json.dumps(chanel1,cls=JSONChanelSerializer))]}

    return render(request, 'node/index.html',
                  context={"network": context})
