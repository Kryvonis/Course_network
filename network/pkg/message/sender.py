from network.pkg.message.creator import generate_response_to_connect, split_messages_to_datagrams, \
    generate_request_to_connect, generate_same_message
from network.pkg.node.finder import find_node_by_address
from network.pkg.channels.finder import find_channel
import datetime

statistic_table = {'0': 0}
establish_connections = []


def set_statistic_table(stat_tbl):
    statistic_table['0'] = stat_tbl


def step(i, network, network_channels):
    current_node = network[i]

    for channel in current_node.channels:
        buffer = channel.get_node_buffer(current_node.id)
        if buffer:
            if buffer[0].type_message == 'datagram':
                datagram_logic(buffer, current_node, channel, network)
                continue
            if buffer[0].type_message == 'connect':
                connect_logic(buffer, current_node, channel, network)
                continue
            if 'data' in buffer[0].type_message:
                data_logic(buffer, current_node, channel, network)
                continue
            if buffer[0].type_message == 'response_rel+':
                release_logic(buffer, current_node, channel, network)
                continue
            if buffer[0].type_message == 'request':
                request_logic(buffer, current_node, channel, network)
                continue
            if buffer[0].type_message == 'response+':
                response_plus_logic(buffer, current_node, channel, network)
                continue
            if buffer[0].type_message == 'response-':
                response_minus_logic(buffer, current_node, channel, network)
                continue

    for channel in network_channels:
        channel.send_from_channel_to_buffer()


def datagram_logic(buffer, current_node, channel, network):
    if buffer[0].to_node == current_node.address:
        # try:
        #     # buffer[0].time = (datetime.datetime.now() - buffer[0].time).microseconds
        # except:
        #     print('ERROR')
        #     print(buffer[0])
        #     print(buffer[0].time)
        #     print(current_node)
        #     print(channel)
        message_delivered(channel, buffer[0], current_node)
        # return
    else:
        send_message(buffer, current_node, channel, network)


def connect_logic(buffer, current_node, channel, network):
    """
    generate request for connection and make chanel busy because we cant take some messages
    :param buffer:
    :param current_node:
    :param channel:
    :param network:
    :return:
    """
    if not channel.is_busy:
        # create request and wait for response
        request = generate_request_to_connect(buffer[0])
        request.type_message = 'connect'
        statistic_table['0'].message_delivered(request)

        request = generate_request_to_connect(buffer[0])
        statistic_table['0'].message_add(request)
        buffer.insert(0, request)
        # buffer.remove(buffer[1])
        send_message(buffer, current_node, channel, network)

    channel.is_busy = 1


def request_logic(buffer, current_node, channel, network):
    """
    if request for this node need to generate response
    else need to send request to next node
    :param buffer:
    :param current_node:
    :param channel:
    :param network:
    :return:
    """
    check_establish = {
        'to_node': buffer[0].from_node,
        'from_node': buffer[0].to_node,
    }

    if buffer[0].to_node == current_node.address:
        statistic_table['0'].message_delivered(buffer[0])
        # generate response check some situation when channel can`t be
        response = generate_response_to_connect(buffer[0], '+')
        channel.is_busy = 1

        channel.remove_from_buffer(current_node.id, buffer[0])
        buffer.insert(0, response)
        statistic_table['0'].message_add(buffer[0])
        send_message(buffer, current_node, channel, network)
    # elif buffer[0].from_node == current_node.address:
    #     if not channel.is_busy:
    #         send_message(buffer, current_node, channel, network)
    #     channel.is_busy = 1
    else:
        node_sender = find_node_by_address(buffer[0].from_node, network)
        node_getter = find_node_by_address(buffer[0].to_node, network)
        next_node = find_node_by_address(get_next_node_path(node_sender, node_getter, current_node),
                                         network)
        # next_step_node = find_node_by_address(get_next_node_path(node_sender, node_getter, next_node),
        #                                       network)
        # if next_step_node and next_step_node != next_node:
        next_step_channel = find_channel(next_node.channels, current_node.id,
                                         next_node.id)
        if next_step_channel and next_step_channel.is_busy:
            # buffer[0].time = (datetime.datetime.now() - buffer[0].time).microseconds

            response = generate_response_to_connect(buffer[0], '-')
            # statistic_table['0'].message_delivered(buffer[0])
            # channel.remove_from_buffer(current_node.id, buffer[0])
            # buffer.insert(0, response)
            # channel.is_busy = 0
            statistic_table['0'].message_add(response)
            # send_message(buffer, current_node, channel, network)
        else:
            send_message(buffer, current_node, channel, network)
            channel.is_busy = 1
            # else:
            #     channel.is_busy = 0
            #     send_message(buffer, current_node, channel, network)
            #     channel.is_busy = 1


