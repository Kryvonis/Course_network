from network.pkg.channels.models import Channel
from network.pkg.channels.serializers import JSONChanelSerializer
import random

weights = (1, 2, 3, 4, 5, 7, 11, 12, 15, 17, 19, 24, 27, 28)
channels_types = ('duplex', 'halfduplex')


def generate_channel(id, start_node, end_node, channel_type=0, weight=0):
    id = id
    start_node_buffer = []
    end_node_buffer = []
    is_busy = 0
    message_buffer = {}
    if not weight:
        weight = random.choice(weights)
    if not channel_type:
        channel_type = random.choice(channels_types)

    error_prob = random.random() * 0.01
    # error_prob = random.random()
    return Channel(id=id,
                   start_node_id=start_node,
                   end_node_id=end_node,
                   error_prob=error_prob,
                   weight=weight,
                   type=channel_type,
                   message_buffer=message_buffer,
                   is_busy=is_busy,
                   end_node_buffer=end_node_buffer,
                   start_node_buffer=start_node_buffer,
                   )
