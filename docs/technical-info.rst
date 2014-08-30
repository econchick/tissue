:orphan:

To capture network information, tissue uses the Python package capturing library `scapy <http://www.secdev.org/projects/scapy/>`_. The captured data is aggregated in a Python backend that serves the aggregated information via `Twisted <http://www.twistedmatrix.com/>`_ and web sockets. You can use any browser to connect to the Twisted server and view the information. The server does not have to run on the same network as the client browser.

To learn more about the internals of tissue please see the `Developer Information page <https://github.com/econchick/tissue/wiki/Developer-Information>`_ on the tissue wiki.
