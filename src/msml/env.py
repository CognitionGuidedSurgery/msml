# -*- encoding: utf-8 -*-

"""
Environment things, such as defining alphabet search path, 
defining msml-wide options and user configuration

"""


__author__ = "Alexander Weigl"
__date__ = "2014-01-25"


from path import path
import os
from msml.model.alphabet import Alphabet, PythonOperator, Argument, SharedObjectOperator, ShellOperator

# msml alphabet search path
alphabet_search_paths = list()

# the current alphabet
current_alphabet = None

# path where the msml file resides
msml_file_path = None

def load_user_file(loc = "~/.config/msmlrc.py"):
        global alphabet_search_paths
        loc = path(loc).expanduser()
        if loc.exists():
            execfile(loc, {"alphabet_search_path" : alphabet_search_paths})
        else:
            env_path = path(__file__)
            alphabet__path = env_path.dirname() / '..' / '..' / 'share' / 'alphabet'
            alphabet_search_paths.append(alphabet__path)

            import msml.envconfg as C
            import sys
            #Import release and debug paths here?
            sys.path.append(C.operators_path)
            sys.path.append(C.operators_path_debug)
            sys.path.append(C.operators_path_release)
            
            #Add windows paths to python path - Python sometimes only checks this directories for dependencies (e.g. boost dlls)
            win_path = os.environ.get('path')
            if win_path is not None:       
                win_paths = win_path.split(';')
                for currentPath in win_paths:
                    sys.path.append(currentPath)
            





def gather_alphabet_files():
    """
    finds all xml files in the alphabet_search_paths  
    """
    files = []
    for loc in alphabet_search_paths:
        loc = path(loc)
        if loc.isfile():
            files.append(loc)
        else:
            files += loc.walkfiles("*.xml" , errors= 'warn')
    return files

def load_alphabet(fil = "alphabet.cache"):
    p = path(fil).expanduser().expandvars()

    if p.exists():
        global current_alphabet
        current_alphabet = Alphabet.load(p);
        return current_alphabet
    else:
        print("WARNING: alphabet file »%s« not found, please run msml.py alphabet" % fil)
        return None

def _debug_install_operators():
    global current_alphabet
    current_alphabet = Alphabet()

    op_square = PythonOperator("square", [Argument('n', 'int', None, True)],
                                         [Argument('n', 'int', None, True)],
                                         runtime = {'exec':'python', 'module': 'test', 'function': 'square'})

    op_square.function = lambda n: int(n) ** 2

    op_output = PythonOperator("output", [Argument('object', '*', None, True)],
                                         runtime = {'exec':'python', 'module': 'pprint', 'function': 'pprint'})

    op_output.bind_function()
    
    op_ctype = SharedObjectOperator("ctime", None, [Argument('time', 'int', None, True)],
                        runtime = {'exec':'so', 'file': 'libc.so.6', 'symbol': 'time'})
    op_ctype.bind_function()

    op_id = ShellOperator("id", [Argument('name', 'string', None, True)],
                                         runtime = {'exec':'sh', 'template' : 'id {name}'})

    current_alphabet.append((op_square, op_output, op_ctype, op_id))

