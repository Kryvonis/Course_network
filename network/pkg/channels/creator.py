from network.pkg.channels.models import Channel
from network.pkg.channels.serializers import JSONChanelSerializer


def generate_channel(id, start_node, end_node):
    return JSONChanelSerializer.encode(Channel(id=id,
                                               type='Duplex',
                                               start_node_id=start_node,
                                               end_node_id=end_node))
