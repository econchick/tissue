import sys

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from txsockjs.factory import SockJSFactory

from ports import ports
from sniff import trace_route, map_ip


class PortStatus(object):
    def __init__(self):
        self.open_ports = set()

    def update(self, ports):
        new_ports = [port for port in ports if port not in self.open_ports]
        closed_ports = [port for port in self.open_ports if port not in ports]
        self.open_ports = ports

        return new_ports, closed_ports


class PCAPProtocol(Protocol):
    def __init__(self):
        self.port_status = PortStatus()

    def connectionMade(self):
        lp = LoopingCall(self.update_ports, status='ESTABLISHED')
        gc = LoopingCall(self.get_coordinates)
        lp.start(1)
        gc.start(25)

    def dataReceived(self, data):
        pass

    def write_to_socket(self, key, data):
        self.transport.write((key, data))

    def update_ports(self, status):
        scanned_ports = ports(status)
        new_ports, closed_ports = self.port_status.update(scanned_ports)
        self.write_to_socket(status, new_ports)
        if closed_ports:
            self.write_to_socket('CLOSED', closed_ports)

    def write_coordinates(self, key, port, data):
        self.transport.write((key, port, data))

    def get_coordinates(self):
        traceroute, sport = trace_route()
        coordinates = map_ip(traceroute)
        print "traceroute = ", traceroute
        print "coordinates = ", coordinates
        self.write_coordinates('TRACE', sport, coordinates)



log.startLogging(sys.stdout)
reactor.listenTCP(8080, SockJSFactory(Factory.forProtocol(PCAPProtocol)))
reactor.run()
