
function createElementWithString(tag, s) {

  var element = '<'+tag+'>';
  element += s;
  element += '</'+tag+'>';

  return element;

}

function createTableFromInstructions() {

  var rows = '';
  for (var r = 0, l = instructions.length; r < l; r ++) {
    var instruction = instructions[r];
    var columns = createElementWithString('td', r);
    for (var c = 0, cl = instructions[r].length; c < cl; c ++) {
      var instructionValue = instructions[r][c];
      columns += createElementWithString('td', instructionValue);
    }
    rows += createElementWithString('tr', columns);
  }
  var table = createElementWithString('table', rows);
  return table;

}
