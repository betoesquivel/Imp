
function between(x, lower, upper) {

  return ( x >= lower && x <= upper );

}

function isBoolAddress(dir) {

  switch (true) {

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

  switch (true) {

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

  switch (true) {

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

  switch (true) {

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

  switch (true) {

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
  switch (true) {

    case (isCharAddress(dir)):
      return ( isNaN(value) ? value.charCodeAt(0) : value );
    case (isStringAddress(dir)):
      return value;
    default:
      return eval(value);

  }
}

function getValueFromMemory(dir) {

  var value;
  switch (true) {
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

  switch (true) {
    case (dir < localDirs[5]) :
      dir -= localDirs[0];
      local[dir] = parsedValue;
      break;
    case (dir < globalDirs[5]) :
      dir -= globalDirs[0];
      global[dir] = parsedValue;
      break;
    case (dir < tempDirs[5]) :
      dir -= tempDirs[0];
      temp[dir] = parsedValue;
      break;
    case (dir < tempGlobalDirs[5]) :
      dir -= tempGlobalDirs[0];
      tempGlobal[dir] = parsedValue;
      break;
    default:
      console.log("NO ENTRO");
      break;
  }

}
