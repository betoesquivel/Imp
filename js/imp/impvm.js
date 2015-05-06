var functions = executable['funcs'];
var instructions = executable['quadruples'];
var constants = executable['constants'];
var globals = executable['globals'];
var decisions = executable['decisions'];
var codeLines = executable['code'];

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

debug['functions'].innerHTML = JSON.stringify(functions);
debug['instructions'].innerHTML = createTableFromInstructions();
debug['constants'].innerHTML = JSON.stringify(constants);
debug['memory'].innerHTML = JSON.stringify(startDirs);

viewModel.codeLines(codeLines);

var local = [];
var global = [];
var temp = [];
var tempGlobal = [];


var executionStack = [];
var parametersStack = []; // for nested function calls
var parameters = []; // for function calls
var currentAddress = 0;
var currentFunctionId = 'main';
var stackPosition = 'main'; // holds the name of the current stack position


// crea un diccionario con:
// 1) el arreglo de memoria local (deep copy, tiene que ser nuevo)
// 2) direccion actual en instructions
// luego le hace push al stack de ejecucion
function runtimeSnapshot() {
  var self = this;

  self.memory = jQuery.extend(true, [], local);
  self.tempMemory = jQuery.extend(true, [], temp);
  self.address = -1;
  self.functionId = currentFunctionId;
  self.parametersStack = jQuery.extend(true, [], parametersStack);
  self.parameters = jQuery.extend(true, [], parameters);
  self.stackPosition = stackPosition;
  self.trackedLocal = viewModel.trackedLocal();

}

function saveRuntime() {

  executionStack.push(new runtimeSnapshot());

}

function restoreRuntime(line) {

  if (executionStack.length > 0) {

    var previousStack = executionStack.pop();
    local = previousStack.memory;
    temp = previousStack.tempMemory;
    currentAddress = previousStack.address;
    currentFunctionId = previousStack.functionId;
    parametersStack = previousStack.parametersStack;
    parameters = previousStack.parameters;

    viewModel.clearLocalVariables();

    stackPosition = previousStack.stackPosition;
    data = {};
    data.stackPosition = stackPosition;
    data.line = line;
    viewModel.displayStackPosition( data );

    var trackedLocal = previousStack.trackedLocal;
    viewModel.batchLoadLocalVariables(trackedLocal);

  }

}

function expandActivationRecord(functionId) {

  saveRuntime();
  currentFunctionId = functionId;
  parameters.length = 0;

}

function loadParametersToLocalMemory() {

    var functionData = functions[currentFunctionId];
    for (var i = 0, l = parameters.length; i < l; i ++) {

      var value = parameters[i];
      var localParameterAddress = functionData.params[i].address;
      setValueInMemory(value, localParameterAddress);

    }

}

function goSub(destinationDir, line) {

  previousStack = executionStack.pop();
  previousStack.address = currentAddress + 1;
  executionStack.push(previousStack);

  currentAddress = destinationDir;
  local.length = 0;
  viewModel.clearLocalVariables();
  temp.length = 0;

  stackPosition += '/' + currentFunctionId + '(' + parameters.join(',') + ')';
  data = {};
  data.stackPosition = stackPosition;
  data.line = line;
  viewModel.displayStackPosition( data );

  loadParametersToLocalMemory();

}

function parameterAction(value, parameterIndex) {

    parameters[parameterIndex] = value;
    console.log("Added parameter " + value + " to the parameters array for " + currentFunctionId);

}

function returnAction(value, line) {

    var functionData = functions[currentFunctionId];
    var globalFunctionVariableAddress = functionData.address;
    setValueInMemory(value, globalFunctionVariableAddress);
    console.log(getValueFromMemory(globalFunctionVariableAddress));

    data = {};
    data.returnValue = value;
    data.line = line;
    viewModel.displayReturn( data );

}

function endProcAction(line) {

  parametersStack.length = 0;
  parameters.length = 0;
  local.length = 0;
  temp.length = 0;
  restoreRuntime(line);

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
        var modIndex = instruction[2];
        if ( isLocalAddress(dirOp1) ){
          var variable_object = functions[currentFunctionId].id_addresses[dirOp1];
          var mod_line = variable_object.mods[modIndex];
          console.log("MODIFIED LOCAL VARIABLE AT LINE: " + mod_line);
          console.log(functions[currentFunctionId].id_addresses[dirOp1]);

          viewModel.varChanged(dirOp1, mod_line);
        }else if ( isGlobalAddress(dirOp1) ){
          var variable_object = globals[dirOp1];
          var mod_line = variable_object.mods[modIndex];
          console.log("MODIFIED GLOBAL VARIABLE AT LINE: " + mod_line);
          console.log(globals[dirOp1]);

          viewModel.varChanged(dirOp1, mod_line);
        }
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
        data = {};
        data.line = instruction[1];
        data.message = getValueFromMemory(instruction[3]);
        viewModel.displayToConsole( data );
        break;

      case 'GOTO':
        currentAddress = instruction[3];
        console.log(currentAddress);
        currentAddress -= 1; // padding for the  i++ in the for
        break;

      case 'GOTOF':
        var condition = getValueFromMemory(instruction[1]);
        var decisionIndex = instruction[2];
        var decisionType = decisions[decisionIndex].type;
        var decisionLine = decisions[decisionIndex].line;
        if (!condition) {
          currentAddress = instruction[3];
          console.log('Going to instruction: ' + currentAddress);
          currentAddress -= 1; // padding for the  i++ in the for
        }
        console.log('DECISION TAKEN');
        console.log('Decision type: ' + decisionType);
        console.log('Decision line: ' + decisionLine);
        var data = {};
        data.decision = Boolean( condition );
        data.line = decisionLine;
        data.type = decisionType;
        viewModel.displayDecision(data);
        break;

      case 'ERA':
        expandActivationRecord(instruction[3], instruction[2]);
        break;

      case 'PARAMETER':
        var value = getValueFromMemory(instruction[1]);
        parameterAction(value, instruction[3]);
        break;

      case 'GOSUB':
        var line = instruction[1];
        goSub(instruction[3], line);
        currentAddress -= 1; // padding for the i++ in the for
        break;

      case 'ENDPROC':
        endProcAction(instruction[3]);
        currentAddress -= 1; // padding for the i++ in the for
        break;

      case 'RETURN':
        var value = getValueFromMemory(instruction[3]);
        var line = instruction[1];
        returnAction(value, line);
        break;

      case 'DECLARE':
        var id = instruction[1];
        var address = instruction[3];
        viewModel.trackNewVar(id, address);

      default:
        break;
    }
  }

}

vm();
