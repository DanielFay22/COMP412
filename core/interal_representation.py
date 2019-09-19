

from resources import *


class InternalRepresentation(object):

    def __init__(self):
        self._ir: list = [None] * 16
        self._ir[IR_LN] = 0

        self._head = self._ir

        self.count = 0

        self.max_reg = 0
        self.active = None

    @property
    def ir(self):
        return self._ir

    @property
    def head(self):
        return self._head

    def add_token(self, op, r1, r2, r3) -> None:
        """
        Enters a new operation to the current IR and increments the head.
        """
        l = [None] * 16
        l[IR_PREV] = self._head
        self._head[IR_NEXT] = l
        l[IR_LN] = self._head[IR_LN] + 1

        self._head[0] = op
        self._head[1] = r1
        self._head[5] = r2
        self._head[9] = r3

        self._head = l

        self.count += 1

    def print_ir(self):
        s = ""

        l = self._ir

        while l is not self._head:
            s += str([instructions[l[0]]] + l[1:-2:4]) + "\n"
            l = l[-2]

        print(s)

    def to_code(self, header: str = ""):
        """
        Prints internal representation as ILOC assembly code.
        """
        s = header

        l = self._ir

        while l is not self._head:
            s += self._gen_line_str(l)
            l = l[-2]

        print(s)

    @staticmethod
    def _gen_line_str(l):
        """
        Constructs ILOC assembly code for a single operation in IR form.
        """
        i = "\t"

        i += instructions[l[0]]

        regs = l[1:-2:4]
        vregs = l[2:-2:4]

        if not (l[0] == LOADI_VAL or l[0] == OUTPUT_VAL):
            i += '\tvr' + str(vregs[0])
        else:
            i += '\t' + str(regs[0])

        if l[0] != STORE_VAL:
            if regs[1] is not None:
                i += ', vr' + str(vregs[1])
            else:
                i += '\t'

            if regs[2] is not None:
                i += '\t=> vr' + str(vregs[2]) + '\n'
            else:
                i += '\n'
        else:
            i += '\t\t=> vr' + str(vregs[1]) + '\n'

        return i
