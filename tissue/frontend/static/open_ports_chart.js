function OpenPortsChart(svg, diameter) {
    svg.attr("width", diameter)
        .attr("height", diameter)
        .attr("class", "bubble");

    var bubbleChart = new BubbleChart(svg, diameter);

    function isEstablishedMessage(e) {
        return e.data != null && e.data.indexOf('ESTABLISHED') !== -1;
    }

    function isClosedMessage(e) {
        return e.data != null && e.data.indexOf('CLOSED') !== -1;
    }

    var MAX_NODE_SIZE = 5;

    function resizeExistingBubbles(bubbleChart) {
        for (var i in bubbleChart.allbubbles.children){
            var child = bubbleChart.allbubbles.children[i];

            if (child.value < MAX_NODE_SIZE){
                var node = bubbleChart.getNode(child.className);
                bubbleChart.resizeNode(node, child.value + 1);
            }

        }
    }

    function extractPorts(e) {
        var ports = [];
        for (var i in e.data[1]) {
            ports.push(e.data[1][i]);
        }
        return ports;
    }

    function createNewBubbles(e, bubbleChart) {
        var extractedPorts = extractPorts(e);
        for (var port in extractedPorts){
            bubbleChart.addNode({
                "name": "port" + port,
                "size": 1,
                "id": extractedPorts[port]
            }, null);
        }
    }

    function removeBubble(e) {
        var extractedPorts = extractPorts(e)
        for (var port in extractedPorts) {
            var node = bubbleChart.getNode(extractedPorts[port]);
            bubbleChart.removeNode(node);
        }
    }

    this.receivedData = function(e) {
        if (isEstablishedMessage(e)) {
            resizeExistingBubbles(bubbleChart);
            createNewBubbles(e, bubbleChart);
        }
        else if (isClosedMessage(e)) {
            removeBubble(e);
        }
    };
}