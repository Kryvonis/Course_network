from django.test import TestCase
from network.pkg.message.creator import generate_message
from network.pkg.node.creator import generate_randomly
from network.pkg.message.sender import get_next_node_path, add_message_in_datagram, main_loop
from network.pkg.routing.finder import initialize
from network.pkg.node.finder import find_node_by_address


class TestMessageSending(TestCase):
    def test_correct_path(self):
        network, _ = generate_randomly(3, 2)
        initialize(network)

    def test_correct_send_in_datagram(self):
        network, network_channels = generate_randomly(3, 2)
        initialize(network)
        message = generate_message('0.1', '1.2', 'data', 10)
        add_message_in_datagram(message, network)
        main_loop(network, network_channels)


if __name__ == '__main__':
    T = TestMessageSending()
    # T.test_correct_path()
    T.test_correct_send_in_datagram()
