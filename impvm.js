
functions = executable['funcs'];
instructions = executable['quadruples'];
constants = executable['constants'];

debug = {
  'functions': document.getElementById('debug-functions'),
  'instructions': document.getElementById('debug-instructions'),
  'constants': document.getElementById('debug-constants')
};
output = document.getElementById('output');
vartable = document.getElementById('vartable');

debug['functions'].innerHTML = JSON.stringify(functions);
debug['instructions'].innerHTML = JSON.stringify(instructions);
debug['constants'].innerHTML = JSON.stringify(constants);

vm();

function vm() {


}

