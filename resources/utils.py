"""
Container for general resources.
"""

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
ENDFILE_CAT     = categories.index('ENDFILE')


DIGITS = '0123456789'
WHITESPACE = ' \t'
NEWLINES = '\n\r'

# indices for each component of the token structure
TOK_ID  = 0
TOK_VAL = 1
TOK_LN  = 2



IR_OP       = 0
IR_R1       = 1
IR_VR1      = 2
IR_PR1      = 3
IR_NU1      = 4
IR_R2       = 5
IR_VR2      = 6
IR_PR2      = 7
IR_NU2      = 8
IR_R3       = 9
IR_VR3      = 10
IR_PR3      = 11
IR_NU3      = 12
IR_LN       = 13
IR_IND      = 14