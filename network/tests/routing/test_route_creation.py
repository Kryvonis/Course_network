from django.test import TestCase
from network.pkg.routing.models import RouteTable
from network.pkg.routing.serializers import JSONRouteTableSerializer
import json


class RouteTestCase(TestCase):
    def setUp(self):
        self.rout_table = RouteTable(0, [], [], [])

    def test_creation(self):
        obj = RouteTable(0, [], [], [])
        self.assertIsNotNone(obj)

    def test_correct_parameters(self):
        obj = RouteTable(0, [], [], [])
        self.assertDictEqual(obj.__dict__,
                             {'node_id': 0,
                              'addresses': [],
                              'metric': [],
                              'path': [],
                              })

    def test_correct_json(self):
        obj = RouteTable(0, [], [], [])
        self.assertEqual(JSONRouteTableSerializer.encode(obj),
                         {'node_id': 0,
                          'addresses': [],
                          'metric': [],
                          'path': [],})

    def test_create_from_json(self):
        obj = RouteTable(0, [], [], [])
        json_obj = JSONRouteTableSerializer.encode(obj)
        self.assertEqual(obj,
                         JSONRouteTableSerializer.decode(json_obj))
