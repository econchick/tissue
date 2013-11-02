import sys

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from txsockjs.factory import SockJSMultiFactory

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


class PortProtocol(Protocol):
    def __init__(self):
        self.port_status = PortStatus()

    def connectionMade(self):
        lp = LoopingCall(self.update_ports, status='ESTABLISHED')
        lp.start(1)

    def dataReceived(self, data):
        pass

    def write_to_socket(self, key, data):
        self.transport.write((key, data))

    def update_ports(self, status):
        scanned_ports = ports(status)
        new_ports, closed_ports = self.port_status.update(scanned_ports)
        self.write_to_socket(status, new_ports)
        print new_ports, closed_ports
        if closed_ports:
            self.write_to_socket('CLOSED', closed_ports)


class TracerouteProtocol(Protocol):
    def connectionMade(self):
        gc = LoopingCall(self.get_coordinates)
        gc.start(4, now=False)

    def dataReceived(self, data):
        pass

    def write_coordinates(self, key, port, data):
        self.transport.write((key, port, data))

    def get_coordinates(self):
        traceroute, sport = trace_route()
        coordinates = map_ip(traceroute)
        print "traceroute = ", traceroute
        print "coordinates = ", coordinates
        self.write_coordinates('TRACE', sport, coordinates)


class PortsPlugin(object):
    def __init__(self):
        self.port_status = PortStatus()

    def receivedData(self, socket):
        scanned_ports = ports("ESTABLISHED")
        new_ports, closed_ports = self.port_status.update(scanned_ports)
        print "sending"
        socket.transport.write(("ESTABLISHED", new_ports))
        print "sent"
        print new_ports, closed_ports
        if closed_ports:
            socket.transport.write(('CLOSED', closed_ports))


class TraceroutePlugin(object):
    def __init__(self):
        self.working = False

    def receivedData(self, socket):
        if self.working:
            return
        self.working = True
        traceroute, sport = trace_route()
        coordinates = map_ip(traceroute)
        print "traceroute = ", traceroute
        print "coordinates = ", coordinates
        return ('TRACE', sport, coordinates)
#        socket.transport.write(('TRACE', sport, coordinates))
#        self.working = False


class SniffProtocol(Protocol):
    def __init__(self):
        self.plugins = [PortsPlugin(), TraceroutePlugin()]

    def connectionMade(self):
        print 'blahblah'
        main_loop = LoopingCall(self.updated_data)
        main_loop.start(2, now=False)
        print 'bar'

    def blockingWrite(self, data):
        self.transport.write(data)

    def get_data(self, plugin):
        result = plugin.receivedData(self)
        reactor.callFromThread(self.blockingWrite, result)

    def updated_data(self):
        #streams = get_streams()
        print 'updated data'
        for plugin in self.plugins:
            print plugin
            reactor.callInThread(self.get_data, plugin)

        print 'foooo'


class SniffFactory(Factory):
    protocol = SniffProtocol

    def __init__(self, plugins):
        self.plugins = plugins


log.startLogging(sys.stdout)

f = SockJSMultiFactory()
#f.addFactory(Factory.forProtocol(PortProtocol), "port")
f.addFactory(Factory.forProtocol(SniffProtocol), 'sniff')

reactor.listenTCP(8080, f)
reactor.run()
