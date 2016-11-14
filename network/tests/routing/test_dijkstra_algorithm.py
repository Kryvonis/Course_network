from django.test import TestCase
from network.pkg.routing.finder import initialize
from network.pkg.node.creator import generate_randomly


class Dijkstra(TestCase):
    def setUp(self):
        self.nosed = generate_randomly(7, 2)

    def test_create_routtables(self):
        self.assertEqual(True, True)
