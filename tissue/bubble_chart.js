function BubbleChart(svg, diameter) {
   // Add object properties like this
   this.svg = svg;
   this.allbubbles = {children: []};

    this.diameter = diameter,
    this.format = d3.format(",d"),
    this.color = d3.scale.category20c();

    this.bubble = d3.layout.pack()
        .sort(null)
        .size([this.diameter, this.diameter])
        .padding(1.5);

    this.updateNodes = function() {
        svg.selectAll(".node")
            .data(this.bubble.nodes(this.allbubbles)
            .filter(function(d) { return !d.children; }))
        .select("g circle")
            .attr("r", function(d) { return d.r; });

        svg.selectAll(".node").transition()
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    };

    this.resizeNode = function(nnode, size) {
        var index = this.allbubbles.children.indexOf(nnode);
        this.allbubbles.children[index].value = size;

        var node = svg.selectAll("#node-" + nnode.className);
        var circle = node.select("circle");
        var self = this;

        circle
            .transition().duration(1000)
            .style("fill", "orange")
            .each("end", function() {
                self.updateNodes();
                circle.transition().duration(1000)
                    .style("fill", "#3182bd")
            })
    };

    this.getNode = function(name) {
        for (var n in this.allbubbles.children) {
            if (this.allbubbles.children[n].className == name) {
                return this.allbubbles.children[n];
            }
        }
        return null;
    }

    this.removeNode = function(oldnode) {
        var index = this.allbubbles.children.indexOf(oldnode);
        var node = svg.selectAll("#node-" + oldnode.className);
        var circle = node.select("circle");
        var self = this;

        circle
            .transition().duration(1000)
            .style("fill", "red")
            .each("end", function() {
                node.select("text").remove();
            })
            .transition().duration(1000)
            .attr("r", function(d) { return 0; })
            .each("end", function() {
                node.remove();
                self.allbubbles.children.splice(index, 1);
                self.updateNodes();
            });
    };

    this.addNode = function(newnode, onclick) {
        this.allbubbles.children.push({packageName: null, className: "" + newnode.id, value: newnode.size});

        var node = svg.selectAll(".node")
            .data(this.bubble.nodes(this.allbubbles)
            .filter(function(d) { return !d.children; }))
        .enter().append("g")
            .attr("class", "node")
            .attr("id", "node-" + newnode.id)
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
            .on("click", onclick);

        var self = this;

        node.append("title")
          .text(function(d) { return d.className + ": " + self.format(d.value); });

        node.append("circle")
            .style("fill", "green")
            .transition().duration(1000)
            .style("fill", function(d) { return self.color(d.packageName); });

        node.append("text")
            .attr("dy", ".3em")
            .style("text-anchor", "middle")
            .style("fill", "#272727")
            .text(function(d) { return d.className.substring(0, d.r / 3); });

        this.updateNodes();

        return node;
    };
}