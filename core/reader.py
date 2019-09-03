



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
