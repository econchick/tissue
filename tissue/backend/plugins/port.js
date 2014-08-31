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

    this.initialize = function(message_log) {
        this._message_log = message_log;
        var main_div = document.querySelector(".tissue-main");
        main_div.innerHTML = '<style type = "text/css" scoped> \
        .port-cell-program { text-align:right;vertical-align:middle } \
        </style> \
        <h2>Currently running programs with open ports</h2> \
          <div class="table-responsive"> \
            <table class="table table-striped ports-table"> \
              <thead> \
                <tr> \
                  <th width="150px" style="text-align:right">Program</th> \
                  <th>Open ports</th> \
                </tr> \
              </thead> \
              <tbody> \
              </tbody> \
            </table> \
          </div>';
    };

    this._port_information = {};

    this._addRow  = function(table, program_name) {
        var row = table.insertRow();
        var cell1 = row.insertCell();
        cell1.className = "port-cell-program";
        cell1.innerHTML = program_name;
        row.insertCell();
        return row;
    };

    this._updatePorts = function(processes) {
        for (var process in processes) {
            var program = process;
            var established_ports = processes[process].ports;
            if (program in this._port_information) {
            } else {
                var table = document.querySelector(".ports-table");
                var row = this._addRow(table, program);
                var portsRow = new PortsRow(d3.select(row.cells[1]));
                for (var j=0; j<established_ports.length; j++) {
                    portsRow.addPort(established_ports[j]);
                }
            }
        }
    }

    this.receivedData = function(e) {
        if (isEstablishedMessage(e)) {
            this._updatePorts(e.data[1]);
            this._message_log.log('fpp');
            this._message_log.log(e.data[1][0]);
//        console.log(d3.select("#ports-dropbox"));
//        console.log(portsRow);
//portsRow.addPort(65535);
//setTimeout(function() {portsRow.addPort(30)}, 2000);
//setTimeout(function() {portsRow.addPort(5)}, 4000);
//setTimeout(function() {portsRow.removePort(5)}, 6000);
        }
        else if (isClosedMessage(e)) {
        }
    };
}
