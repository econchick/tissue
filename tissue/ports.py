import psutil


def get_connections():
    """
    Iterates over running processes and return any that have connections.
    """
    connections = {}
    for process in psutil.process_iter():
        try:
            if process.get_connections() != []:
                connections[process.name] = process.get_connections()
        except psutil.AccessDenied:
            continue
    return connections

def get_ports(connections, status):
    """
    Iterates over connections and returns unique ports for a given
    connection status.
    arg: connections - dictionary of open local connections
    arg: status - string, e.g. 'LISTEN', 'ESTABLISHED'
    ret: ports - list of ports
    """
    ports = []
    for key, value in connections.iteritems():
        for connection in connections[key]:
            if connection.status == status:
                _, port = connection.laddr
                ports.append(port)

    return list(set(ports))

def ports(status, previous_ports):
    connections = get_connections()
    scanned_ports = get_ports(connections, status)
    if previous_ports:
        print 'hello'
        print 'scanned', scanned_ports
        print 'previous', previous_ports
        if previous_ports == scanned_ports:
            return None
        else:
            return scanned_ports

    return scanned_ports