def response_plus_logic(buffer, current_node, channel, network):
    """
    if we get response+ for our message need to send our message
    :param buffer:
    :param current_node:
    :param channel:
    :param network:
    :return:
    """
    if buffer[0].to_node == current_node.address:
        statistic_table['0'].message_delivered(buffer[0])
        establish_connections.append(
            {
                'to_node': buffer[0].from_node,
                'from_node': buffer[0].to_node,
            }
        )
        buffer.remove(buffer[0])  # remove from buffer "response+"
        # channel.is_busy = 1
        # packets = split_messages_to_datagrams(buffer[0], 'data')
        # packets[0].type_message = 'data_last'
        # buffer.remove(buffer[0])  # remove from buffer "connect"
        # for i in packets:
        #     channel.add_to_buffer(current_node.id, i)
        #     ##
        #     # Comment about TIME, need to count or save previously
        #     ##
        #     statistic_table['0'].add_row('create new connect pocket message with data size {}'.format(i.info_size),
        #                                  i.from_node,
        #                                  i.to_node,
        #                                  datetime.datetime.now().microsecond
        #                                  )
        #     statistic_table['0'].message_add(i)
        # # buffer[0].type_message = 'data'
        # # statistic_table['0'].message_add(buffer[0])
        #
        # send_message(buffer, current_node, channel, network)
        # channel.is_busy = 1
    else:
        send_message(buffer, current_node, channel, network)


def data_logic(buffer, current_node, channel, network):
    """
    if we get data message need to generate response for releasing channel
    :param buffer:
    :param current_node:
    :param channel:
    :param network:
    :return:
    """
    if buffer[0].to_node == current_node.address:
        # check is this data message is the last


        # statistic_table['0'].message_delivered(buffer[0])

        if buffer[0].type_message == 'data_last':
            response = generate_response_to_connect(buffer[0], '_rel+')
            message_delivered(channel, buffer[0], current_node)
            # check_establish = {
            #     'to_node': buffer[0].from_node,
            #     'from_node': buffer[0].to_node,
            # }
            # establish_connections.pop(establish_connections.index(check_establish))
            channel.is_busy = 0
            buffer.insert(0, response)
            statistic_table['0'].message_add(response)
            send_message(buffer, current_node, channel, network)
        else:
            message_delivered(channel, buffer[0], current_node)
    else:
        check_establish = {
            'to_node': buffer[0].to_node,
            'from_node': buffer[0].from_node,
        }
        if check_establish in establish_connections:
            channel.is_busy = 0
            send_message(buffer, current_node, channel, network)
            channel.is_busy = 1


def release_logic(buffer, current_node, channel, network):
    """
    if we get response_rel+ message need to release channel
    :param buffer:
    :param current_node:
    :param channel:
    :param network:
    :return:
    """
    if buffer[0].to_node == current_node.address:
        channel.is_busy = 0
        check_establish = {
            'to_node': buffer[0].from_node,
            'from_node': buffer[0].to_node,
        }
        establish_connections.pop(establish_connections.index(check_establish))
        statistic_table['0'].message_delivered(buffer[0])
        buffer.remove(buffer[0])
    else:
        send_message(buffer, current_node, channel, network)
        channel.is_busy = 0


def send_message(buffer, current_node, channel, network):
    node_sender = find_node_by_address(buffer[0].from_node, network)
    node_getter = find_node_by_address(buffer[0].to_node, network)
    next_node = find_node_by_address(get_next_node_path(node_sender, node_getter, current_node),
                                     network)
    channel_sender = find_channel(current_node.channels, current_node.id,
                                  next_node.id)
    msg_type = generate_same_message(buffer[0])
    msg_type.id = buffer[0].id
    flag = False
    if channel_sender != channel:
        # get from one buffer and sent to another buffer on node
        statistic_table['0'].add_row('from one buffer to another. Message {}'.format(msg_type),
                                     current_node.address,
                                     next_node.address,
                                     datetime.datetime.now().microsecond
                                     )
        try:
            channel_sender.add_to_buffer(current_node.id, buffer[0])
        except:
            print(next_node)
            print(current_node)
            print(node_sender)
            print(node_getter)
        flag = channel_sender.try_send_from_node_buffer_to_channel(current_node.id, buffer[0])
        if flag:
            statistic_table['0'].add_row(
                'send message using channel between. Message {}'.format(msg_type),
                current_node.address,
                next_node.address,
                datetime.datetime.now().microsecond
            )
        channel.remove_from_buffer(current_node.id, buffer[0])
    else:
        if channel.try_send_from_node_buffer_to_channel(current_node.id, buffer[0]):
            statistic_table['0'].add_row(
                'send message using channel between. Message {}'.format(msg_type),
                current_node.address,
                next_node.address,
                datetime.datetime.now().microsecond
            )
    return flag


