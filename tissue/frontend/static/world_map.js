function WorldMap(svg, width, height) {
    this.svg = svg;

    this.projection = d3.geo.mercator()
        .scale((width + 1) / 2 / Math.PI)
        .translate([width / 2, height / 2])
        .precision(.1);

    var path = d3.geo.path()
        .projection(this.projection);

    var graticule = d3.geo.graticule();

    svg.append("path")
        .datum(graticule)
        .attr("class", "graticule")
        .attr("d", path);

    d3.json('static/world-50m.json', function(error, world) {
      svg.insert("path", ".graticule")
          .datum(topojson.feature(world, world.objects.land))
          .attr("class", "land")
          .attr("d", path);

      svg.insert("path", ".graticule")
          .datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
          .attr("class", "boundary")
          .attr("d", path);
    });

    this.addLine = function(from, to, color) {
        console.log(from);
        console.log(to);
        var scaled_from = this.projection(from);
        var scaled_to = this.projection(to);
        console.log(scaled_from);
        console.log(scaled_to);

        var line = svg.append("line")
            .style("stroke", color)
            .attr("stroke-width",2)
            .attr("x1", scaled_from[0])
            .attr("y1", scaled_from[1])
            .attr("x2", scaled_to[0])
            .attr("y2", scaled_to[1]);

            line
                .attr("opacity", 1)
                .transition().duration(5000)
                .attr("opacity", 0)
                .each("end", function() {
                    line.remove();
                });
    };

}