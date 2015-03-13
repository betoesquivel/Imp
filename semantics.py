#!env/bin/python
import pprint

pp = pprint.PrettyPrinter()

errors = {
        'REPEATED_DECLARATION': 'Repeated declaration of variable {0} found at line: {1} ',
        'REPEATED_FUNC_DECLARATION': 'Repeated declaration of function {0} found at line: {1} ',
        'UNDECLARED_VARIABLE': 'Undeclared variable {0} found at line: {1} '
}

current = {
    'scope': 'global',
    'id': None,
    'dimensionx': 0,
    'dimensiony': 0,
    'type': None,
    'params':[]
}

func_dict = {}

var_dict = {
    'global' : {
     },
    'local' : {
    }
}

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


def add_var_to_dict(vscope, vid, vtype, vdimensionx, vdimensiony):
    var_dict[vscope][vid] = {
            'type' : vtype,
            'dimensionx' : vdimensionx,
            'dimensiony' : vdimensiony
    }


def clear_current():
    current = {
        'scope': 'global',
        'id': None,
        'type': None,
        'params': [],
        'dimensionx': 0,
        'dimensiony': 0
    }

def clear_local():
    var_dict['local'].clear()
