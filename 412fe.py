

import sys
from dataclasses import dataclass






instructions = [
    "load",
    "loadI",
    "store",
    "add",
    "sub",
    "mult",
    "lshift",
    "rshift",
    "output",
    "nop"
]


@dataclass
class Operation(object):
    opCode: int

    sr1: int
    vr1: int
    pr1: int
    nu1: int

    sr2: int
    vr2: int
    pr2: int
    nu2: int

    sr3: int
    vr3: int
    pr3: int
    nu3: int

    next_op = None


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

def parse_line(fr: FileReader):
    """

    :param fr:
    :return:
    """
    line = []

    c = fr.read_char()

    if c == 'l':
        c2 = fr.read_char()

        if c2 == 'o': # load
            pass
        elif c2 == 's': # lshift
            chars = "hift"
            for char in chars:
                if fr.read_char() != char:
                    # Error
                    pass
            pass
        else: # Error
            pass


    elif c == 's':
        pass
    elif c == 'a':
        pass
    elif c == 'm':
        pass
    elif c == 'r':
        pass
    elif c == 'o':
        pass
    elif c == 'n':
        pass
    else:
        if not c: # EOF
            pass
        else: # Error
            pass





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




