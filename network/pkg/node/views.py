from django.shortcuts import render
from django.http import HttpResponse
from network.pkg.chanels.models import Chanel, ChanelSerializer


# Create your views here.
def index(request):
    return render(request, 'node/index.html', context=ChanelSerializer().encode(Chanel()))
