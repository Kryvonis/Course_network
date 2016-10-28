from django.test import TestCase
from network.pkg.chanels.models import Chanel
from network.pkg.chanels.serializers import JSONChanelSerializer
import json


class ChanelTestCase(TestCase):
    def test_creation(self):
        obj = Chanel(0, 0, 0, 0, 0, 0, 'Duplex')
        self.assertIsNotNone(obj)

    def test_correct_parameters(self):
        obj = Chanel(0, 0, 0, 0, 0, 0, 'Duplex')
        self.assertDictEqual(obj.__dict__,
                             {'id': 0,
                              'weight': 0,
                              'fromX': 0,
                              'toX': 0,
                              'fromY': 0,
                              'toY': 0,
                              'type': 'Duplex',
                              })

    def test_correct_json(self):
        obj = Chanel(0, 0, 0, 0, 0, 0, 'Duplex')
        self.assertEqual(json.dumps(obj, cls=JSONChanelSerializer),
                         json.dumps({'id': 0,
                                     'weight': 0,
                                     'fromX': 0,
                                     'toX': 0,
                                     'fromY': 0,
                                     'toY': 0,
                                     'type': 'Duplex',
                                     }))

    def test_create_from_json(self):
        obj = Chanel(0, 0, 0, 0, 0, 0, 'Duplex')
        json_obj = json.dumps(obj, cls=JSONChanelSerializer)
        self.assertEqual(obj,
                         JSONChanelSerializer.decode(json_obj))
