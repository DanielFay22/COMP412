

from resources import *

from .reader import FileReader


class Scanner(object):

    chars = []
    
    def __init__(self, fr: FileReader):

        self._fr = fr

        self.ln = 0

        self.token_queue = []

    def get_token(self) -> Token:
        """
        Reads the file and returns the next token.

        If there is an error during reading, reports the error and returns an Error token.
        """
        

        if self.token_queue:
            return self.token_queue.pop(0)
        if not self.chars:
            c = self._fr.read_char()
            self.chars.append(c)
        else:
            c = self.chars[-1]

        # load, loadI, lshift
        if c == 'l':
            c2 = self._fr.read_char()
            self.chars.append(c2)

            if c2 == 'o':  # load
                if self._read_remaining_token("ad"):
                    self.chars.append(self._fr.read_char())

                    if self.chars[-1] == 'I':
                        self.chars = []
                        return LOADI(ln = self.ln)
                    else:
                        self.chars = self.chars[-1:]
                        return MEMOP(ln = self.ln, value = LOAD_VAL)

                else:
                    self._error(self.chars)
            elif c2 == 's':  # lshift
                if self._read_remaining_token("hift"):
                    self.chars = []
                    return ARITHOP(value=LSHIFT_VAL, ln = self.ln)
                else:
                    # Return error token
                    self._error(self.chars)

            else:
                self._error(self.chars)

        # store, sub
        elif c == 's':
            c2 = self._fr.read_char()
            self.chars.append(c2)

            # store
            if c2 == 't':
                if self._read_remaining_token("ore"):
                    self.chars = []
                    return MEMOP(ln = self.ln, value = STORE_VAL)
                else:
                    self._error(self.chars)

            # sub
            elif c2 == 'u':
                self.chars.append(self._fr.read_char())
                if self.chars[-1] == 'b':
                    self.chars = []
                    return ARITHOP(ln = self.ln, value = SUB_VAL)
                else:
                    self._error(self.chars)

            # error
            else:
                self._error(self.chars)

        # add
        elif c == 'a':
            if self._read_remaining_token("dd"):
                self.chars = []
                return ARITHOP(value = ADD_VAL, ln = self.ln)
            else:
                self._error(self.chars)

        # mult
        elif c == 'm':
            if self._read_remaining_token("ult"):
                self.chars = []
                return ARITHOP(value = MULT_VAL, ln = self.ln)
            else:
                self._error(self.chars)

        # rshift, register
        elif c == 'r':
            c2 = self._fr.read_char()
            self.chars.append(c2)

            if c2 == "s":
                if self._read_remaining_token("hift"):
                    self.chars = []
                    return ARITHOP(value = RSHIFT_VAL, ln = self.ln)
                else:
                    self._error(self.chars)

            elif c2.isnumeric():
                if c2 == '0':
                    self.chars = []
                    return REGISTER(value = 0, ln = self.ln)
                else:
                    return REGISTER(
                        value = self._read_constant(first_digit = int(c2)), ln = self.ln
                    )
            else:
                self._error(self.chars)

        # output
        elif c == 'o':

            if self._read_remaining_token("utput"):
                self.chars = []
                return OUTPUT(ln = self.ln)
            else:
                self._error(self.chars)

        # nop
        elif c == 'n':

            if self._read_remaining_token("op"):
                self.chars = []
                return NOP(ln = self.ln)
            else:
                self._error(self.chars)

        # comma
        elif c == ',':
            self.chars = []
            return COMMA(ln = self.ln)

        # constant
        elif c.isnumeric():
            if c == '0':
                self.chars = []
                return CONSTANT(value = 0, ln = self.ln)
            else:
                # read_constant() handles clearing character buffer
                return CONSTANT(
                    value = self._read_constant(first_digit = int(c)), ln = self.ln
                )

        # into
        elif c == '=':
            if self._read_remaining_token('>'):
                self.chars = []
                return INTO(ln = self.ln)
            else:
                self._error(self.chars)

        # newline
        elif c == '\n':
            self.ln += 1
            self.chars = []
            return self.get_token()

        # comment
        elif c == '/':
            c2 = self._fr.read_char()

            if c2 == '/':
                # read rest of line
                self._read_to_line_end()
                self.chars = []
                return self.get_token()
            else:
                # return error token
                self._error(self.chars + [c2])

        # whitespace
        elif c.isspace():
            self.chars = []
            return self.get_token()

        else:
            if not c:  # EOF
                return ENDFILE(ln = self.ln)
            else:  # Error
                self._error(self.chars)

        self.chars = []

    def _read_to_line_end(self):
        """
        Reads characters until it encounters the end of the line.
        """
        c = self._fr.read_char()
        while c and c != '\n':
            c = self._fr.read_char()

    def _read_remaining_token(self, expected: str) -> bool:
        for e in expected:
            self.chars.append(self._fr.read_char())
            if self.chars[-1] != e:
                return False

        return True

    def _read_constant(self, first_digit: int) -> int:

        s = first_digit
        self.chars.append(self._fr.read_char())

        while self.chars[-1].isnumeric():
            s = s * 10 + int(self.chars[-1])
            self.chars.append(self._fr.read_char())

        self.chars = self.chars[-1:]
        # if not c.isspace():
        #     self.token_queue.append(
        #         self.get_token(init_char = c)
        #     )

        return s

    def _error(self, chars: list) -> None:
        """
        Reports error message for scanning.
        """
        error(f"{self.ln}: Invalid token {''.join(chars)}.", "Lexical Error")
