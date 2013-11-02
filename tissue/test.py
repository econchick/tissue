from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from txsockjs.factory import SockJSMultiFactory
from txsockjs.utils import broadcast

class EchoProtocol(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class ChatProtocol(Protocol):
    def connectionMade(self):
        if not hasattr(self.factory, "transports"):
            self.factory.transports = set()
        self.factory.transports.add(self.transport)

    def dataReceived(self, data):
        broadcast(data, self.factory.transports)

    def connectionLost(self, reason):
        self.factory.transports.remove(self.transport)

f = SockJSMultiFactory()
f.addFactory(Factory.forProtocol(EchoProtocol), "echo")
f.addFactory(Factory.forProtocol(ChatProtocol), "chat")

reactor.listenTCP(8080, f)
reactor.run()