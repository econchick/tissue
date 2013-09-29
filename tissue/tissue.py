import sys

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.python import log
from txsockjs.factory import SockJSFactory

from ports import ports


class PCAPProtocol(Protocol):
    def __init__(self):
        self.listen_ports = ports('LISTEN')
        self.established_ports = ports('ESTABLISHED')


    def connectionMade(self):
        self.transport.write(('listen', self.listen_ports))
        self.transport.write(('est', self.established_ports))


    def dataReceived(self, data):
        pass


log.startLogging(sys.stdout)
reactor.listenTCP(8080, SockJSFactory(Factory.forProtocol(PCAPProtocol)))
reactor.run()