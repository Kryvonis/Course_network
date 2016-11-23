from django.shortcuts import render
from network.pkg.message.sender import statistic_table
from network.pkg.statistic.serializers import JSONStatisticTableSerializer


# Create your views here.

def show_statistic(request):
    statistic = JSONStatisticTableSerializer.encode(statistic_table)
    return render(request, 'statistic/index.html',
                  context={"statistic": statistic})
