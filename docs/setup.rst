.. _setup:

Setup
=====

.. _step-1-binaries:

Step 1: Binaries
----------------

* install `libpcap <http://www.tcpdump.org/>`_
    * For Linux: `sudo apt-get install libpcap0.8-dev`
    * For Mac OSX: Should already have tcpdump (that includes libpcap)
* download/install `libdnet <http://libdnet.sourceforge.net/>`_:


Libdnet + python wrapper:

::

    $ wget http://libdnet.googlecode.com/files/libdnet-1.12.tgz
    $ tar xfz libdnet-1.12.tgz
    $ ./configure
    $ make
    $ sudo make install
    $ cd python
    $ python2.5 setup.py install

Step 2: Python packages
-----------------------

``pip install -r requirements.txt``


Error Messages
--------------

Got error messages when installing?

1. Install libpcap-dev (from :ref:`step-1-binaries`) if you see this message:

::

    pcapdumper.cc:12:18: fatal error: pcap.h: No such file or directory

    #include <pcap.h>


