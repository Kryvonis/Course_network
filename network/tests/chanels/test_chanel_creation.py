from django.test import TestCase
from network.pkg.chanels.models import Channel
from network.pkg.chanels.serializers import JSONChanelSerializer
import json


class ChanelTestCase(TestCase):
    def test_creation(self):
        obj = Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex')
        self.assertIsNotNone(obj)

    def test_correct_parameters(self):
        obj = Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex')
        self.assertDictEqual(obj.__dict__,
                             {'id': 0,
                              'weight': 0,
                              'fromX': 0,
                              'toX': 0,
                              'fromY': 0,
                              'toY': 0,
                              'start_node_id': 0,
                              'end_node_id': 1,
                              'type': 'Duplex',
                              })

    def test_correct_json(self):
        obj = Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex')
        self.assertEqual(json.loads(json.dumps(obj, cls=JSONChanelSerializer)),
                         json.loads(json.dumps({'id': 0,
                                                'weight': 0,
                                                'fromX': 0,
                                                'toX': 0,
                                                'fromY': 0,
                                                'toY': 0,
                                                'start_node_id': 0,
                                                'end_node_id': 1,
                                                'type': 'Duplex',
                                                })))

    def test_create_from_json(self):
        obj = Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex')
        json_obj = json.dumps(obj, cls=JSONChanelSerializer)
        self.assertEqual(obj,
                         JSONChanelSerializer.decode(json_obj))

    def test_list_creation(self):
        obj = [Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex'),
               Channel(1, 0, 0, 0, 0, 0, 0, 1, 'Duplex')]
        self.assertIsNotNone(obj)

    def test_list_correct_parameters(self):
        obj = [Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex'),
               Channel(1, 0, 0, 0, 0, 0, 0, 1, 'Duplex')]
        for i, _ in enumerate(obj):
            self.assertDictEqual(_.__dict__,
                                 {'id': i,
                                  'weight': 0,
                                  'fromX': 0,
                                  'toX': 0,
                                  'fromY': 0,
                                  'toY': 0,
                                  'start_node_id': 0,
                                  'end_node_id': 1,
                                  'type': 'Duplex',
                                  })

    def test_list_correct_json(self):
        obj = [Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex'),
               Channel(1, 0, 0, 0, 0, 0, 0, 1, 'Duplex')]
        self.assertEqual(json.loads(json.dumps(obj, cls=JSONChanelSerializer)),
                         json.loads(json.dumps([{'id': 0,
                                                 'weight': 0,
                                                 'fromX': 0,
                                                 'toX': 0,
                                                 'fromY': 0,
                                                 'toY': 0,
                                                 'start_node_id': 0,
                                                 'end_node_id': 1,
                                                 'type': 'Duplex',
                                                 },
                                                {'id': 1,
                                                 'weight': 0,
                                                 'fromX': 0,
                                                 'toX': 0,
                                                 'fromY': 0,
                                                 'toY': 0,
                                                 'start_node_id': 0,
                                                 'end_node_id': 1,
                                                 'type': 'Duplex',
                                                 },
                                                ])
                                    )
                         )

    def test_list_create_from_json(self):
        obj = [Channel(0, 0, 0, 0, 0, 0, 0, 1, 'Duplex'),
               Channel(1, 0, 0, 0, 0, 0, 0, 1, 'Duplex')]
        json_obj = json.dumps(obj, cls=JSONChanelSerializer)
        self.assertEqual(obj,
                         JSONChanelSerializer.decode(json_obj))
