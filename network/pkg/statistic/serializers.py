import json
from network.pkg.statistic.models import StatisticTable


class JSONStatisticTableSerializer:
    @classmethod
    def encode(cls, o):
        if isinstance(o, StatisticTable):
            attr = {'rows': o.rows,
                    'avrg_time': o.avrg_time,
                    'all_data_size': o.all_data_size,
                    'all_service_size': o.all_service_size}
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