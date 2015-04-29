
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
debug['instructions'].innerHTML = createTableFromInstructions();
debug['constants'].innerHTML = JSON.stringify(constants);
debug['memory'].innerHTML = JSON.stringify(startDirs);


var local = [];
var global = [];
var temp = [];
var tempGlobal = [];


var executionStack = [];
var currentAddress = 0;
var currentFunctionId = 'main';


// crea un diccionario con:
// 1) el arreglo de memoria local (deep copy, tiene que ser nuevo)
// 2) direccion actual en instructions
// luego le hace push al stack de ejecucion
function runtimeSnapshot() {
  var self = this;

  self.memory = jQuery.extend(true, {}, local);
  self.address = -1;
  self.functionId = currentFunctionId;

}

function saveRuntime() {

  executionStack.push(new runtimeSnapshot());

}

function restoreRuntime() {

  if (executionStack.length > 0) {

    local.length = 0;

    var previousStack = executionStack.pop();
    local = previousStack.memory;
    currentAddress = previousStack.address;
    currentFunctionId = previousStack.functionId;

  }

}

function expandActivationRecord(functionId) {

  saveRuntime();
  currentFunctionId = functionId;
  local.length = 0;

}

function goSub(destinationDir) {

  previousStack = executionStack.pop();
  previousStack.address = currentAddress + 1;
  executionStack.push(previousStack);

  currentAddress = destinationDir;

}

function parameterAction(value, parameterIndex) {

    var functionData = functions[currentFunctionId];
    var localParameterAddress = functionData.params[ parameterIndex ].address;
    setValueInMemory(value, localParameterAddress);
    console.log(getValueFromMemory(localParameterAddress));

}

function returnAction(value) {

    var functionData = functions[currentFunctionId];
    var globalFunctionVariableAddress = functionData.address;
    setValueInMemory(value, globalFunctionVariableAddress);
    console.log(getValueFromMemory(globalFunctionVariableAddress));

}

function vm() {

  for (currentAddress = 0, l = instructions.length; currentAddress < l; currentAddress++) {
    var instruction = instructions[currentAddress];
    console.log("\nINSTRUCTION: " + currentAddress);
    console.log(instruction.join());

    switch( instruction[0] ) {
      case '=':
        var op2 = getValueFromMemory(instruction[1]);
        var dirOp1 = instruction[3];
        setValueInMemory(op2, dirOp1);
        console.log(getValueFromMemory(dirOp1));
        break;

      case '+':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 + op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '-':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 - op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '*':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 * op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '/':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 / op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '<':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 < op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '>':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 > op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '<=':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 <= op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '>=':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 >= op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '==':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 === op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case '<>':
        var op1 = getValueFromMemory(instruction[1]);
        var op2 = getValueFromMemory(instruction[2]);
        setValueInMemory(op1 === op2, instruction[3]);
        console.log(getValueFromMemory(instruction[3]));
        break;

      case 'PRINT':
        console.log("PRINT TO CONSOLE:" + getValueFromMemory( instruction[3] ) );
        break;

      case 'GOTO':
        currentAddress = instruction[3];
        console.log(currentAddress);
        currentAddress -= 1; // padding for the  i++ in the for
        break;

      case 'GOTOF':
        var condition = getValueFromMemory(instruction[1]);
        if (!condition) {
          currentAddress = instruction[3];
          console.log('Going to instruction: ' + currentAddress);
          currentAddress -= 1; // padding for the  i++ in the for
        }
        break;

      case 'ERA':
        expandActivationRecord(instruction[3]);
        break;

      case 'PARAMETER':
        var value = getValueFromMemory(instruction[1]);
        parameterAction(value, instruction[3]);
        break;

      case 'GOSUB':
        goSub(instruction[3]);
        currentAddress -= 1; // padding for the i++ in the for
        break;

      case 'ENDPROC':
        restoreRuntime();
        currentAddress -= 1; // padding for the i++ in the for
        break;

      case 'RETURN':
        var value = getValueFromMemory(instruction[3]);
        returnAction(value);
        break;

      default:
        break;
    }
  }

}

vm();
