from django.shortcuts import render
from network.pkg.message.sender import statistic_table
from network.pkg.statistic.serializers import JSONStatisticTableSerializer


# Create your views here.

def show_statistic(request):
    statistic_table['0'].get_statistic()
    statistic = JSONStatisticTableSerializer.encode(statistic_table['0'])
    statistic = {
        'total_send': statistic['total_send'],
        'total_data_received': statistic['total_data_received'],
        'total_service_received': statistic['total_service_received'],
        'avrg_delivery_time': statistic['avrg_delivery_time'],
        'all_data_size': statistic['all_data_size'],
        'all_service_size': statistic['all_service_size'],
        # 'rows':statistic['rows']
    }
    return render(request, 'statistic/index.html',
                  context={"statistic": statistic})


def show_steps(request):
    statistic_table['0'].get_statistic()
    statistic = JSONStatisticTableSerializer.encode(statistic_table['0'])
    statistic = {
        'rows': statistic['rows']
    }
    return render(request, 'statistic/rows.html',
                  context={"statistic": statistic})
