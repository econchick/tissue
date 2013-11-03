import logging
import sys

from twisted.internet import reactor, threads
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from txsockjs.factory import SockJSMultiFactory

from yapsy.PluginManager import PluginManager


class SniffProtocol(Protocol):
    def __init__(self):
        #self.plugins = [PortsPlugin(), TraceroutePlugin(), ThroughputPlugin()]
        #self.plugins = [PortsPlugin(), TraceroutePlugin()]
        #self.plugins = manager = PluginManager()
        logging.basicConfig(level=logging.DEBUG)
        self.manager = PluginManager()
        self.manager.setPluginPlaces(["plugins"])
        self.manager.collectPlugins()

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
        for plugin in self.manager.getAllPlugins():
            d = threads.deferToThread(self.get_data, plugin.plugin_object)
            d.addCallback(self.blockingWrite)

log.startLogging(sys.stdout)

f = SockJSMultiFactory()
f.addFactory(Factory.forProtocol(SniffProtocol), 'sniff')

reactor.listenTCP(8800, f)
reactor.run()
