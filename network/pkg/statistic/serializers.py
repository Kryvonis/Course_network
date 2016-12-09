import json
from network.pkg.statistic.models import StatisticTable


class JSONStatisticTableSerializer:
    @classmethod
    def encode(cls, o):
        if isinstance(o, StatisticTable):
            attr = {
                'total_send': o.delivered_service_num + o.delivered_data_num,
                'total_data_received': o.delivered_data_num,
                'total_service_received': o.delivered_service_num,
                'avrg_delivery_time': "{0:.3f}".format(o.avrg_data_time * 0.001),
                'all_data_size': o.all_data_size,
                'all_service_size': o.all_service_size,
                'rows': o.rows,
            }
            return attr
        if isinstance(o, list):
            nodes = []
            for row in o:
                nodes.append(JSONStatisticTableSerializer.encode(row))
            return nodes

    @classmethod
    def decode(cls, o):
        if isinstance(o, dict):
            st = StatisticTable()
            st.rows = o['rows']
            return st
