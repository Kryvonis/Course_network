from django.db import models
import datetime


# Create your models here.
class StatisticTable:
    def __init__(self):
        self.rows = []
        self.message_nums = 0
        self.created_service_message = []
        self.created_data_message = []
        self.delivered_service_message = []
        self.delivered_data_message = []
        self.connect_created_num = 0
        self.delivered_service_num = len(self.delivered_service_message)
        self.delivered_data_num = len(self.delivered_data_message)
        self.created_service_num = len(self.created_service_message)
        self.created_data_num = len(self.created_data_message)
        self.avrg_service_time = 0
        self.avrg_data_time = 0
        self.all_data_size = 0
        self.all_service_size = 0

    def add_row(self, row_type, from_node, to_node, time):
        self.rows.append({'row_type': row_type, 'from_node': from_node,
                          'to_node': to_node, 'time': time})

    def message_connect_created_num(self):
        return self.connect_created_num

    def message_add(self, msg):
        if msg.type_message == 'connect':
            self.connect_created_num += 1
            return
        if ('data' in msg.type_message):
            self.created_data_message.append(msg)
            # self.created_data_num = len(self.created_data_message)
            self.created_data_num += 1
        else:
            self.created_service_message.append(msg)
            # self.created_service_num = len(self.created_service_message)
            self.created_service_num += 1

    def message_delivered(self, msg):
        if msg.type_message == 'connect':
            return
        msg.time = (datetime.datetime.now() - msg.time).microseconds
        if ('data' in msg.type_message):
            self.delivered_data_message.append(msg)
            # self.delivered_data_num += len(self.delivered_data_message)
            self.delivered_data_num += 1
        else:
            self.delivered_service_message.append(msg)
            # self.delivered_service_num = len(self.delivered_service_message)
            self.delivered_service_num += 1

    def get_statistic(self):
        self.avrg_time = 0
        self.all_data_size = 0
        self.all_service_size = 0

        for msg in self.delivered_service_message:
            self.all_service_size += msg.service_size
        for msg in self.delivered_data_message:
            self.all_data_size += msg.info_size
            self.all_service_size += msg.service_size
            self.avrg_data_time += msg.time
        try:
            self.avrg_data_time /= self.delivered_data_num
        except ZeroDivisionError:
            self.avrg_time = 0


            # total send message
            # total received message
            # total data received message
            # avg time all message
            # avg time data message
            # total size received message
            # total size received data message
