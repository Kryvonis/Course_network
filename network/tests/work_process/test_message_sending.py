from network.pkg.node.creator import generate_randomly
from network.pkg.message.creator import generate_message
from network.pkg.message.sender import add_message_in_connect,add_message_in_datagram, step
from network.pkg.routing.finder import initialize

if __name__ == '__main__':
    network, _ = generate_randomly(2, 1)
    initialize(network)
    message = generate_message('0.1', '1.1', 'connect', 10, 10)
    add_message_in_connect(message, network)
    i = 0
    for j in range(200):
        step(i, network, _)

        i += 1
        if i == len(network):
            i = 0
