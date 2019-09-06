
from resources import *
from .reader import FileReader


class Scanner(object):

    chars = []
    
    def __init__(self, fr: FileReader):

        self._fr = fr

        self.ln = 1
        
        self.read_char = self._fr.read_char

    def get_token(self):
        """
        Reads the file and returns the next token.

        If there is an error during reading, reports the error and returns an Error token.
        """
        # map function to local variable
        
        if not self.chars:
            c = self.read_char()
            self.chars.append(c)
        else:
            c = self.chars[-1]

        # whitespace
        if c == ' ' or c == '\t':
            self.chars *= 0
            return self.get_token()

        # rshift, register
        elif c == 'r':
            r = self._scan_r()

            if r: return r

        # load, loadI, lshift
        elif c == 'l':
            r = self._scan_l()

            if r: return r

        # store, sub
        elif c == 's':
            r = self._scan_s()

            if r: return r

        # add
        elif c == 'a':
            if self._read_remaining_token("dd"):
                return ARITHOP_CAT, ADD_VAL, self.ln

        # mult
        elif c == 'm':
            if self._read_remaining_token("ult"):
                return ARITHOP_CAT, MULT_VAL, self.ln

        # output
        elif c == 'o':

            if self._read_remaining_token("utput"):
                return OUTPUT_CAT, OUTPUT_VAL, self.ln

        # nop
        elif c == 'n':
            if self._read_remaining_token("op"):
                return NOP_CAT, NOP_VAL, self.ln

        # comma
        elif c == ',':
            self.chars *= 0
            return COMMA_CAT, None, self.ln

        # into
        elif c == '=':
            if self._read_remaining_token('>'):
                return INTO_CAT, None, self.ln

        # comment
        elif c == '/':
            c2 = self.read_char()
            self.chars.append(c2)

            if c2 == '/':
                # read rest of line
                self._read_to_line_end()
                self.chars *= 0
                return self.get_token()
            else:
                # return error token
                self._lexical_error(self.chars)

        elif not c:  # EOF
            return ENDFILE_CAT, None, self.ln

        # constant
        elif c in DIGITS:
            return CONSTANT_CAT, self._read_constant(first_digit=int(c)), self.ln

        # newline
        elif c == '\n' or c == '\r':
            self.ln += 1
            self.chars *= 0
            return self.get_token()

        else:
            # Error
            self._lexical_error(self.chars)

        self.chars *= 0

    def _scan_l(self) -> tuple:
        """
        Handler for scanning tokens beginning with 'l'.
        """
        c2 = self._fr.read_char()
        self.chars.append(c2)

        if c2 == 'o':  # load
            if self._read_remaining_token("ad"):
                f = self._read_remaining_token("I", verbose=False)

                if f:
                    return LOADI_CAT, LOADI_VAL, self.ln
                elif (not f) and (self.chars[-1] == ' ' or self.chars[-1] == '\t'):
                    self.chars = []
                    return MEMOP_CAT, LOAD_VAL, self.ln
                else:
                    self._whitespace_error()

        elif c2 == 's':  # lshift
            if self._read_remaining_token("hift"):
                return ARITHOP_CAT, LSHIFT_VAL, self.ln

        else:
            self._lexical_error(self.chars)

    def _scan_s(self) -> tuple:
        """
        Handler for scanning tokens beginning with 's'.
        """
        c2 = self._fr.read_char()
        self.chars.append(c2)

        # store
        if c2 == 't':
            if self._read_remaining_token("ore"):
                return MEMOP_CAT, STORE_VAL, self.ln

        # sub
        elif c2 == 'u':
            if self._read_remaining_token("b"):
                return ARITHOP_CAT, SUB_VAL, self.ln

        # error
        else:
            self._lexical_error(self.chars)

    def _scan_r(self) -> tuple:
        """
        Handler for scanning tokens beginning with 'r'.
        """
        c2 = self._fr.read_char()
        self.chars.append(c2)

        if c2 == "s":
            if self._read_remaining_token("hift"):
                return ARITHOP_CAT, RSHIFT_VAL, self.ln

        elif c2 in DIGITS:
            return REGISTER_CAT, self._read_constant(first_digit=int(c2)), self.ln

        else:
            self._lexical_error(self.chars)

    def _read_to_line_end(self):
        """
        Reads characters until it encounters the end of the line.
        """
        new_char = self._fr.read_char
        c = new_char()
        while c and c not in NEWLINES:
            c = new_char()
        self.ln += 1

    def _read_remaining_token(self, expected: str, verbose: bool = True) -> bool:
        """
        Reads the next n characters (where n is the length of expected) and
        returns True iff the characters match the expected.

        If whitespace is True, checks that the character following the token is a whitespace character.
        """
        append = self.chars.append
        for e in expected:
            append(self._fr.read_char())
            if self.chars[-1] != e:
                if verbose:
                    self._lexical_error(self.chars)
                return False

        self.chars *= 0
        return True

    def _read_constant(self, first_digit: int) -> int:

        s = first_digit
        c = self._fr.read_char()

        while c in DIGITS:
            s = s * 10 + int(c)
            c = self._fr.read_char()

        self.chars[0] = c
        del self.chars[1:]

        return s

    def _lexical_error(self, chars: list) -> None:
        """
        Reports error message for lexical errors.
        """
        error("Line {0}: \"{1}\" is not a valid word."
              .format(self.ln, ''.join(chars).strip()), "Lexical Error")
        self._read_to_line_end()

    def _whitespace_error(self) -> None:
        """
        Reports error message for missing whitespace.
        """
        error("Line {}: Op-codes must be followed by whitespace."
              .format(self.ln), "Lexical Error")
        self._read_to_line_end()

