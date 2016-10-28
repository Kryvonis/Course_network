from django.test import TestCase
from network.pkg.routing.models import RouteTable
from network.pkg.routing.serializers import JSONRouteTableSerializer
import json


class ChanelTestCase(TestCase):
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
        self.assertEqual(json.loads(json.dumps(obj, cls=JSONRouteTableSerializer)),
                         json.loads(json.dumps({'node_id': 0,
                                                'addresses': [],
                                                'metric': [],
                                                'path': [],
                                                }))
                         )

    def test_create_from_json(self):
        obj = RouteTable(0, [], [], [])
        json_obj = json.dumps(obj, cls=JSONRouteTableSerializer)
        self.assertEqual(obj,
                         JSONRouteTableSerializer.decode(json_obj))