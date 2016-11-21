from network.pkg.channels.models import Channel
import json


class JSONChanelSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            channels = []
            for o in obj:
                channels.append(JSONChanelSerializer.encode(o))
                # channels.append(o.__dict__)
            return channels
        if isinstance(obj, Channel):
            return {
                'id': obj.id,
                'weight': obj.weight,
                'type': obj.type,
                'error_prob': obj.error_prob,
                'start_node_id': obj.start_node_id,
                'end_node_id': obj.end_node_id,
                'message_buffer': obj.message_buffer,
                'start_node_buffer': obj.start_node_buffer,
                'end_node_buffer': obj.end_node_buffer,
                'buisy': str(obj.is_buisy),
            }

    @classmethod
    def decode(cls, ojb):
        if isinstance(ojb, list):
            channels = []
            for o in ojb:
                channels.append(Channel(**o))
            return channels
        if isinstance(ojb, dict):
            return Channel(**ojb)
