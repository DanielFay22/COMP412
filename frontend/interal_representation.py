
from typing import Union

from resources import *


class InternalRepresentation(object):

    def __init__(self, init_size: int = 1000):
        self._ir = self._gen_empty_ir(init_size)

        self._head = self._ir

        self.count = 0

    @staticmethod
    def _gen_empty_ir(n: int = 1000) -> list:
        """
        Generates an empty internal representation
        """
        l = [[None] * 15 for _ in range(n)]

        for x in range(n - 1):
            l[x][-2] = l[x + 1]
            l[x + 1][-1] = l[x]

        return l[0]

    def _expand_ir(self) -> None:
        ir = self._gen_empty_ir()

        self._head[-2] = ir
        ir[-1] = self._head

    def add_token(
            self, op: int,
            r1: Union[int, None],
            r2: Union[int, None],
            r3: Union[int, None]) -> None:
        """
        Enters a new operation to the current IR and increments the head.
        """
        self._head[0] = op
        self._head[1] = r1
        self._head[5] = r2
        self._head[9] = r3

        if self._head[-2] is None:
            self._expand_ir()

        self._head = self._head[-2]

        self.count += 1

    def print_ir(self):
        s = ""

        l = self._ir

        while l is not self._head:
            s += str([instructions[l[0]]] + l[1:-2:4]) + "\n"
            l = l[-2]

        print(s)

    def pprint_ir(self):
        """
        Prints internal representation as ILOC assembly code.
        """
        s = ""

        l = self._ir

        while l is not self._head:
            s += self._gen_line_str(l)#str([instructions[l[0]]] + l[1:-2:4]) + "\n"
            l = l[-2]

        print(s)

    @staticmethod
    def _gen_line_str(l):
        """
        Constructs ILOC assembly code for a single operation in IR form.
        """
        i = instructions[l[0]]

        regs = l[1:-2:4]

        if not (l[0] == LOADI_VAL or l[0] == OUTPUT_VAL):
            i += '\tr' + str(regs[0])
        else:
            i += '\t' + str(regs[0])

        if regs[1]:
            i += ',r' + str(regs[1])

        if regs[2]:
            i += ' => r' + str(regs[2]) + '\n'

        return i
