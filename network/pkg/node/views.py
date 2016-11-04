from django.shortcuts import render, redirect
from django.http import HttpResponse
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.chanels.serializers import JSONChanelSerializer
from network.pkg.node.creator import generate_randomly
import json

network = {}
network['nodes'], network['channels'] = generate_randomly()


# Create your views here.
def index(request):
    return render(request, 'node/index.html',
                  context={"network": network})


def save_pos(request):
    req = json.loads(request.body.decode('utf-8'))
    network['nodes'] = req['nodes']
    network['channels'] = req['channels']
    return HttpResponse(200)


def add_node(request):
    pass


def remove_node(reqest, id):
    # nodes remmove
    for channel in network['nodes'][id].channels:
        network['channels'].pop(id)
    network['nodes'].pop(id)

    return
