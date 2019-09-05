



class FileReader(object):
    """
    Buffered IO object. Supports reading a file one character at a time,
    with an internal buffer to limit overhead.
    """

    bufsize = 8192*2

    def __init__(self, fn: str):
        self.file = open(fn, "r")

        self.pos = 0
        self.buf = ""

        self.EOF = False

    def read_buf(self):
        self.buf = self.file.read(self.bufsize)

        self.pos = 0

    def read_char(self):
        """
        Return the next character from the buffer, refilling the buffer if necessary.
        """
        try:

            self.pos += 1
            return self.buf[self.pos - 1]

        except IndexError:
            self.read_buf()

            try:
                self.pos += 1
                return self.buf[self.pos - 1]

            except IndexError:
                self.EOF = True
                return None

    def close(self):
        self.file.close()
        del self

