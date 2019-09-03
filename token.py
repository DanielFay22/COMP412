

from resources import *


class Token(object):

    def __init__(self, id, value):

        self.id = id

        self.val = value

    def name(self):
        return "TOK"

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
        super(MEMOP, self).__init__(id = 0, value = value)


# Category 1
class LOADI(Op):

    # Only token value is "loadI", which has value 2
    def __init__(self, value: int = None):
        super(LOADI, self).__init__(id = 1, value = 2)

# Category 2
class ARITHOP(Op):

    def __init__(self, value: int):
        super(ARITHOP, self).__init__(id = 2, value = value)

# Category 3
class OUTPUT(Op):

    # Only token value is "output", which has value 8
    def __init__(self, value: int = None):
        super(OUTPUT, self).__init__(id = 3, value = 8)

# Category 4
class NOP(Op):

    # Only token value is "nop", which has value 9
    def __init__(self, value: int = None):
        super(NOP, self).__init__(id = 4, value = 9)

# Category 5
class CONSTANT(Token):

    def __init__(self, value: int):
        super(CONSTANT, self).__init__(id = 5, value = value)

    def name(self):
        return str(self.val)

# Category 6
class REGISTER(Token):

    def __init__(self, value: int):
        super(REGISTER, self).__init__(id = 6, value = value)

    def name(self):
        return "r" + str(self.val)

# Category 7
class COMMA(Token):

    def __init__(self, value: int = None):
        super(COMMA, self).__init__(id = 5, value = None)

    def name(self):
        return ","

# Category 8
class INTO(Token):

    def __init__(self, value: int = None):
        super(INTO, self).__init__(id = 5, value = None)

    def name(self):
        return "=>"