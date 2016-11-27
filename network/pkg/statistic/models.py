from django.db import models


# Create your models here.
class StatisticTable:
    def __init__(self):
        self.rows = []
        self.message_nums = 0
        self.created_message = []
        self.delivered_message = []
        self.delivered_data_message = []
        self.delivered_data_num = 0
        self.created_num = len(self.created_message)
        self.delivered_num = len(self.delivered_message)
        self.avrg_time = 0
        self.all_data_size = 0
        self.all_service_size = 0

    def add_row(self, row_type, from_node, to_node, time):
        self.rows.append({'row_type': row_type, 'from_node': from_node,
                          'to_node': to_node, 'time': time})

    def message_add(self, msg):
        self.created_message.append(msg)
        self.created_num = len(self.created_message)

    def message_delivered(self, msg):
        self.delivered_message.append(msg)
        if 'data' in msg.type_message:
            self.delivered_data_message.append(msg)
            self.delivered_data_num = len(self.delivered_data_message)
        self.delivered_num = len(self.delivered_message)

    def get_statistic(self):
        self.created_num = len(self.created_message)
        self.delivered_num = len(self.delivered_message)
        self.avrg_time = 0
        self.all_data_size = 0
        self.all_service_size = 0
        for msg in self.delivered_message:
            self.avrg_time += msg.time
            self.all_data_size += msg.info_size
            self.all_service_size += msg.service_size
        try:
            self.avrg_time /= self.delivered_num
        except ZeroDivisionError:
            self.avrg_time = 0

    def show(self):
        for i in self.rows:
            print('{}\n{} -> {}\n{}\n'.format(i['row_type'], i['from_node'], i['to_node'], i['time']))