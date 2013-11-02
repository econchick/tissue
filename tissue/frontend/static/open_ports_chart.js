function OpenPortsChart(svg, diameter, websocket) {

    svg.attr("width", diameter)
        .attr("height", diameter)
        .attr("class", "bubble");

    var bubbleChart = new BubbleChart(svg, diameter);

    function isEstablishedMessage(e) {
        return e.data.indexof('ESTABLISHED') !== -1;
    }

    function isClosedMessage(e) {
        return e.data.indexof('CLOSED') !== -1;
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
        for (var i in e.data[1]) {
            yield e.data[1][i];
        }
    }

    function createNewBubbles(e, bubbleChart) {
        for (var port in extractPorts(e)){
            bubbleChart.addNode({
                "name": "port" + port,
                "size": 1,
                "id": port
            }, null);
        }
    }

    function removeBubble(e) {
        for (var port in extractPorts(e)) {
            var node = bubbleChart.getNode(port);
            bubbleChart.removeNode(node);
        }
    }

    websocket.onmessage = function(e) {
        if (isEstablishedMessage(e)) {
            resizeExistingBubbles(bubbleChart);
            createNewBubbles(e);
        }
        else if (isClosedMessage(e)) {
            removeBubble(e);
        }
    };
}