from network.pkg.message.models import Message


class JSONMessageSerializer:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, list):
            messages = []
            for o in obj:
                messages.append({'id': o.id,
                                 'time': o.time,
                                 'from_node': o.from_node,
                                 'to_node': o.to_node,
                                 'type_message': o.type_message,
                                 'info_size': o.info_size,
                                 'service_size': o.service_size,
                                 }
                                )
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
                message = Message(o['time'],
                                  o['from_node'],
                                  o['to_node'],
                                  o['type_message'],
                                  o['info_size'],
                                  o['service_size'],
                                  )
                message.set_id(o['id'])
                messages.append(message)
            return messages
        if isinstance(obj, dict):
            message = Message(obj['time'],
                              obj['from_node'],
                              obj['to_node'],
                              obj['type_message'],
                              obj['info_size'],
                              obj['service_size'],
                              )
            message.set_id(obj['id'])
            return message
