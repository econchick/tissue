function OpenPortsChart(svg, width, height) {
    svg.attr("width", width)
        .attr("height", height)
        .attr("class", "bubble");

    var bubbleChart = new BubbleChart(svg, width);

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
        var connections = e.data[1];
        var ports = [];
        for (var i in connections) {
            ports.push(connections[i]);
        }
        return ports;
    }

    function extractGroups(e) {
        var connections = e.data[1];
        var groups = [];
        for (var i in connections) {
            groups.push(connections[i])
        }
        return groups
    }

    function addPorts(e) {
        for (var i in e){
            bubbleChart.addNode({
                "title": e[i],
                "name": "port" + e[i],
                "size": 1,
                "id": e[i]
            }, null);
        }
    }

    function createNewBubbles(e, bubbleChart) {
        var extractedGroups = extractGroups(e);
        for (var connection in extractedGroups){
            bubbleChart.addNode({
                "title": extractedGroups[connection][0],
                "name": "port" + connection,
                "size": 1,
                "id": extractedGroups[connection][0],
                "ports": addPorts(extractedGroups[connection][1])
            }, null);
        }
    }

    // function createNewBubbles(e, bubbleChart) {
    //     var extractedPorts = extractPorts(e);
    //     for (var connection in extractedPorts){
    //         bubbleChart.addNode({
    //             "title": extractedPorts[connection[0]][0],
    //             "name": "port" + connection[1],
    //             "size": 1,
    //             "id": extractedPorts[connection][1]
    //         }, null);
    //     }
    // }

    function removeBubble(e) {
        var extractedPorts = extractPorts(e)
        for (var i in extractedPorts) {
            var node = bubbleChart.getNode(extractedPorts[i][1]);
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
