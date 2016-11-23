from django.db import models


# Create your models here.
class StatisticTable:
    def __init__(self):
        self.rows = []

    def add_row(self, row_type, from_node, to_node, time):
        self.rows.append({'row_type': row_type, 'from_node': from_node,
                          'to_node': to_node, 'time': time})

    def show(self):
        for i in self.rows:
            print('{}\n{} -> {}\n{}\n'.format(i['row_type'], i['from_node'], i['to_node'], i['time']))
