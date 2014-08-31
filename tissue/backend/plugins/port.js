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
        cell1.innerHTML = '<a href="#myModal" data-backdrop="false" data-toggle="modal">' + program_name + '</a>';
        row.insertCell();
        return row;
    };

    function _getPortsCell(row) {
        return row.cells[1];
    }

    /**
     * Creates a new HTML row and stores information about it.
     */
    this._createRow = function(program) {
        var table = document.querySelector(".ports-table");
        var row = this._addRow(table, program);

        var portsRow = new PortsRow(d3.select(_getPortsCell(row)));

        this._port_information[program] = portsRow;
    };

    /**
     * Takes received process information and creates new port information
     * and GUI objects to represent the ports.
     */
    this._addPorts = function(processes) {
        for (var process in processes) {
            var program = process;

            // It's a new process we've not seen before. Let's create a new
            // row in the table for it.
            if (program in this._port_information === false) {
                this._createRow(program);
            }

            var portsRow = this._port_information[program];

            if (portsRow === null) {
                // It's possible that the port was closed in the meantime.
                return;
            }

            var established_ports = processes[process].ports;

            for (var j=0; j<established_ports.length; j++) {
                portsRow.addPort(established_ports[j]);
            }
        }
    };

    this.receivedData = function(e) {
            console.log(e);
        if (isEstablishedMessage(e)) {
            this._message_log.log('Message received: New ports established');
            this._addPorts(e.data[1]);
        }
        else if (isClosedMessage(e)) {
            this._message_log.log('Message received: Existing ports closed');
        }
    };
}
