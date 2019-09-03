

from .utils import *


class Token(object):

    def __init__(self, id, value):

        self.id = id

        self.val = value

    def name(self):
        return "TOKEN"

    def __repr__(self):
        return "< " + self.__class__.__name__ + "\t, " + "\"" + self.name() + "\" >"


class Op(Token):

    def __init__(self, id: int, value: int):
        super(Op, self).__init__(id = id, value = value)

    def name(self):
        return instructions[self.val]

# Category 0
class MEMOP(Op):

    def __init__(self, value: int):
        super(MEMOP, self).__init__(id = MEMOP_CAT, value = value)


# Category 1
class LOADI(Op):

    # Only token value is "loadI", which has value 2
    def __init__(self, value: int = None):
        super(LOADI, self).__init__(id = LOADI_CAT, value = LOADI_VAL)

# Category 2
class ARITHOP(Op):

    def __init__(self, value: int):
        super(ARITHOP, self).__init__(id = ARITHOP_CAT, value = value)

# Category 3
class OUTPUT(Op):

    # Only token value is "output", which has value 8
    def __init__(self, value: int = None):
        super(OUTPUT, self).__init__(id = OUTPUT_CAT, value = OUTPUT_VAL)

# Category 4
class NOP(Op):

    # Only token value is "nop", which has value 9
    def __init__(self, value: int = None):
        super(NOP, self).__init__(id = NOP_CAT, value = NOP_VAL)

# Category 5
class CONSTANT(Token):

    def __init__(self, value: int):
        super(CONSTANT, self).__init__(id = CONSTANT_CAT, value = value)

    def name(self):
        return str(self.val)

# Category 6
class REGISTER(Token):

    def __init__(self, value: int):
        super(REGISTER, self).__init__(id = REGISTER_CAT, value = value)

    def name(self):
        return "r" + str(self.val)

# Category 7
class COMMA(Token):

    def __init__(self, value: int = None):
        super(COMMA, self).__init__(id = COMMA_CAT, value = None)

    def name(self):
        return ","

# Category 8
class INTO(Token):

    def __init__(self, value: int = None):
        super(INTO, self).__init__(id = INTO_CAT, value = None)

    def name(self):
        return "=>"

class NewLine(Token):

    def __init__(self):
        super(NewLine, self).__init__(id = NEWLINE_CAT, value = None)

    def name(self):
        return '\\n'

class Error(Token):

    def __init__(self, message: str):
        super(Error, self).__init__(id = ERROR_CAT, value = None)

        self.message = message

    def name(self):
        return self.message