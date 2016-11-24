from network.pkg.message.models import Message


class JSONMessageSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            messages = []
            for o in obj:
                messages.append(JSONMessageSerializer.encode(o))
            return messages
        if isinstance(obj, Message):
            return {'id': obj.id,
                    'time': obj.time,
                    'from_node': obj.from_node,
                    'to_node': obj.to_node,
                    'type_message': obj.type_message,
                    'info_size': obj.info_size,
                    'service_size': obj.service_size,
                    }

    @classmethod
    def decode(cls, obj):
        if isinstance(obj, list):
            messages = []
            for o in obj:
                messages.append(JSONMessageSerializer.decode(o))
            return messages
        if isinstance(obj, dict):
            message = Message(obj['time'],
                              obj['from_node'],
                              obj['to_node'],
                              obj['type_message'],
                              obj['info_size'],
                              obj['service_size'],
                              obj['delay'],
                              )
            message.set_id(obj['id'])
            return message
