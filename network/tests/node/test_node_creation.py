from django.test import TestCase
from network.pkg.node.models import Node
from network.pkg.routing.models import RouteTable
from network.pkg.chanels.models import Channel
from network.pkg.chanels.serializers import JSONChanelSerializer
from network.pkg.node.serializers import JSONNodeSerializer
from network.pkg.routing.serializers import JSONRouteTableSerializer
import json


class NodeTestCase(TestCase):
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
                              'channels': [],
                              })

    def test_correct_json(self):
        obj = Node(0, [], self.rout_table, 0, 0)
        self.assertEqual(JSONNodeSerializer.encode(obj),
                         {'id': 0,
                          'table': JSONRouteTableSerializer.encode(self.rout_table),
                          'X': 0,
                          'Y': 0,
                          'channels': JSONChanelSerializer.encode([]),
                          })

    def test_create_from_json(self):
        obj = Node(0, [], self.rout_table, 0, 0)
        json_obj = JSONNodeSerializer.encode(obj)
        self.assertEqual(obj,
                         JSONNodeSerializer.decode(json_obj))

    def test_network_creation(self):
        rt0 = RouteTable(0, [0, 1], [0, 5], 0)
        rt1 = RouteTable(1, [1, 0], [0, 5], 0)
        chanel1 = Channel(0, 5, 0, 1)

        node0 = Node(0, chanel1, rt0, 0, 0)
        node1 = Node(1, chanel1, rt1, 50, 50)

        network = [node0, node1]
        self.assertIsNotNone(network)
