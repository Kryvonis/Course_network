def find_node(id, network):
    for i in network:
        if i.id == id:
            return i
    return None


def find_node_by_address(addr, network):
    for i in network:
        if i.address == addr:
            return i
    return None
