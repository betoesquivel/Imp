
var functions = executable['funcs'];
var instructions = executable['quadruples'];
var constants = executable['constants'];

var startDirs = executable['start_dirs'];
var localDirs = startDirs['local'];
var globalDirs = startDirs['global'];
var tempDirs = startDirs['temp'];
var constantDirs = startDirs['constants'];
var tempGlobalDirs = startDirs['temp_global'];

debug = {
  'functions': document.getElementById('debug-functions'),
  'instructions': document.getElementById('debug-instructions'),
  'constants': document.getElementById('debug-constants'),
  'memory': document.getElementById('debug-memory')
};
output = document.getElementById('output');
input = document.getElementById('input');
vartable = document.getElementById('vartable');

debug['functions'].innerHTML = JSON.stringify(functions);
debug['instructions'].innerHTML = JSON.stringify(instructions);
debug['constants'].innerHTML = JSON.stringify(constants);
debug['memory'].innerHTML = JSON.stringify(startDirs);

var local = [];
var global = [];
var temp = [];
var tempGlobal = [];

vm();

function between(x, lower, upper) {

  return ( x >= lower && x <= upper );

}

function isBoolAddress(dir) {

  switch (dir) {

    case ( between(dir, localDirs[0], localDirs[1]) ):
          return true;
    case ( between(dir, globalDirs[0], globalDirs[1]) ):
          return true;
    case ( between(dir, tempDirs[0], tempDirs[1]) ):
          return true;
    case ( between(dir, tempGlobalDirs[0], tempGlobalDirs[1]) ):
          return true;
    case ( between(dir, constantDirs[0], constantDirs[1]) ):
          return true;
    default:
          return false;

  }

}
function isIntAddress(dir) {

  switch (dir) {

    case ( between(dir, localDirs[1], localDirs[2]) ):
          return true;
    case ( between(dir, globalDirs[1], globalDirs[2]) ):
          return true;
    case ( between(dir, tempDirs[1], tempDirs[2]) ):
          return true;
    case ( between(dir, tempGlobalDirs[1], tempGlobalDirs[2]) ):
          return true;
    case ( between(dir, constantDirs[1], constantDirs[2]) ):
          return true;
    default:
          return false;

  }

}
function isFloatAddress(dir) {

  switch (dir) {

    case ( between(dir, localDirs[2], localDirs[3]) ):
          return true;
    case ( between(dir, globalDirs[2], globalDirs[3]) ):
          return true;
    case ( between(dir, tempDirs[2], tempDirs[3]) ):
          return true;
    case ( between(dir, tempGlobalDirs[2], tempGlobalDirs[3]) ):
          return true;
    case ( between(dir, constantDirs[2], constantDirs[3]) ):
          return true;
    default:
          return false;

  }

}
function isCharAddress(dir) {

  switch (dir) {

    case ( between(dir, localDirs[3], localDirs[4]) ):
          return true;
    case ( between(dir, globalDirs[3], globalDirs[4]) ):
          return true;
    case ( between(dir, tempDirs[3], tempDirs[4]) ):
          return true;
    case ( between(dir, tempGlobalDirs[3], tempGlobalDirs[4]) ):
          return true;
    case ( between(dir, constantDirs[3], constantDirs[4]) ):
          return true;
    default:
          return false;

  }

}
function isStringAddress(dir) {

  switch (dir) {

    case ( between(dir, localDirs[4], localDirs[5]) ):
          return true;
    case ( between(dir, globalDirs[4], globalDirs[5]) ):
          return true;
    case ( between(dir, tempDirs[4], tempDirs[5]) ):
          return true;
    case ( between(dir, tempGlobalDirs[4], tempGlobalDirs[5]) ):
          return true;
    case ( between(dir, constantDirs[4], constantDirs[5]) ):
          return true;
    default:
          return false;

  }

}

function parseValueWithAddress(value, dir) {
  switch (dir) {

    case (isCharAddress(dir)):
      return ( IsNumeric(value) ? value : value.charCodeAt(0) );
    case (isStringAddress(dir)):
      return value;
    default:
      return eval(value);

  }
}

function getValueFromMemory(dir) {

  var value;
  switch (dir) {
    case (dir < localDirs[5]) :
      value = local[dir - localDirs[0]];
      break;
    case (dir < globalDirs[5]) :
      value = global[dir - globalDirs[0]];
      break;
    case (dir < constantDirs[5]) :
      value = constants[dir];
      break;
    case (dir < tempDirs[5]) :
      value = temp[dir - tempDirs[0]];
      break;
    case (dir < tempGlobalDirs[5]) :
      value = tempGlobal[dir - tempGlobalDirs[0]];
      break;
    default:
      console.log("NO ENTRO");
      break;
  }
  return parseValueWithAddress(value, dir);

}

function setValueInMemory(value, dir) {

  var parsedValue = parseValueWithAddress(value, dir);

  switch (dir) {
    case (dir < localDirs[5]) :
      dir -= localDirs[0];
      local[dir] = parsedValue;
    case (dir < globalDirs[5]) :
      dir -= globalDirs[0];
      global[dir] = parsedValue;
    case (dir < tempDirs[5]) :
      dir -= tempDirs[0];
      temp[dir] = parsedValue;
    case (dir < tempGlobalDirs[5]) :
      dir -= tempGlobalDirs[0];
      tempGlobal[dir] = parsedValue;
    default:
      console.log("NO ENTRO");
      break;
  }

}

function vm() {

  for (var i = 0, l = instructions.length; i < l; i ++) {
    var instruction = instructions[i];
    switch( instruction[0] ) {
      case '+':
        console.log(instruction.join());
        var op1 = getValueFromMemory(Number( instruction[1] ));
        var op2 = getValueFromMemory(Number( instruction[2] ));
        setValueInMemory(op1 + op2, Number( instruction[3] ));
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '=':
        console.log(instruction.join());
        var op2 = getValueFromMemory(Number( instruction[1] ));
        var dirOp1 = Number( instruction[3] );
        setValueInMemory(op2, dirOp1);
        console.log(getValueFromMemory(dirOp1));
        break;

      case 'PRINT':
        console.log(instruction.join());
        console.log("PRINT TO CONSOLE:" + getValueFromMemory(Number( instruction[3] )) );
        break;

      default:
        console.log(instruction.join());
    }
  }

}

