#!env/bin/python
import pprint

pp = pprint.PrettyPrinter()

errors = {
        'PARAMETER_LENGTH_MISMATCH': 'Function {0} expects {1} parameters and received {2} parameters at line: {3} ',
        'REPEATED_DECLARATION': 'Repeated declaration of variable {0} found at line: {1} ',
        'REPEATED_FUNC_DECLARATION': 'Repeated declaration of function {0} found at line: {1} ',
        'UNDECLARED_VARIABLE': 'Undeclared variable {0} found at line: {1} ',
        'UNDECLARED_FUNCTION': 'Undeclared function {0} found at line: {1} ',
        'STACKOVERFLOW': 'Stackoverflow, the program is too big.',
        'PARAMETER_TYPE_MISMATCH': 'Function {0}, expected type {1} and received type {2} in position {3}',
        'PARAMETER_LENGTH_MISMATCH': 'Function {0}, expected {1} parameters'
}

current = {
    'scope': 'global',
    'id': None,
    'dimensionx': 0,
    'dimensiony': 0,
    'type': None,
    'params':[],
    'isfunc':False
}

func_dict = {}

debug = True
debug_var_const_dict = {}

var_dict = {
    'global' : {
     },
    'local' : {
    }
}

constant_dict = {
}

temp_dict = {
}

def get_constant_memory_address (constant, constant_type, memory):
    '''Gets memory for the constant if it doesn't yet exist in memory.'''
    if constant not in constant_dict:
        constant_dict[constant] = add_to_memory(memory, constant_type)
        debug_var_const_dict[constant_dict[constant]] = str(constant)

    return constant_dict[constant]

example_function = {
    'type' : 'void',
    'params' : [] # list of types
}



def print_current():
    print "\nCURRENT"
    pp.pprint(current)


def print_var_dict():
    print "\nVAR DICT"
    pp.pprint(var_dict)

def print_func_dict():
    print "\nFUNC DICT"
    pp.pprint(func_dict)


def var_exists_in_dict(vscope, vid):
    if vid in var_dict[vscope]:
        return True
    else:
        if vid in var_dict['global']:
            return True
        else:
            return False

def func_exists_in_dict(fid):
    if fid in func_dict:
        return True
    else:
        return False


def add_func_to_dict(fid, ftype, fparams):
    func_dict[fid] = {
        'type' : ftype,
        'params' : fparams
    }


def add_to_memory(memory, mtype):
    if mtype == 'bool':
        return memory.add_bool()
    elif mtype == 'int':
        return memory.add_int()
    elif mtype == 'float':
        return memory.add_float()
    elif mtype == 'char':
        return memory.add_char()
    elif mtype == 'string':
        return memory.add_string()
    else:
        print 'Invalid constant type. No memory for it.'
        exit(1)


def add_var_to_dict(vscope, vid, vtype, vdimensionx, vdimensiony, memory):
    var_dict[vscope][vid] = {
            'type' : vtype,
            'dimensionx' : vdimensionx,
            'dimensiony' : vdimensiony,
            'address' : add_to_memory(memory, vtype)
    }
    debug_var_const_dict[ var_dict[vscope][vid]['address'] ] = vid


def clear_current():
    current['id'] = None
    #current['scope'] = 'global'
    current['type'] = None
    current['params'] = []
    current['dimensionx'] = 0
    current['dimensiony'] = 0
    current['isfunc'] = False

def clear_local():
    var_dict['local'].clear()

