def find_node(id, network):
    for i in network:
        if i.id == id:
            return i
    return None


def find_node_by_address(addr, network, mode=0):
    for i in network:
        if i.address == addr:
            if mode:
                if not i.shutdown:
                    return i
            else:
                return i
    # print('return None on addr')
    # print(addr)
    return None

