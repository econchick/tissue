import datetime
import itertools
import operator

import psutil
from yapsy.IPlugin import IPlugin


class PortStatus(object):
    def __init__(self):
        self.open_ports = set()
        self.connected_processes = {}

    def update(self, ports, processes):
        new_ports = [port for port in ports if port not in self.open_ports]
        closed_ports = [port for port in self.open_ports if port not in ports]
        self.open_ports = ports

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

        connected_processes = {}
        for item in grouped_new:
            if item[0] in processes.keys():
                connected_processes[item[0]] = {}
                connected_processes[item[0]]['info'] = processes[item[0]]
                connected_processes[item[0]]['ports'] = item[1]
        self.connected_processes = processes

        disconnected_processes = {}
        for item in grouped_closed:
            if item[0] in self.connected_processes.keys():
                disconnected_processes[item[0]] = {}
                disconnected_processes[item[0]]['info'] = processes[item[0]]
                disconnected_processes[item[0]]['ports'] = item[1]

        return connected_processes, disconnected_processes


class PortsPlugin(IPlugin):
    def __init__(self):
        self.port_status = PortStatus()

    def update(self):
        processes, scanned_ports = ports("ESTABLISHED")
        new_connections, disconnected_processes = self.port_status.update(scanned_ports, processes)

        return_values = []

        if new_connections:
            return_values.append(("ESTABLISHED", new_connections))
        if disconnected_processes:
            return_values.append(("CLOSED", disconnected_processes))

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
    p = {}
    for process in psutil.process_iter():
        try:
            if process.get_connections() != []:
                connections[process.name] = process.get_connections()
                p[process.name] = {}
                p[process.name]['pid'] = process.pid
                p[process.name]['path'] = process.exe
                p[process.name]['username'] = process.username
                create = datetime.datetime.fromtimestamp(int(process.create_time)).strftime('%Y-%m-%d %H:%M:%S')
                p[process.name]['create_time'] = create
                p[process.name]['threads'] = process.get_num_threads()
                p[process.name]['memory_percent'] = process.get_memory_percent()
                p[process.name]['cpu_percent'] = process.get_cpu_percent()
                p[process.name]['has_children'] = process.get_children != []
        except psutil.AccessDenied:
            continue
        except psutil.NoSuchProcess:
            continue
    return p, connections


def get_processes():
    """Iterates over running processes to grab information"""
    processes = []
    for p in psutil.process_iter():
        try:
            process = {}
            if p.get_connections:
                process[p.name] = p.as_dict()
                processes.append(process)
        except psutil.AccessDenied:
            continue
        except psutil.NoSuchProcess:
            continue
    return processes


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
    processes, connections = get_connections()
    return processes, get_ports(connections, status)