semantics_cube = {
    # logical operators
    ('int', 'log', 'int') : 'bool',
    ('int', 'log', 'bool') : 'bool',
    ('int', 'log', 'float') : 'bool',
    ('int', 'log', 'string') : 'bool',
    ('int', 'log', 'char') : 'bool',
    ('bool', 'log', 'float') : 'bool',
    ('bool', 'log', 'char') : 'bool',
    ('bool', 'log', 'string') : 'bool',
    ('bool', 'log', 'bool') : 'bool',
    ('char', 'log', 'float') : 'bool',
    ('char', 'log', 'string') : 'bool',
    ('char', 'log', 'char') : 'bool',
    ('string', 'log', 'float') : 'bool',
    ('string', 'log', 'string') : 'bool',
    ('float', 'log', 'float') : 'bool',

    # comparators
    ('int', 'comp', 'int') : 'bool',
   #('int', 'comp', 'string') : 'bool',
    ('int', 'comp', 'char') : 'bool',
    ('int', 'comp', 'bool') : 'bool',
    ('int', 'comp', 'float') : 'bool',

    ('float', 'comp', 'float') : 'bool',

    ('bool', 'comp', 'bool') : 'bool',

    ('char', 'comp', 'char') : 'bool',
    ('char', 'comp', 'bool') : 'bool',
    ('char', 'comp', 'float') : 'bool',
   #('string', 'comp', 'string') : 'bool',

    # int with ___
    ('int', '+', 'int') : 'int',
    ('int', '+', 'string') : 'string',
    ('int', '+', 'char') : 'int',
    ('int', '+', 'bool') : 'int',
    ('int', '+', 'float') : 'float',

    ('int', '-', 'int') : 'int',
   #('int', '-', 'string') : 'string',
    ('int', '-', 'char') : 'int',
    ('int', '-', 'bool') : 'int',
    ('int', '-', 'float') : 'float',

    ('int', '*', 'int') : 'int',
   #('int', '*', 'string') : 'string',
    ('int', '*', 'char') : 'int',
   #('int', '*', 'bool') : 'int',
    ('int', '*', 'float') : 'float',

    ('int', '/', 'int') : 'int',
   #('int', '/', 'string') : 'string',
    ('int', '/', 'char') : 'int',
   #('int', '/', 'bool') : 'int',
    ('int', '/', 'float') : 'float',

   #('int', '=', 'string') : 'string',
    ('int', '=', 'int') : 'int',
    ('int', '=', 'char') : 'int',
   #('int', '=', 'bool') : 'int',
    ('int', '=', 'float') : 'int',

    # string with ___
    ('string', '+', 'string') : 'string',
    ('string', '+', 'char') : 'string',
    ('string', '+', 'bool') : 'string',
    ('string', '+', 'float') : 'string',

   #('string', '-', 'string') : 'string',
   #('string', '-', 'string') : 'string',
   #('string', '-', 'bool') : 'string',
   #('string', '-', 'char') : 'string',
   #('string', '-', 'float') : 'float',

   #('string', '*', 'string') : 'string',
   #('string', '*', 'string') : 'string',
   #('string', '*', 'char') : 'string',
   #('string', '*', 'bool') : 'string',
   #('string', '*', 'float') : 'float',

   #('string', '/', 'string') : 'string',
   #('string', '/', 'string') : 'string',
   #('string', '/', 'char') : 'string',
   #('string', '/', 'bool') : 'string',
   #('string', '/', 'float') : 'float',

    ('string', '=', 'string') : 'string',
    ('string', '=', 'char') : 'string',
    ('string', '=', 'bool') : 'string',
    ('string', '=', 'float') : 'string',

    # char with __
    ('char', '+', 'char') : 'int',
    ('char', '+', 'string') : 'string',
   #('char', '+', 'bool') : 'char',
    ('char', '+', 'float') : 'float',

    ('char', '-', 'char') : 'int',
   #('char', '-', 'string') : 'string',
   #('char', '-', 'bool') : 'char',
    ('char', '-', 'float') : 'float',

    ('char', '*', 'char') : 'int',
   #('char', '*', 'string') : 'string',
   #('char', '*', 'char') : 'char',
   #('char', '*', 'bool') : 'char',
    ('char', '*', 'float') : 'float',

    ('char', '/', 'char') : 'char',
   #('char', '/', 'string') : 'string',
   #('char', '/', 'char') : 'char',
   #('char', '/', 'bool') : 'char',
    ('char', '/', 'float') : 'float',

   #('char', '=', 'string') : 'string',
    ('char', '=', 'char') : 'char',
    ('char', '=', 'int') : 'char',
   #('char', '=', 'bool') : 'char',
   #('char', '=', 'float') : 'char',

    # bool with ___
    ('bool', '+', 'bool') : 'int',
    ('bool', '+', 'char') : 'int',
    ('bool', '+', 'float') : 'float',

    ('bool', '-', 'bool') : 'int',
   #('bool', '-', 'string') : 'string',
    ('bool', '-', 'char') : 'int',
    ('bool', '-', 'float') : 'float',

    ('bool', '*', 'bool') : 'int',
   #('bool', '*', 'string') : 'string',
    ('bool', '*', 'char') : 'int',
   #('bool', '*', 'bool') : 'bool',
    ('bool', '*', 'float') : 'float',

    ('bool', '/', 'bool') : 'int',
   #('bool', '/', 'string') : 'string',
    ('bool', '/', 'char') : 'int',
   #('bool', '/', 'bool') : 'bool',
    ('bool', '/', 'float') : 'float',

    ('bool', '=', 'string') : 'bool',
    ('bool', '=', 'bool') : 'bool',
    ('bool', '=', 'char') : 'bool',
    ('bool', '=', 'float') : 'bool',

    # float with float
    ('float', '=', 'float') : 'float',
    ('float', '+', 'float') : 'float',
    ('float', '-', 'float') : 'float',
    ('float', '*', 'float') : 'float',
    ('float', '/', 'float') : 'float'


}
