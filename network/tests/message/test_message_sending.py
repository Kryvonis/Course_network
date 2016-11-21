from django.test import TestCase
from network.pkg.message.creator import generate_message
from network.pkg.node.creator import generate_randomly
from network.pkg.message.sender import get_next_node_path, send_message_in_datagram
from network.pkg.routing.finder import initialize
from network.pkg.node.finder import find_node_by_address


class TestMessageSending(TestCase):
    def test_correct_path(self):
        network, _ = generate_randomly(3, 2)
        initialize(network)
        from_node = find_node_by_address('0.1', network)
        to_node = find_node_by_address('1.2', network)
        current = find_node_by_address('0.1', network)
        while get_next_node_path(from_node, to_node, current) != 0:
            next_addres = get_next_node_path(from_node, to_node, current)
            self.assertIsNotNone(next_addres)
            current = find_node_by_address(next_addres, network)

    def test_correct_send_in_datagram(self):
        network, _ = generate_randomly(3, 2)
        initialize(network)
        message = generate_message('0.1', '1.2', 'data', 10)
        send_message_in_datagram(message, network)


if __name__ == '__main__':
    T = TestMessageSending()
    T.test_correct_path()
    T.test_correct_send_in_datagram()
