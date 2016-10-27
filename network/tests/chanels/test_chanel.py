from django.test import TestCase
from network.pkg.chanels.models import Chanel


class ChanelTestCase(TestCase):
    def test_creation(self):
        obj = Chanel(0, 0, 0, 0, 0, 0, 'duplex')
        self.assertIsNotNone(obj)

    def test_correct_parameters(self):
        obj = Chanel(0, 0, 0, 0, 0, 0, 'duplex')
        self.assertDictEqual(obj.__dict__,
                             {'id': 0,
                              'weight': 0,
                              'fromX': 0,
                              'toX': 0,
                              'fromY': 0,
                              'toY': 0,
                              'type': 'duplex'
                              })
