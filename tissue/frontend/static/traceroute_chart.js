function TracerouteChart(svg, width, height) {
    svg.attr("width", width)
        .attr("height", height);

    var worldMap = new WorldMap(svg, width, height);

    function isTraceMessage(e) {
        return e.data.indexOf('TRACE') !== -1;
    }

    this.receivedData = function(e) {
        if (isTraceMessage(e) ){
            for (var i = 0; i < e.data[2].length - 1; i++) {
                var from = e.data[2][i];
                var to = e.data[2][i + 1];
                worldMap.addLine(from, to, "green");
            }
        }
    };
}