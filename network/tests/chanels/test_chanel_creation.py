from django.test import TestCase
from network.pkg.channels.models import Channel
from network.pkg.channels.serializers import JSONChanelSerializer
import json


class ChanelTestCase(TestCase):
    def test_creation(self):
        obj = Channel(0, 0, 0, 1, 'Duplex')
        self.assertIsNotNone(obj)

    def test_correct_parameters(self):
        obj = Channel(0, 0, 0, 1, 'Duplex')
        self.assertDictEqual(obj.__dict__,
                             {'id': 0,
                              'weight': 0,
                              'start_node_id': 0,
                              'end_node_id': 1,
                              'type': 'Duplex',
                              })

    def test_correct_json(self):
        obj = Channel(0, 0,  0, 1, 'Duplex')
        self.assertEqual(JSONChanelSerializer.encode(obj),
                         {'id': 0,
                          'weight': 0,
                          'start_node_id': 0,
                          'end_node_id': 1,
                          'type': 'Duplex',
                          })

    def test_create_from_json(self):
        obj = Channel(0, 0, 0, 1, 'Duplex')
        self.assertEqual(obj,
                         JSONChanelSerializer.decode(JSONChanelSerializer.encode(obj)))

    def test_list_creation(self):
        obj = [Channel(0, 0, 0, 1, 'Duplex'),
               Channel(1, 0, 0, 1, 'Duplex')]
        self.assertIsNotNone(obj)

    def test_list_correct_json(self):
        obj = [Channel(0, 0, 0, 1, 'Duplex'),
               Channel(1, 0, 0, 1, 'Duplex')]
        self.assertEqual(JSONChanelSerializer.encode(obj),
                         [{'id': 0,
                           'weight': 0,
                           'start_node_id': 0,
                           'end_node_id': 1,
                           'type': 'Duplex',
                           },
                          {'id': 1,
                           'weight': 0,
                           'start_node_id': 0,
                           'end_node_id': 1,
                           'type': 'Duplex',
                           },
                          ])

    def test_list_create_from_json(self):
        obj = [Channel(0, 0, 0, 1, 'Duplex'),
               Channel(1, 0, 0, 1, 'Duplex')]
        json_obj = JSONChanelSerializer.encode(obj)
        self.assertEqual(obj,
                         JSONChanelSerializer.decode(json_obj))
