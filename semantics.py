#!env/bin/python
import pprint

pp = pprint.PrettyPrinter()

errors = {
        'REPEATED_DECLARATION': 'Repeated declaration found at: '
}

current = {
    'scope': 'global',
    'id': None,
    'dimensionx': 0,
    'dimensiony': 0,
    'type': None,
    'params':[]
}

scopes_and_vars = {
    'global' : {
        'vars' : {}
     },
    'main' : {
        'vars' : {}
    }
}

def print_current():
    print "\nCURRENT"
    pp.pprint(current)


def print_full_dict():
    print "\nSCOPES AND VARS"
    pp.pprint(scopes_and_vars)


def var_exists_in_dict(vscope, vid):
    if scopes_and_vars[ current['scope'] ]['vars'].get(current['id']) is None:
        if scopes_and_vars['global']['vars'].get(current['id']) is None:
            return False
        else:
            return True
    else:
        return True



def add_function_to_dict(fid, ftype, fparams):
    scopes_and_vars[fid] = {
        'type' : ftype,
        'params' : fparams,
        'vars' : {}
    }


def add_var_to_scope(vscope, vid, vtype, vdimensionx, vdimensiony):
    scopes_and_vars[vscope]['vars'][vid] = {
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

