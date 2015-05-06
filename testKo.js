function ViewModel() {
  var self = this;

  self.array = ko.observableArray([]);
  self.counter = ko.observable(0);

}
vm = new ViewModel();

ko.applyBindings(vm);

vm.array.subscribe(function(change){

  vm.counter( vm.counter() + 1 );

});
