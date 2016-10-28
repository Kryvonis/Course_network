from django.test import TestCase
from network.pkg.node.models import Node
from network.pkg.routing.models import RouteTable
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.routing.serializers import JSONRouteTableSerializer
import json


class ChanelTestCase(TestCase):
    def setUp(self):
        self.rout_table = RouteTable(0, [], [], [])

    def test_creation(self):
        obj = Node(0, [], self.rout_table, 0, 0)
        self.assertIsNotNone(obj)

    def test_correct_parameters(self):
        obj = Node(0, [], self.rout_table, 0, 0)
        self.assertDictEqual(obj.__dict__,
                             {'id': 0,
                              'table': self.rout_table,
                              'X': 0,
                              'Y': 0,
                              'chanels': [],
                              })

    def test_correct_json(self):
        obj = Node(0, [], self.rout_table, 0, 0)
        self.assertEqual(json.dumps(obj, cls=JSONNodeSerializer),
                         json.dumps({'id': 0,
                                     'table': json.dumps(self.rout_table, cls=JSONRouteTableSerializer),
                                     'X': 0,
                                     'Y': 0,
                                     'chanels': [],
                                     }))

    def test_create_from_json(self):
        obj = Node(0, [], self.rout_table, 0, 0)
        json_obj = json.dumps(obj, cls=JSONNodeSerializer)
        self.assertEqual(obj,
                         JSONNodeSerializer.decode(json_obj))
