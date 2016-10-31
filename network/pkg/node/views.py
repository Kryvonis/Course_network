from django.shortcuts import render
from django.http import HttpResponse
from network.pkg.node.models import Node
from network.pkg.chanels.models import Channel
from network.pkg.routing.models import RouteTable
from network.pkg.node.serializers import JSONNodeSerializer
import json


# Create your views here.
def index(request):
    # generate objects randomly
    rt0 = RouteTable(0, [0, 1], [0, 5], 0)
    rt1 = RouteTable(1, [1, 0], [0, 5], 0)
    chanel1 = Channel(0, 5, 0, 50, 0, 50, 0, 1)

    node0 = Node(0, chanel1, rt0, 0, 0)
    node1 = Node(1, chanel1, rt1, 50, 50)

    network = [node0, node1]
    return render(request, 'node/index.html',
                  context={"network": json.loads(json.dumps(network, cls=JSONNodeSerializer))})
