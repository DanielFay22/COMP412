

from .utils import instructions, categories
from .utils import LOAD_VAL, STORE_VAL, LOADI_VAL, ADD_VAL, SUB_VAL, \
    MULT_VAL, LSHIFT_VAL, RSHIFT_VAL, OUTPUT_VAL, NOP_VAL
from .utils import MEMOP_CAT, LOADI_CAT, ARITHOP_CAT, OUTPUT_CAT, NOP_CAT, \
    REGISTER_CAT, CONSTANT_CAT, COMMA_CAT, INTO_CAT, ENDFILE_CAT
from .utils import error

from .token import Token, MEMOP, LOADI, ARITHOP, OUTPUT, \
    NOP, CONSTANT, REGISTER, COMMA, INTO, ENDFILE