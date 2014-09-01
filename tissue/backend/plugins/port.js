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
        .port-cell-program { text-align:left;vertical-align:middle } \
        </style> \
        <h4>Currently running programs with open ports</h4> \
          <div class="table-responsive"> \
            <table class="table table-striped ports-table"> \
              <thead> \
                <tr> \
                  <th width="50px" style="text-align:left">Program</th> \
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
        var escaped_program_name = program_name.replace(/\./g, "-").replace(/\ /g, "-");
        cell1.className = "port-cell-program";
        cell1.innerHTML = '<a href="#modal-'+ escaped_program_name +'" data-backdrop="false" data-toggle="modal">' + program_name + '</a>';
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

            var process_information = processes[process].info;
            this._set_modal_html(program, process_information);

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

    this._set_modal_html = function(program_name, program_info) {
        var escaped_program_name = program_name.replace(/\./g, "-").replace(/\ /g, "-");
        var modal_div = $("#tissue-modal");
        modal_div.append('<!-- Modal --> \
            <div id=modal-' + escaped_program_name + ' class="modal fade"> \
              <div class="modal-dialog"> \
                <div class="modal-content"> \
                  <div class="modal-header"> \
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button> \
                    <h4 class="modal-title">Process Information</h4> \
                  </div> \
                  <div class="modal-body"> \
                  <div class="table-responsive"> \
                    <table class="table table-striped"> \
                      <thead> \
                        <tr><td colspan="2">' + program_name + '</td></tr> \
                      </thead> \
                      <tbody> \
                        <tr> \
                          <td>Program Name</td> \
                          <td>' + program_name + '</td> \
                        </tr> \
                        <tr> \
                          <td>Path</td> \
                          <td>' + program_info.path + '</td> \
                        </tr> \
                        <tr> \
                          <td>Username</td> \
                          <td>' + program_info.username + '</td> \
                        </tr> \
                        <tr> \
                          <td>Process ID</td> \
                          <td>' + program_info.pid + '</td> \
                        </tr> \
                        <tr> \
                          <td>Has Children</td> \
                          <td>' + program_info.has_children + '</td> \
                        </tr> \
                        <tr> \
                          <td>Create Time</td> \
                          <td>' + program_info.create_time + '</td> \
                        </tr> \
                        <tr> \
                          <td>Memory %</td> \
                          <td>' + program_info.memory_percent + '</td> \
                        </tr> \
                        <tr> \
                          <td>CPU %</td> \
                          <td>' + program_info.CPU_percent + '</td> \
                        </tr> \
                        <tr> \
                          <td># of Threads</td> \
                          <td>' + program_info.threads + '</td> \
                        </tr> \
                      </tbody> \
                    </table> \
                  </div> \
                  <div class="modal-footer"> \
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> \
                  </div> \
                </div> \
                <!-- /.modal-content --> \
              </div> \
              <!-- /.modal-dialog --> \
            </div> \
            <!-- /.modal -->');
        $("#modal-" + escaped_program_name).draggable({
            handle: ".modal-header"
        });
        return modal_div;
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
