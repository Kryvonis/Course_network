from django.shortcuts import render
from network.pkg.message.sender import statistic_table
from network.pkg.statistic.serializers import JSONStatisticTableSerializer


# Create your views here.

def show_statistic(request):
    statistic_table['0'].get_statistic()
    statistic = JSONStatisticTableSerializer.encode(statistic_table['0'])
    statistic = {'avrg_time': statistic['avrg_time'],
                 'all_data_size': statistic['all_data_size'],
                 'all_service_size': statistic['all_service_size']}
    return render(request, 'statistic/index.html',
                  context={"statistic": statistic})
