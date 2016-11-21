from django.shortcuts import render
from django.http.response import HttpResponse

from network.pkg.message.creator import generate_message
from network.pkg.message.sender import send_message_in_datagram as smid
from network.pkg.message.sender import send_message_in_connect as smic
from network.pkg.node.views import network

import json


# Create your views here.

def send_message_in_datagram(request):
    req = json.loads(request.body.decode('utf-8'))
    message = generate_message(req['start_node_address'], req['end_node_address'], 'data', int(req['info_size']))
    # smid()
    print(req['start_node_address'])
    print(req['end_node_address'])
    return HttpResponse(200)


def send_message_in_connect(request):
    return HttpResponse(200)
