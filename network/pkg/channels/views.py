from django.shortcuts import render
from network.pkg.channels.serializers import JSONChanelSerializer
from network.pkg.channels.models import Channel
import json


# Create your views here.
def index(request):
    # obj = Chanel()
    return render(request, 'node/index.html')


def add_channel(request):
    pass


def remove_channel(request):
    pass
