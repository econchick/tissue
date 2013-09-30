import select as s
import socket as sock

from scapy.all import *
import pygeoip


def parse_stream(stream):
    ether_layer = stream.getlayer(Ether)
    IP_layer = stream.getlayer(IP)
    proto_layer = stream.getlayer(TCP)
    return ether_layer, IP_layer, proto_layer

def get_local_ip():
    return sock.gethostbyname(socket.gethostname())

def trace_route():
    # filter should be local IP addr
    streams = sniff(iface="en1", filter='tcp and src %s' % get_local_ip(), count=10)
    for stream in streams:
        ether_layer, IP_layer, proto_layer = parse_stream(stream)
        destination = IP_layer.dst
        src = IP_layer.src
        dport = proto_layer.dport
        sport = proto_layer.sport

        while True:
            try:
                res, unans = traceroute(target=destination, dport=dport, sport=sport, maxttl=20)
                traces = res.res
                hops = [src]
                for trace in traces:
                    hops.append(trace[1].src)

                return hops, sport
            except s.error:
                continue


def map_ip(hops):
    gip = pygeoip.GeoIP('/Users/lynnroot/Dev/tissue/GeoLiteCity.dat')
    coordinates = []
    for hop in hops:
        geo_data = gip.record_by_addr(hop)
        if geo_data:
            lat = geo_data['latitude']
            lon = geo_data['longitude']
            coordinates.append((lon, lat))

    return coordinates
