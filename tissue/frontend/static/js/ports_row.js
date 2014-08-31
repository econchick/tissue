function PortsRow(parent) {
    this.CIRCLE_RADIUS = 30;
    this.CIRCLE_DIAMETER = 2 * this.CIRCLE_RADIUS;
    this.CIRCLE_SPACING = this.CIRCLE_DIAMETER + 0;

    this.COLOR_NEW_PORT = "green";
    this.COLOR_CLOSED_PORT = "red";

    this._svg = parent.append("svg")
        .attr('height', this.CIRCLE_DIAMETER + 'px')
        .attr('width', '100%');

    this._ports = [];

    this._arrangePorts = function() {
        for (var i = 0; i<this._ports.length;i++) {
            var port_information = this._ports[i];

            var new_x = (i + 1) * this.CIRCLE_SPACING;
            var new_y = this.CIRCLE_RADIUS;

            port_information.g
              .transition()
              .duration(1000)
              .attr("transform", "translate(" + new_x + ", " + new_y + ")");
        }
    };

    this._createVisualGroup = function(port) {
        var new_x = (this._ports.length + 1) * this.CIRCLE_SPACING;
        var new_y = this.CIRCLE_RADIUS;

        var g = this._svg.append("g")
            .attr("transform", "translate(" + new_x + ", " + new_y + ")");
    
        g.append("circle")
          .attr("r", this.CIRCLE_RADIUS)
          .style("fill", this.COLOR_NEW_PORT);
    
        g.append("text")
            .attr('y', 5)
            .attr('fill', 'white')
            .style('font-size', '15px')
            .style('font-weight', 'bold')
            .attr("text-anchor", "middle")
            .text(port);

        return g;
    };

    this._portSorter = function(lhs, rhs) {
        return lhs.port - rhs.port;
    };

    this.addPort = function(port) {
        var port_information = {
            'port': port,
            'g': this._createVisualGroup(port)
        };

        this._ports.push(port_information);
        this._ports.sort(this._portSorter);

        this._arrangePorts();
    };

    this._findPort = function(port) {
        for (var i=0; i<this._ports.length; i++) {
            var port_information = this._ports[i];
            if (port_information.port == port) {
                return port_information;
            }
        }

        return null;
    };

    this._changeColor = function(g) {
        g.select('circle')
            .transition(1000)
            .style("fill", "red");
    };

    this.removePort = function(port) {
        var port_information = this._findPort(port);

        if (port_information !== null) {
            var index = this._ports.indexOf(port_information);
            if (index > -1) {
                this._ports.splice(index, 1);
            }

            var self = this;

            port_information.g.select('circle')
                .transition().duration(1000)
                .style("fill", this.COLOR_CLOSED_PORT)
                .each("end", function() {
                    port_information.g.select("text").remove();
                })
                .transition().duration(1000)
                .attr("r", function(d) { return 0; })
                .each("end", function() {
                    port_information.g.remove();
                    self._arrangePorts();
                });
        }
    };
}
