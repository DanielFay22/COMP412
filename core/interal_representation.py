

from resources import *


class InternalRepresentation(object):

    def __init__(self):
        self._ir = []

        self.count = 0

        self.max_reg = 0
        self.active = None
        self.index = 0

    @property
    def ir(self):
        return self._ir

    def add_token(self, op, r1, r2, r3) -> None:
        """
        Enters a new operation to the current IR and increments the head.
        """
        l = [None] * 16

        l[IR_OP] = op
        l[IR_R1] = r1
        l[IR_R2] = r2
        l[IR_R3] = r3

        l[IR_LN] = self.count
        self.count += 1

        self._ir.append(l)

    def add_full_token(self, op,
                       r1=None, vr1=None, pr1=None, nu1=None,
                       r2=None, vr2=None, pr2=None, nu2=None,
                       r3=None, vr3=None, pr3=None, nu3=None):
        """

        """
        l = [None] * 16

        l[IR_OP] = op

        l[IR_R1] = r1
        l[IR_VR1] = vr1
        l[IR_PR1] = pr1
        l[IR_NU1] = nu1

        l[IR_R2] = r2
        l[IR_VR2] = vr2
        l[IR_PR2] = pr2
        l[IR_NU2] = nu2

        l[IR_R3] = r3
        l[IR_VR3] = vr3
        l[IR_PR3] = pr3
        l[IR_NU3] = nu3

        l[IR_LN] = self.count
        self.count += 1

        self._ir.append(l)


    def print_ir(self):
        s = ""

        for l in self._ir:
            s += str([instructions[l[0]]] + l[1:-2:4]) + "\n"

        print(s)

    def to_code(self, header: str = ""):
        """
        Prints internal representation as ILOC assembly code.
        """
        s = header

        for l in self._ir:
            s += self._gen_line_str_v(l)

        print(s)

    @staticmethod
    def _gen_line_str(l):
        """
        Constructs ILOC assembly code for a single operation in IR form.
        """
        i = "\t"

        i += instructions[l[0]]

        regs = l[1:-2:4]

        if not (l[0] == LOADI_VAL or l[0] == OUTPUT_VAL):
            i += '\tr' + str(regs[0])
        else:
            i += '\t' + str(regs[0])

        if l[0] != STORE_VAL:
            if regs[1] is not None:
                i += ', r' + str(regs[1])
            else:
                i += '\t'

            if regs[2] is not None:
                i += '\t=> r' + str(regs[2]) + '\n'
            else:
                i += '\n'
        else:
            i += '\t\t=> r' + str(regs[1]) + '\n'

        return i

    @staticmethod
    def _gen_line_str_v(l):
        """
        Constructs ILOC assembly code for a single operation in IR form.
        """
        i = "\t"

        i += instructions[l[0]]

        if l[0] == NOP_VAL:
            return i + '\n'

        regs = l[1:-2:4]
        vregs = l[2:-2:4]

        if not (l[0] == LOADI_VAL or l[0] == OUTPUT_VAL):
            i += '\tr' + str(vregs[0])
        else:
            i += '\t' + str(regs[0])

        if l[0] != STORE_VAL:
            if regs[1] is not None:
                i += ', r' + str(vregs[1])
            else:
                i += '\t'

            if regs[2] is not None:
                i += '\t=> r' + str(vregs[2]) + '\n'
            else:
                i += '\n'
        else:
            i += '\t\t=> r' + str(vregs[1]) + '\n'

        return i