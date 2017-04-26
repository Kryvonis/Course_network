from network.pkg.channels.models import Channel
from network.pkg.message.serializers import JSONMessageSerializer
import json


class JSONChanelSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            channels = []
            for o in obj:
                channels.append(JSONChanelSerializer.encode(o))
            return channels
        if isinstance(obj, Channel):
            return {
                "id": obj.id,
                "weight": obj.weight,
                "type": obj.type,
                "error_prob": "{0:.3f}".format(obj.error_prob),
                "start_node_id": obj.start_node_id,
                "end_node_id": obj.end_node_id,
                "message_buffer": JSONMessageSerializer.encode(
                    obj.message_buffer),
                "start_node_buffer": JSONMessageSerializer.encode(
                    obj.start_node_buffer),
                "end_node_buffer": JSONMessageSerializer.encode(
                    obj.end_node_buffer),
                "is_busy": obj.is_busy,
                "shutdown": obj.shutdown,
            }

    @classmethod
    def decode(cls, obj):
        if isinstance(obj, list):
            channels = []
            for o in obj:
                channels.append(JSONChanelSerializer.decode(o))
            return channels
        if isinstance(obj, dict):
            return Channel(int(obj['id']),
                           int(obj['start_node_id']),
                           int(obj['end_node_id']),
                           int(obj['weight']),
                           obj['type'],
                           JSONMessageSerializer.decode(
                               obj['start_node_buffer']),
                           JSONMessageSerializer.decode(
                               obj['end_node_buffer']),
                           int(obj['is_busy']),
                           JSONMessageSerializer.decode(obj['message_buffer']),
                           float(obj['error_prob']),
                           int(obj['shutdown']))

