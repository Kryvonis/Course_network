from network.pkg.node.creator import generate_randomly
from django.test import TestCase


class NetworkGenerateTestCase(TestCase):
    def test_generate_nodes(self):
        network, nodes, channels = generate_randomly(5)
        self.assertIsNotNone(network)
        self.assertIsNotNone(nodes)
        self.assertIsNotNone(channels)
        print(network)
        print()
        print(nodes)
        print()
        print(channels)
