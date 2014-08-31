function OpenPortsChart(svg, width, height) {

    /** Determines whether a given message signals new established ports. */
    function isEstablishedMessage(e) {
        return e.data !== null && e.data.indexOf('ESTABLISHED') !== -1;
    }

    /** Determines whether a given message signals new closed ports. */
    function isClosedMessage(e) {
        return e.data !== null && e.data.indexOf('CLOSED') !== -1;
    }

    /** Given a row, returns the cell that contains the ports information. */
    function _getPortsCell(row) {
        return row.cells[1];
    }

    /** Maps from program names to PortsRow port information objects. */
    this._port_information = {};

    /** Maps from program names to table rows. */
    this._port_rows = {};

    /** Called when the plugin is first initialized. **/
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

    /** Inserts a row at the end of a given table. */
    this._addRow  = function(table, program_name) {
        var row = table.insertRow();
        var cell1 = row.insertCell();
        cell1.className = "port-cell-program";
        cell1.innerHTML = '<a href="#myModal" data-backdrop="false" data-toggle="modal">' + program_name + '</a>';
        row.insertCell();
        return row;
    };

    /** Creates a new HTML row and stores information about it. */
    this._createRow = function(program) {
        var table = document.querySelector(".ports-table");
        var row = this._addRow(table, program);

        var portsRow = new PortsRow(d3.select(_getPortsCell(row)));

        this._port_information[program] = portsRow;
        this._port_rows[program] = table.rows.length - 1;
    };

    /** Removes the row of the given program from the UI. */
    this._removeRow = function(program) {
        var table = document.querySelector(".ports-table");
        var index = this._port_rows[program];

        // Decrement the indices of all rows after the deleted row.
        for (var p in this._port_rows) {
            if (this._port_rows[p] > index) {
                this._port_rows[p] = this._port_rows[p] - 1;
            }
        }

        table.deleteRow(index);

        delete this._port_information[program];
        delete this._port_rows[program];
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

    /** Removes the given ports from the UI. */
    this._removePorts = function(processes) {
        for (var process in processes) {
            var program = process;

            if (program in this._port_information === false) {
                // It's possible that the program was closed in the meantime.
                return;
            }

            var portsRow = this._port_information[program];

            if (portsRow === null) {
                // It's possible that the port was closed in the meantime.
                return;
            }

            var removed_ports = processes[process].ports;

            for (var j=0; j<removed_ports.length; j++) {
                portsRow.removePort(removed_ports[j]);
            }

            if (!portsRow.hasPorts()) {
                this._removeRow(program);
            }
        }
    };

    /** Invoked by the plugin handler when a new message arrives. */
    this.receivedData = function(e) {
        if (isEstablishedMessage(e)) {
            this._message_log.log('Message received: New ports established');
            this._addPorts(e.data[1]);
        }
        else if (isClosedMessage(e)) {
            this._message_log.log('Message received: Existing ports closed');
            this._removePorts(e.data[1]);
        }
    };
}
