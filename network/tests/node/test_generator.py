from network.pkg.node.creator import generate_randomly
from django.test import TestCase


class NetworkGenerateTestCase(TestCase):
    def test_generate_nodes(self):
        nodes, channels = generate_randomly()
        self.assertIsNotNone(nodes)
        self.assertIsNotNone(channels)
