import logging
import os
import sys

import click

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
               plugin.plugin_object.getInformation(SniffProtocol._iface))])

        main_loop = LoopingCall(self.updated_data)
        main_loop.start(SniffProtocol.REFRESH_PERIOD, now=False)

    def updated_data(self):
        for plugin in self.manager.getAllPlugins():
            d = threads.deferToThread(plugin.plugin_object.update)
            d.addCallback(self._blocking_write)


@click.command()
@click.option(
    '--port', '-p', default=8080, type=click.IntRange(0, 65535),
    help='tissue server port')
@click.option(
    '--iface', default=None, help='Network interface to listen on')
def start_server(port, iface):
    euid = os.geteuid()
    if euid != 0:
        print "Error: tissue server must be run as root"
        sys.exit(1)

    SniffProtocol._iface = iface

    f = SockJSMultiFactory()
    f.addFactory(Factory.forProtocol(SniffProtocol), 'sniff')

    try:
        reactor.listenTCP(port, f)
        reactor.run()
    except OverflowError:
        print "Error: Port must be in range 0-65535"

if __name__ == '__main__':
    start_server()