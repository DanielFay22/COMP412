"""
Container for general resources.
"""
import sys


instructions = [
    "load",     # 0
    "store",    # 1
    "loadI",    # 2
    "add",      # 3
    "sub",      # 4
    "mult",     # 5
    "lshift",   # 6
    "rshift",   # 7
    "output",   # 8
    "nop"       # 9
]

LOAD_VAL    = 0
STORE_VAL   = 1
LOADI_VAL   = 2
ADD_VAL     = 3
SUB_VAL     = 4
MULT_VAL    = 5
LSHIFT_VAL  = 6
RSHIFT_VAL  = 7
OUTPUT_VAL  = 8
NOP_VAL     = 9

categories = [
    'MEMOP',
    'LOADI',
    'ARITHOP',
    'OUTPUT',
    'NOP',
    'CONSTANT',
    'REGISTER',
    'COMMA',
    'INTO',
    'ENDFILE'
]

MEMOP_CAT       = categories.index('MEMOP')
LOADI_CAT       = categories.index('LOADI')
ARITHOP_CAT     = categories.index('ARITHOP')
OUTPUT_CAT      = categories.index('OUTPUT')
NOP_CAT         = categories.index('NOP')
CONSTANT_CAT    = categories.index('CONSTANT')
REGISTER_CAT    = categories.index('REGISTER')
COMMA_CAT       = categories.index('COMMA')
INTO_CAT        = categories.index('INTO')
ENDFILE_CAT       = categories.index('ENDFILE')


DIGITS = '0123456789'
WHITESPACE = ' \t'
NEWLINES = '\n\r'


def error(msg: str, err_type: str = "Error"):
    """
    Prints error message to stderr.
    """
    sys.stderr.write(f"{err_type}: {msg}\n")
