import sys

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from txsockjs.factory import SockJSFactory

from ports import ports


class PCAPProtocol(Protocol):
    def __init__(self):
        self.listen_ports = ports('LISTEN', None)
        self.established_ports = ports('ESTABLISHED', None)
        ep = LoopingCall(self.update_ports, status=('ESTABLISHED',self.established_ports))
        ep.start(5)
        lp = LoopingCall(self.update_ports, status=('LISTEN', self.listen_ports))
        lp.start(5)

    def connectionMade(self):
        self.write_ports('LISTEN', self.listen_ports)
        self.write_ports('ESTABLISHED', self.established_ports)

    def dataReceived(self, data):
        pass

    def write_ports(self, status, ports):
        self.transport.write((status, ports))

    def update_ports(self, status):
        new_ports = ports(status[0], status[1])
        if not new_ports:
            print 'no new ports'
            return
        else:
            print 'new ports!'
            self.write_ports(status[0], new_ports)
            return


log.startLogging(sys.stdout)
reactor.listenTCP(8080, SockJSFactory(Factory.forProtocol(PCAPProtocol)))
reactor.run()