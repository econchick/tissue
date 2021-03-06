import select as s
import socket as sock

from scapy.all import *
import pygeoip

from yapsy.IPlugin import IPlugin


class TraceroutePlugin():
    def __init__(self):
        self.working = False

    def update(self):
        if self.working:
            return []
        self.working = True
        traceroute, sport, errors = trace_route(self.iface)
        coordinates = map_ip(traceroute)
        self.working = False
        result = [('TRACE', sport, coordinates)]
        if errors:
            result.append(('ERROR', errors))
        return result

    def getInformation(self, iface):
        self.iface = iface

        with open('plugins/traceroute.js', 'r') as content_file:
            content = content_file.read()
        return {
            'MainClass': 'TracerouteChart',
            'Code': content,
            'GridWidth': 2,
            'GridHeight': 1
        }

def parse_stream(stream):
    ether_layer = stream.getlayer(Ether)
    IP_layer = stream.getlayer(IP)
    proto_layer = stream.getlayer(TCP)
    return ether_layer, IP_layer, proto_layer


def get_local_ip():
    return sock.gethostbyname(socket.gethostname())


def get_streams(iface):
    return sniff(
        iface='eth0', filter='tcp and src %s' % get_local_ip(), count=10)


def trace_route(iface):
    for stream in get_streams(iface):
        ether_layer, IP_layer, proto_layer = parse_stream(stream)
        destination = IP_layer.dst
        src = IP_layer.src
        dport = proto_layer.dport
        sport = proto_layer.sport

        errors = []

        try:
            res, unans = traceroute(target=destination, dport=dport, sport=sport, maxttl=20)
            traces = res.res
            hops = [src]
            for trace in traces:
                hops.append(trace[1].src)

            return hops, sport, errors
        except s.error, e:
            errors.append('Traceroute Error: Coult not traceroute IP %s (%s)' % (destination, str(e)))
            return [], 0, errors


def map_ip(hops):
    gip = pygeoip.GeoIP('../data/GeoLiteCity.dat')
    coordinates = []
    for hop in hops:
        geo_data = gip.record_by_addr(hop)
        if geo_data:
            lat = geo_data['latitude']
            lon = geo_data['longitude']
            coordinates.append((lon, lat))

    return coordinates
