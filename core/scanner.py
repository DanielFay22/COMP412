

from resources import *

from .reader import FileReader


class Scanner(object):

    def __init__(self, fr: FileReader):

        self._fr = fr

        self.ln = 0

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

        elif c == '\n':
            self.ln += 1
            return self.get_token()

        elif c == '/':
            c2 = self._fr.read_char()
            if c2 == '/':
                # read rest of line
                pass
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
