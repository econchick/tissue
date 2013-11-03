function ThroughputChart(svg, width, height) {
    svg.attr("width", width)
        .attr("height", height)
        .attr("class", "bubble");

    var bubbleChart = new BubbleChart(svg, width);

    function isThroughputMessage(e) {
        return e.data != null && e.data.indexOf('THROUGHPUT-DATA') !== -1;
    }

    function isClosedMessage(e) {
        return e.data != null && e.data.indexOf('CLOSED') !== -1;
    }

    var MAX_NODE_SIZE = 5;

    function getBubbleSize(size) {
        if (size <= 100) {
            return 1;
        }
        else if (size <= 1000) {
            return 2;
        }
        else if (size <= 10000) {
            return 3;
        }
        else if (size <= 100000) {
            return 4;
        }
        else {
            return 5;
        }
    }

    function sanitizeIP(ip) {
        return ip.split(".").join("+");
    }

    function updateBubbles(e, bubbleChart) {
        var throughputInfo = extractThroughput(e);
        for (var i in throughputInfo) {
            var throughput = throughputInfo[i];
            var ip = throughput[0];
            var size = throughput[1];
            var bubbleSize = getBubbleSize(size);
            var node = bubbleChart.getNode(ip);
            if (node === null) {
                createNewBubble(ip, sanitizeIP(ip), bubbleSize);
            }
            else {
                bubbleChart.resizeNode(node, bubbleSize);
            }
        }
    }

    function extractThroughput(e) {
        var throughput = [];
        for (var i in e.data[1]) {
            throughput.push(e.data[1][i]);
        }
        return throughput;
    }

    function createNewBubble(title, id, size) {
        bubbleChart.addNode({
            "title": title,
            "name": "throughput-" + id,
            "size": size,
            "id": id
        }, null);
    }

    function removeBubble(e) {
        var throughputInformation = extractThroughput(e)
        for (var i in throughputInformation) {
            var throughput = throughputInformation[i];
            var ip = throughput[0];
            var node = bubbleChart.getNode(ip);
            if (node !== null) {
                bubbleChart.removeNode(node);
            }
        }
    }

    this.receivedData = function(e) {
        if (isThroughputMessage(e)) {
            updateBubbles(e, bubbleChart);
        }
        else if (isClosedMessage(e)) {
            removeBubble(e);
        }
    };
}
