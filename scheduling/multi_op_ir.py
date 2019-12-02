
from resources import *


class MultiInternalRepresentation(object):


    def __init__(self):

        self._ir = []

    def add_op(self, ops):
        if len(ops) == 1:
            ops += ([NOP_VAL] + [None] * 13,)
        self._ir.append(ops)

    def add_nop(self):
        self._ir.append(
            ([NOP_VAL] + [None] * 13, [NOP_VAL] + [None] * 13)
        )

    def to_code(self, header=""):

        s = header

        for l in self._ir:
            s += "[" + self.to_code_op(l[0]) + ";" + self.to_code_op(l[1]) + "]\n"
        print(s)
        print(len(s.splitlines()))
        
    @staticmethod
    def to_code_op(op):

        i = ""

        i += instructions[op[IR_OP]]

        if op[0] == NOP_VAL:
            return i

        regs = op[1:-2:4]
        vregs = op[2:-2:4]

        if not (op[IR_OP] == LOADI_VAL or op[IR_OP] == OUTPUT_VAL):
            i += ' r' + str(vregs[0])
        else:
            i += ' ' + str(regs[0])

        if op[0] != STORE_VAL:
            if vregs[1] is not None:
                i += ', r' + str(vregs[1])

            if vregs[2] is not None:
                i += ' => r' + str(vregs[2])

        else:
            i += ' => r' + str(vregs[1])

        return i