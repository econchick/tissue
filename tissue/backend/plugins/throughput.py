from collections import defaultdict

from yapsy.IPlugin import IPlugin

from sniff import get_streams


class ThroughputPlugin(IPlugin):
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

    def getInformation(self):
        with open('plugins/throughput.js', 'r') as content_file:
            content = content_file.read()
        return {
            'MainClass': 'ThroughputChart',
            'Code': content,
            'GridWidth': 1,
            'GridHeight': 1
        }
