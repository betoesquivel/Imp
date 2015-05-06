
function TrackedItem(id, address) {
  var self = this;

  self.name = id;
  self.address = address;

}

function ImpViewModel() {
  var self = this;

  self.trackedVars = ko.observableArray([]);

  self.trackedAddresses = ko.computed( function() {
    var addresses = ko.utils.arrayMap(self.trackedVars(), function(trackedVar) {
      return trackedVar.address;
    });
    return addresses;
  }, self);

  self.trackedNames = ko.computed( function() {
    var names = ko.utils.arrayMap(self.trackedVars(), function(trackedVar) {
      return trackedVar.name;
    });
    return names;
  }, self);

  self.trackedValues = ko.computed( function() {
    var values = [];
    ko.utils.arrayForEach( self.trackedVars(), function(trackedVar) {
      var val = getValueFromMemory(trackedVar.address);
    });
  }, self);

}
