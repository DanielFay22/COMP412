

import sys
from resources import *



class FileReader(object):
    """
    Buffered IO object. Supports reading a file one character at a time,
    with an internal buffer to limit overhead.
    """

    bufsize = 4096

    def __init__(self, fn: str):
        self.file = open(fn, "r")

        self.pos = 0
        self.buf = ""

        self.EOF = False

    def read_buf(self):
        self.buf = self.file.read(self.bufsize)

        self.pos = 0

        return len(self.buf)

    def read_char(self):
        if self.pos >= len(self.buf):
            s = self.read_buf()
            if not s:
                self.EOF = True
                return ""

        c = self.buf[self.pos]
        self.pos += 1

        return c



class InternalRepresentation(object):

    def __init__(self, init_size: int = 1000):
        self._ir = self._gen_empty_ir(init_size)

        self._head = self._ir

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

    def add_token(self, op: int, r1: int, r2: int, r3: int) -> None:
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


class Scanner(object):

    def __init__(self, fr: FileReader):

        self._fr = fr

        self.token_queue = []

    def get_token(self, init_char: str = None) -> Token:
        """
        Reads the file and returns the next token.

        If there is an error during reading, reports the error and returns an Error token.
        """
        if self.token_queue:
            return self.token_queue.pop(0)
        if init_char is None:
            c = self._fr.read_char()
        else:
            c = init_char

        # load, loadI, lshift
        if c == 'l':
            c2 = self._fr.read_char()

            if c2 == 'o':  # load
                pass
            elif c2 == 's':  # lshift

                if self._read_remaining_token("hift"):
                    return ARITHOP(value=LSHIFT_VAL)
                else:
                    # Return error token
                    pass

            else:  # Error
                pass

        # store, sub
        elif c == 's':
            pass
        # add
        elif c == 'a':
            if self._read_remaining_token("dd"):
                return ARITHOP(value = ADD_VAL)
            else:
                # return error token
                pass
        # mult
        elif c == 'm':

            if self._read_remaining_token("ult"):
                return ARITHOP(value = MULT_VAL)
            else:
                # return error token
                pass

        # rshift, register
        elif c == 'r':
            c2 = self._fr.read_char()

            if c2 == "s":
                if self._read_remaining_token("hift"):
                    return ARITHOP(value = RSHIFT_VAL)
                else:
                    # return error token
                    pass
            elif c2.isnumeric():
                if c2 == '0':
                    return REGISTER(value = 0)
                else:
                    return REGISTER(
                        value = self._read_constant(first_digit = int(c2))
                    )
            else:
                # Error
                pass

        # output
        elif c == 'o':
            if self._read_remaining_token("utput"):
                return OUTPUT()
            else:
                # return error token
                pass

        # nop
        elif c == 'n':
            if self._read_remaining_token("op"):
                return NOP()
            else:
                # return error token
                pass

        # comma
        elif c == ',':
            return COMMA()

        elif c.isnumeric():
            if c == '0':
                return CONSTANT(value = 0)
            else:
                return CONSTANT(
                    value = self._read_constant(first_digit = int(c))
                )

        # into
        elif c == '=':
            if self._read_remaining_token('>'):
                return INTO()
            else:
                # return error token
                pass

        else:
            if not c:  # EOF
                pass
            else:  # Error
                pass

    def _read_remaining_token(self, expected: str) -> bool:

        for e in expected:
            if self._fr.read_char() != e:
                # Error
                return False

        return True

    def _read_constant(self, first_digit: int) -> int:

        s = first_digit
        c = self._fr.read_char()

        while c.isnumeric():
            s = s * 10 + int(c)
            c = self._fr.read_char()

        if not c.isspace():
            self.token_queue.append(
                self.get_token(init_char = c)
            )

        return s



def help_handler():

    print("COMP 412, Fall 2019 Front End (lab 1)\n"
          "Command Syntax:\n"
          "\t./lab1_ref [flags] filename\n"
          "\n"
          "Required arguments:\n"
          "\tfilename  is the pathname (absolute or relative) to the input file\n"
          "\n"
          "Optional flags:\n"
          "\t-h       prints this message\n"
          "\t-l       Opens log file \"./Log\" and starts logging.\n"
          "\t-s       prints tokens in token stream\n"
          "\t-p       invokes parser and reports on success or failure\n"
          "\t-r       prints human readable version of parser's IR")






if __name__ == "__main__":
    argv = sys.argv[1:]

    p = False
    s = False
    r = False

    filename = None

    # Invalid
    if not len(argv):
        pass
    else:
        while argv:
            arg = argv.pop(0)

            if arg == "-h":
                help_handler()
                exit(0)
            elif arg == "-p":
                p = True
            elif arg == "-s":
                p = True
            elif arg == "-r":

                p = True
            else:
                pass




