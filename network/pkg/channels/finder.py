
def find_channel(channels, start_node, end_node):
    for i in channels:
        if (i.start_node_id == start_node and i.end_node_id == end_node) or \
                (i.start_node_id == end_node and i.end_node_id == start_node):
            return i
    return False


def channel_exist(channels, start_node, end_node):
    for i in channels:
        if (i.start_node_id == start_node and i.end_node_id == end_node) or \
                (i.start_node_id == end_node and i.end_node_id == start_node) or \
                (start_node == end_node):
            return True
    return False