def response_minus_logic(buffer, current_node, channel, network):
    """
    if something wrong and we get response- need to send
    :param buffer:
    :param current_node:
    :param channel:
    :param network:
    :return:
    """
    if buffer[0].to_node == current_node.address:
        channel.is_busy = 0
        statistic_table['0'].message_delivered(buffer[0])
        buffer.remove(buffer[0])
    else:
        send_message(buffer, current_node, channel, network)
        channel.is_busy = 0


def get_next_node_path(from_node, to_node, current_node):
    """
    get addres of next node,
    :param from_node: Node model
    :param to_node: Node model
    :param current_node: Node model
    :return: str addresss next node
    """
    if to_node == current_node:
        return current_node.address
    if current_node.address.split('.')[0] != to_node.address.split('.')[0]:

        # check if node sender is main node. If not - need to send to main node and after that send to getter
        if current_node.address.split('.')[1] == '0':

            next_node = current_node.table.path[
                str(to_node.address.split('.')[0] + '.0')
            ].split(',')[1]
        else:
            next_node = current_node.table.path[
                from_node.address.split('.')[0] + '.0'].split(',')[1]
    else:
        next_node = current_node.table.path[to_node.address].split(',')[1]
    return next_node


def add_message_in_datagram(message, network):
    """
    need to send message and return all path of sending
    :param message: what message
    :param network: what network
    :return: path
    """
    node_sender = find_node_by_address(message.from_node, network)
    node_getter = find_node_by_address(message.to_node, network)
    # Node getter from other region
    next_node = get_next_node_path(node_sender, node_getter, node_sender)
    channes_sender = find_channel(node_sender.channels, node_sender.id,
                                  find_node_by_address(next_node, network).id)

    message.time = datetime.datetime.now()

    datagrams = split_messages_to_datagrams(message, 'datagram')
    for i in datagrams:
        channes_sender.add_to_buffer(node_sender.id, i)
        statistic_table['0'].add_row('create new datagram message with data size {}'.format(i.info_size),
                                     i.from_node,
                                     i.to_node,
                                     datetime.datetime.now().microsecond
                                     )
        statistic_table['0'].message_add(i)


def add_message_in_connect(message, network):
    """
    need to send message and return all path of sending
    :param message: what message
    :param network: what network
    :return: path
    """
    node_sender = find_node_by_address(message.from_node, network)
    node_getter = find_node_by_address(message.to_node, network)
    # Node getter from other region
    next_node = get_next_node_path(node_sender, node_getter, node_sender)
    channes_sender = find_channel(node_sender.channels, node_sender.id,
                                  find_node_by_address(next_node, network).id)

    message.time = datetime.datetime.now()

    packets = split_messages_to_datagrams(message, 'data')
    packets[-1].type_message = 'data_last'
    request = generate_request_to_connect(message)
    statistic_table['0'].message_add(request)
    channes_sender.add_to_buffer(node_sender.id, request)
    for i in packets:
        channes_sender.add_to_buffer(node_sender.id, i)
        ##
        # Comment about TIME, need to count or save previously
        ##
        statistic_table['0'].add_row('create new connect pocket message with data size {}'.format(i.info_size),
                                     i.from_node,
                                     i.to_node,
                                     datetime.datetime.now().microsecond
                                     )
        statistic_table['0'].message_add(i)


def message_delivered(channel, message, current_node):
    statistic_table['0'].add_row(
        'read message [type:{};size:{};service size{};delivered time:{};]'.
            format(message.type_message, message.info_size,
                   message.service_size, message.time),
        message.from_node,
        message.to_node,
        datetime.datetime.now().microsecond
    )
    statistic_table['0'].message_delivered(message)
    channel.remove_from_buffer(current_node.id, message)
