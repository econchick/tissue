import sys

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from txsockjs.factory import SockJSFactory

from ports import ports


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
        lp.start(1)

    def dataReceived(self, data):
        pass

    def write_ports(self, status, ports):
        self.transport.write((status, ports))

    def update_ports(self, status):
        scanned_ports = ports(status)
        new_ports, closed_ports = self.port_status.update(scanned_ports)
        if not new_ports and not closed_ports:
            return
        if new_ports:
            self.write_ports(status, new_ports)
        if closed_ports:
            self.write_ports('CLOSED', closed_ports)


log.startLogging(sys.stdout)
reactor.listenTCP(8080, SockJSFactory(Factory.forProtocol(PCAPProtocol)))
reactor.run()
