import logging
import sys

from twisted.internet import reactor, threads
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.task import LoopingCall
from twisted.python import log
from txsockjs.factory import SockJSMultiFactory

from yapsy.PluginManager import PluginManager

log.startLogging(sys.stdout)
logging.basicConfig(level=logging.DEBUG)


class SniffProtocol(Protocol):
    DEFAULT_PLUGIN_PATHS = ['plugins']
    PLUGIN_REGISTRATION_MESSAGE = 'REGISTER-PLUGIN'
    REFRESH_PERIOD = 2

    def __init__(self):
        self.manager = PluginManager()
        self.manager.setPluginPlaces(SniffProtocol.DEFAULT_PLUGIN_PATHS)
        self.manager.collectPlugins()

    def _blocking_write(self, results):
        for result in results:
            self.transport.write(result)

    def connectionMade(self):
        for plugin in self.manager.getAllPlugins():
          self._blocking_write(
              [(SniffProtocol.PLUGIN_REGISTRATION_MESSAGE,
               plugin.plugin_object.getInformation())])

        main_loop = LoopingCall(self.updated_data)
        main_loop.start(SniffProtocol.REFRESH_PERIOD, now=False)

    def updated_data(self):
        for plugin in self.manager.getAllPlugins():
            d = threads.deferToThread(plugin.plugin_object.update)
            d.addCallback(self._blocking_write)

f = SockJSMultiFactory()
f.addFactory(Factory.forProtocol(SniffProtocol), 'sniff')

reactor.listenTCP(8801, f)
reactor.run()
