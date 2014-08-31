import itertools
import operator

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
    def __init__(self):
        self.port_status = PortStatus()

    def update(self):
        scanned_ports = ports("ESTABLISHED")
        new_ports, closed_ports = self.port_status.update(scanned_ports)

        new_ports = sorted(new_ports)
        group_new = itertools.groupby(new_ports, operator.itemgetter(0))
        grouped_new = []
        for k, v in group_new:
            grouped_new.append((k, list(item[1] for item in v)))

        closed_ports = sorted(closed_ports)
        group_closed = itertools.groupby(closed_ports, operator.itemgetter(0))
        grouped_closed = []
        for k, v in group_closed:
            grouped_closed.append((k, list(item[1] for item in v)))

        return_values = []

        return_values.append(("ESTABLISHED", grouped_new))
        if grouped_closed:
            return_values.append(("CLOSED", grouped_closed))
        return return_values

    def getInformation(self, iface):
        with open('plugins/port.js', 'r') as content_file:
            content = content_file.read()
        return {
            'MainClass': 'OpenPortsChart',
            'Name': "Programs with currently opened ports",
            'Code': content,
            'GridWidth': 1,
            'GridHeight': 1
        }


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
                ports.append((key, port))

    return list(set(ports))


def ports(status):
    connections = get_connections()
    return get_ports(connections, status)
