import psutil

from yapsy.IPlugin import IPlugin



class PortStatus(object):
    def __init__(self):
        self.open_ports = set()

    def update(self, ports):
        new_ports = [port for port in ports if port not in self.open_ports]
        closed_ports = [port for port in self.open_ports if port not in ports]
        self.open_ports = ports

        return new_ports, closed_ports


class PortsPlugin(IPlugin):
    name = "port"

    def __init__(self):
        self.port_status = PortStatus()

    def receivedData(self):
        #self.d = defer.Deferred()
        scanned_ports = ports("ESTABLISHED")
        new_ports, closed_ports = self.port_status.update(scanned_ports)
        return_values = []
        return_values.append(("ESTABLISHED", new_ports))
        if closed_ports:
            return_values.append(('CLOSED', closed_ports))
        print return_values
        return return_values

    def getFrontendCode(self):
        with open('plugins/port.js', 'r') as content_file:
            content = content_file.read()
        return ("OpenPortsChart", content)


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
        except psutil.NoSuchProcess:
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


def ports(status):
    connections = get_connections()
    return get_ports(connections, status)
