from django.shortcuts import render
from network.pkg.chanels.serializers import JSONChanelSerializer
from network.pkg.chanels.models import Channel
import json


# Create your views here.
def index(request):
    pass
    # obj = Chanel()
    # return render(request, 'node/index.html',
    #               context={'context': json.loads(json.dumps(obj, cls=JSONChanelSerializer))})
