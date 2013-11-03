# tissue

tissue visualizes activity on networks in real-time on a high level of abstraction. Unlike tools like [Wireshark](http://www.wireshark.org/) or [tcpdump](http://www.tcpdump.org/) that show information about individual packets going over the network, tissue aggregates network data and presents higher level information about what's happening on a network.

To learn more about tissue please visit [our project wiki](https://github.com/econchick/tissue/wiki).

### Setup

TBD
* pip install -r requirements.txt
* scapy is found here: pip install hg+http://hg.secdev.org/scapy
* pcapy: pip install "http://corelabs.coresecurity.com/index.php?module=Wiki&action=attachment&type=tool&page=Pcapy&file=pcapy-0.10.8.tar.gz"
* pylibpcap: pip install http://sourceforge.net/projects/pylibpcap/files/pylibpcap/0.6.4/pylibpcap-0.6.4.tar.gz/download
* dnet: pip install http://prdownloads.sourceforge.net/libdnet/libdnet-1.11.tar.gz?download

### Use

TBD

### Technical information

To capture network information, tissue uses the Python package capturing library [scapy](http://www.secdev.org/projects/scapy/). The captured data is aggregated in a Python backend that serves the aggregated information via [Twisted](http://www.twistedmatrix.com/) and web sockets. You can use any browser to connect to the Twisted server and view the information. The server does not have to run on the same network as the client browser.

To learn more about the internals of tissue please see the [Developer Information page](https://github.com/econchick/tissue/wiki/Developer-Information) on the tissue wiki.

### Bugs and feature requests

If you want to file a bug against or request a feature for tissue, please
use our [project bug tracker](https://github.com/econchick/tissue/issues). We
will then triage your ticket and let you know about the next steps we are
planning to take.

### Contributions

If you want to contribute to tissue, please follow the following steps:

* File a ticket against the tissue project describing the contribution you want to make
* Wait for us to give feedback. Maybe we are already working on what you asked for or maybe we do not want the feature you planned to contribute in tissue. Don't waste your time doing unnecessary work!
* If we greenlight your request, please fork tissue, work on your code and send us a pull request through GitHub when you're done. If you are planning to make big changes, please send us multiple pull requests that are useful independently.
* If we block your request, please fork tissue and start working on your fork. We still appreciate pull requests from your fork down the line.
* Please make sure that you are familiar with the information posted on the [Developer Information page](https://github.com/econchick/tissue/wiki/Developer-Information) on the tissue wiki.

#### Code style guide

As with any project, please try to emulate the existing code style. If you feel that we're doing it wrong, please file a ticket in our issue tracker. For tissue, the indentation question has been solved. We use four spaces for indentation regardless of the language the code is written in.

### Contributors

* Lynn Root ([lynn@tissue.sh](lynn@tissue.sh) / [@roguelynn] (https://twitter.com/roguelynn))
* Sebastian Porst ([sp@porst.tv](sp@porst.tv) / [Google+](https://plus.google.com/+SebastianPorst/))