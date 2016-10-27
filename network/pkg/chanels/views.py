from django.shortcuts import render
from network.pkg.chanels.serializers import ChanelSerializer
from network.pkg.chanels.models import Chanel


# Create your views here.
def index(request):
    return render(request, 'node/index.html', context={'context': ChanelSerializer().encode(Chanel())})
