function getVariableData(address) {
  var variableData = null;
  if (address in functions[currentFunctionId]['id_addresses']){
    variableData = functions[currentFunctionId]['id_addresses'][address];
  }else{
    variableData = globals[address];
  }
  return variableData;
}

function Row(values) {
  var self = this;

  self.values = values;

}
function TableElement(columns, row) {
  var self = this;

  self.columnNames = columns;
  self.rows = ko.observableArray();
  self.rows.push(row);

  self.addRow = function(values) {
    self.rows.push(values);
  };

}

function TrackedItem(id, address) {
  var self = this;

  self.name = id;
  self.address = address;
  //self.value = ko.observable(getValueFromMemory(address));
  self.lastModLine = -1;
  /*
    self.valueChanged = ko.computed(function() {
    var val = self.value();
    return true;
  }, self);
  */

}

function ImpViewModel() {
  var self = this;

  self.codeLines = ko.observableArray([]);

  self.trackedVars = ko.observableArray([]);

  self.valuesChanged = ko.observable(true);

  self.trackedAddresses = ko.computed( function() {
    var addresses = ko.utils.arrayMap(self.trackedVars(), function(trackedVar) {
      return trackedVar.address;
    });
    return addresses;
  }, self);

  self.trackedGlobal = ko.computed ( function() {
    var global = ko.utils.arrayFilter( self.trackedVars(), function (trackedVar) {
        return isGlobalAddress(trackedVar.address);
    });
    return global;
  }, self);

  self.trackedLocal = ko.computed ( function() {
    var local = ko.utils.arrayFilter( self.trackedVars(), function (trackedVar) {
        return isLocalAddress(trackedVar.address);
    });
    return local;
  }, self);

  self.globalNames = ko.computed ( function() {

    var names = ko.utils.arrayMap(self.trackedGlobal(), function(trackedVar) {
      return 'G:'+trackedVar.name;
    });
    return names;

  }, self);

  self.localNames = ko.computed ( function() {

    var names = ko.utils.arrayMap(self.trackedLocal(), function(trackedVar) {
      return 'L:'+trackedVar.name;
    });
    return names;

  }, self);

  self.trackedNames = ko.computed( function() {
    return self.globalNames().concat( self.localNames() );
  }, self);


  self.trackedValues = function() {
    var values = [];

    ko.utils.arrayForEach( self.trackedGlobal(), function(trackedVar) {
      var variableData = getVariableData(trackedVar.address);
      var val = [];
      for (var i = 0, l = variableData.size; i < l; i ++) {
        var v = getValueFromMemory(trackedVar.address + i);
        val[val.length] = v;
      }

      if (val.length == 1){
        val = val[0];
      }

      var next = values.length;
      if (val) {
        values[next] = {};
        values[next].value = val;
        values[next].line = trackedVar.lastModLine;
      }else{
        console.log(trackedVar.name + ' has no value.' );
      }
    });
    ko.utils.arrayForEach( self.trackedLocal(), function(trackedVar) {
      var variableData = getVariableData(trackedVar.address);
      var val = [];
      for (var i = 0, l = variableData.size; i < l; i ++) {
        var v = getValueFromMemory(trackedVar.address + i);
        val[val.length] = v;
      }

      if (val.length == 1){
        val = val[0];
      }

      var next = values.length;
      if (val) {
        values[next] = {};
        values[next].value = val;
        values[next].line = trackedVar.lastModLine;
      }else{
        console.log(trackedVar.name + ' has no value.' );
      }
    });

    var row = new Row(values);
    return row;
  };

  self.tables = ko.observableArray([]);

  self.trackNewVar = function(id, address) {

    self.trackedVars.push( new TrackedItem(id, address) );

  }

  self.addNewTableFromTracked = function () {

    var newTable = new TableElement(self.trackedNames(), self.trackedValues());
    self.tables.push(newTable);

  };

  self.displayMessage = function ( data ) {

    var msg = data.message;
    var line = data.line;
    var newMessage = new TableElement(['Message at line: ' + line], new Row( [msg] ));
    self.tables.push(newMessage);
    self.addNewTableFromTracked();

  };

  self.displayDecision = function ( data ) {

    var decisionTaken = data.decision;
    var line = data.line;
    var decisionType = data.type;
    var newDecision = new TableElement(['Decision of type ' + decisionType + ' taken at line: ' + line], new Row( [{ 'value': decisionTaken, 'line':line }] ));
    self.tables.push(newDecision);
    self.addNewTableFromTracked();

  };

  self.displayStackPosition = function ( data ) {

    var stackPosition = data.stackPosition;
    var line = data.line;
    var newStackPositionMessage = new TableElement(['Change of context at line: ' + line], new Row( [{ 'value': stackPosition, 'line':false }] ));
    self.tables.push(newStackPositionMessage);
    self.addNewTableFromTracked();

  };

  self.displayReturn = function ( data ) {

    var returnValue = data.returnValue;
    var line = data.line;
    var newReturnMessage = new TableElement(['Returning at line: ' + line], new Row( [{ 'value': returnValue, 'line':false }] ));
    self.tables.push(newReturnMessage);

  };

  self.displayToConsole = function ( data ) {

    var message = data.message;
    var line = data.line;
    var newConsoleOutput = new TableElement(['Printing to console at line: ' + line], new Row( [{ 'value': message, 'line':false }] ));
    self.tables.push(newConsoleOutput);
    self.addNewTableFromTracked();

  };

  self.varChanged = function (address, line) {

    var lastTable = self.tables()[ self.tables().length - 1 ];
    var changed = ko.utils.arrayFirst( self.trackedVars(), function(trackedVar) {
      return trackedVar.address == address;
    });
    changed.lastModLine = line;
    lastTable.addRow( self.trackedValues() );

  };

  self.clearLocalVariables = function () {
    self.trackedVars.remove( function(trackedVar) {
      return isLocalAddress(trackedVar.address);
    });
  };

  self.batchLoadLocalVariables = function (localVariables) {

    var newTracked = self.trackedGlobal();
    var newTracked = newTracked.concat( localVariables );
    self.trackedVars( newTracked );

  };

}

var viewModel = new ImpViewModel();
ko.applyBindings (viewModel);

viewModel.trackedVars.subscribe(function(changed) {

  viewModel.addNewTableFromTracked();

});
