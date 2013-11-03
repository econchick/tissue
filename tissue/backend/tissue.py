from collections import defaultdict
import sys

from twisted.internet import reactor, threads
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from txsockjs.factory import SockJSMultiFactory

from ports import ports
from sniff import trace_route, map_ip, get_streams


class PortStatus(object):
    def __init__(self):
        self.open_ports = set()

    def update(self, ports):
        new_ports = [port for port in ports if port not in self.open_ports]
        closed_ports = [port for port in self.open_ports if port not in ports]
        self.open_ports = ports

        return new_ports, closed_ports


class ThroughputPlugin(object):
    def __init__(self):
        self.stats = defaultdict(int)

    def receivedData(self):
        packets = get_streams()
        throughput_data = defaultdict(int)
        for packet in packets:
            IP_layer = packet.getlayer('IP')
            throughput_data[IP_layer.dst] += IP_layer.len

        results = [('THROUGHPUT-DATA', throughput_data.items())]
        print results
        return results


class PortsPlugin(object):
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


class TraceroutePlugin(object):
    def __init__(self):
        self.working = False

    def receivedData(self):
        if self.working:
            return []
        self.working = True
        traceroute, sport = trace_route()
        coordinates = map_ip(traceroute)
        self.working = False
        print [('TRACE', sport, coordinates)]
        return [('TRACE', sport, coordinates)]


class SniffProtocol(Protocol):
    def __init__(self):
        #self.plugins = [PortsPlugin(), TraceroutePlugin(), ThroughputPlugin()]
        #self.plugins = [PortsPlugin(), TraceroutePlugin()]
        self.plugins = [PortsPlugin(), ThroughputPlugin(), TraceroutePlugin()]

    def connectionMade(self):
        main_loop = LoopingCall(self.updated_data)
        main_loop.start(2, now=False)

    def blockingWrite(self, results):
        for result in results:
            self.transport.write(result)

    def get_data(self, plugin):
        return plugin.receivedData()
        #reactor.callFromThread(self.blockingWrite, result)

    def updated_data(self):
        for plugin in self.plugins:
            d = threads.deferToThread(self.get_data, plugin)
            d.addCallback(self.blockingWrite)


class SniffFactory(Factory):
    protocol = SniffProtocol

    def __init__(self, plugins):
        self.plugins = plugins


log.startLogging(sys.stdout)

f = SockJSMultiFactory()
f.addFactory(Factory.forProtocol(SniffProtocol), 'sniff')

reactor.listenTCP(8081, f)
reactor.run()
