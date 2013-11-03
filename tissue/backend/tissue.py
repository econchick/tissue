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


class PortsPlugin(object):
    def __init__(self):
        self.port_status = PortStatus()

    def receivedData(self):
        scanned_ports = ports("ESTABLISHED")
        new_ports, closed_ports = self.port_status.update(scanned_ports)
        return_values = []
        return_values.append(("ESTABLISHED", new_ports))
        if closed_ports:
            return_values.append(('CLOSED', closed_ports))
        return return_values


class TraceroutePlugin(object):
    def __init__(self):
        self.working = False

    def receivedData(self):
        if self.working:
            return []
        self.working = True
        traceroute, sport = trace_route()
        coordinates = map_ip(traceroute)
        return [('TRACE', sport, coordinates)]
        self.working = False


class SniffProtocol(Protocol):
    def __init__(self):
        self.plugins = [PortsPlugin(), TraceroutePlugin()]

    def connectionMade(self):
        main_loop = LoopingCall(self.updated_data)
        main_loop.start(2, now=False)

    def blockingWrite(self, results):
        for result in results:
            self.transport.write(result)

    def get_data(self, plugin):
        result = plugin.receivedData()
        reactor.callFromThread(self.blockingWrite, result)

    def updated_data(self):
        for plugin in self.plugins:
            print plugin
            reactor.callInThread(self.get_data, plugin)


class SniffFactory(Factory):
    protocol = SniffProtocol

    def __init__(self, plugins):
        self.plugins = plugins


log.startLogging(sys.stdout)

f = SockJSMultiFactory()
f.addFactory(Factory.forProtocol(SniffProtocol), 'sniff')

reactor.listenTCP(8080, f)
reactor.run()
