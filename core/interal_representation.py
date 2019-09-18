

from resources import *


class InternalRepresentation(object):

    def __init__(self):
        self._ir = [None]*15

        self._head = self._ir

        self.count = 0

    def add_token(self, op, r1, r2, r3) -> None:
        """
        Enters a new operation to the current IR and increments the head.
        """
        l = [None] * 15
        l[-1] = self._head
        self._head[-2] = l

        self._head[0] = op
        self._head[1] = r1
        self._head[5] = r2
        self._head[9] = r3

        self._head = l

        # if self._head[-2] is None:
        #     self._expand_ir()
        #
        # self._head = self._head[-2]

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

        if not (l[0] == LOADI_VAL or l[0] == OUTPUT_VAL):
            i += '\tr' + str(regs[0])
        else:
            i += '\t' + str(regs[0])

        if regs[1] is not None:
            i += ', r' + str(regs[1])
        else:
            i += '\t'

        if regs[2] is not None:
            i += '\t=> r' + str(regs[2]) + '\n'
        else:
            i += '\n'

        return i
