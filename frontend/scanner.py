
from typing import Union, List

from resources import *
from .reader import FileReader


class Scanner(object):

    chars = []
    
    def __init__(self, fr: FileReader):

        self._fr = fr

        self.ln = 1

    def get_token(self) -> Token:
        """
        Reads the file and returns the next token.

        If there is an error during reading, reports the error and returns an Error token.
        """

        if not self.chars:
            c = self._fr.read_char()
            self.chars.append(c)
        else:
            c = self.chars[-1]

        # load, loadI, lshift
        if c == 'l':
            r = self._scan_l()

            if r: return r

        # store, sub
        elif c == 's':
            r = self._scan_s()

            if r: return r

        # add
        elif c == 'a':
            if self._read_remaining_token("dd"):
                return ARITHOP(value = ADD_VAL, ln = self.ln)

        # mult
        elif c == 'm':
            if self._read_remaining_token("ult"):
                return ARITHOP(value = MULT_VAL, ln = self.ln)

        # rshift, register
        elif c == 'r':
            r = self._scan_r()

            if r: return r

        # output
        elif c == 'o':

            if self._read_remaining_token("utput"):
                return OUTPUT(ln = self.ln)

        # nop
        elif c == 'n':
            if self._read_remaining_token("op", whitespace=False):
                return NOP(ln = self.ln)

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
            if self._read_remaining_token('>', whitespace=False):
                return INTO(ln = self.ln)

        # newline
        elif c == '\n' or c == '\r':
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
                self._lexical_error(self.chars + [c2])

        # whitespace
        elif c == ' ' or c == '\t':
            self.chars = []
            return self.get_token()

        else:
            if not c:  # EOF
                return ENDFILE(ln = self.ln)
            else:  # Error
                self._lexical_error(self.chars)

        self.chars *= 0

    def _scan_l(self) -> Union[Token, None]:
        """
        Handler for scanning tokens beginning with 'l'.
        """
        c2 = self._fr.read_char()
        self.chars.append(c2)

        if c2 == 'o':  # load
            if self._read_remaining_token("ad", whitespace=False):
                f = self._read_remaining_token("I", verbose=False)

                if f:
                    return LOADI(ln=self.ln)
                elif (not f) and (self.chars[-1] == ' ' or self.chars[-1] == '\t'):
                    self.chars = []
                    return MEMOP(ln=self.ln, value=LOAD_VAL)
                else:
                    self._whitespace_error()

        elif c2 == 's':  # lshift
            if self._read_remaining_token("hift"):
                return ARITHOP(value=LSHIFT_VAL, ln=self.ln)

        else:
            self._lexical_error(self.chars)

    def _scan_s(self) -> Union[Token, None]:
        """
        Handler for scanning tokens beginning with 's'.
        """
        c2 = self._fr.read_char()
        self.chars.append(c2)

        # store
        if c2 == 't':
            if self._read_remaining_token("ore"):
                return MEMOP(ln=self.ln, value=STORE_VAL)

        # sub
        elif c2 == 'u':
            if self._read_remaining_token("b"):
                return ARITHOP(ln=self.ln, value=SUB_VAL)

        # error
        else:
            self._lexical_error(self.chars)

    def _scan_r(self) -> Union[Token, None]:
        """
        Handler for scanning tokens beginning with 'r'.
        """
        c2 = self._fr.read_char()
        self.chars.append(c2)

        if c2 == "s":
            if self._read_remaining_token("hift"):
                return ARITHOP(value=RSHIFT_VAL, ln=self.ln)

        elif c2.isnumeric():
            return REGISTER(
                value=self._read_constant(first_digit=int(c2)), ln=self.ln
            )
        else:
            self._lexical_error(self.chars)

    def _read_to_line_end(self):
        """
        Reads characters until it encounters the end of the line.
        """
        c = self._fr.read_char()
        while c and c != '\n' and c != '\r':
            c = self._fr.read_char()
        self.ln += 1

    def _read_remaining_token(self, expected: str, whitespace: bool = True, verbose: bool = True) -> bool:
        """
        Reads the next n characters (where n is the length of expected) and
        returns True iff the characters match the expected.

        If whitespace is True, checks that the character following the token is a whitespace character.
        """
        for e in expected:
            self.chars.append(self._fr.read_char())
            if self.chars[-1] != e:
                if verbose:
                    self._lexical_error(self.chars)
                return False

        # If the character is not whitespace, report the error.
        # Then clear all but the last character from the buffer
        # and return True.
        if whitespace:
            self.chars.append(self._fr.read_char())
            if not (self.chars[-1] == ' ' or self.chars[-1] == '\t'):
                if verbose:
                    self._whitespace_error()

                # clear all but the last character
                del self.chars[:-1]
                return True

        self.chars *= 0
        return True

    def _read_constant(self, first_digit: int) -> int:

        s = first_digit
        self.chars.append(self._fr.read_char())

        while self.chars[-1].isnumeric():
            s = s * 10 + int(self.chars[-1])
            self.chars.append(self._fr.read_char())

        del self.chars[:-1]

        return s

    def _lexical_error(self, chars: List[str]) -> None:
        """
        Reports error message for lexical errors.
        """
        error(f"Line {self.ln}: {''.join(chars).strip()} is not a valid word.", "Lexical Error")
        # self._read_to_line_end()

    def _whitespace_error(self) -> None:
        """
        Reports error message for missing whitespace.
        """
        error(f"{self.ln}: Op-codes must be followed by whitespace.", "Lexical Error")
        # self._read_to_line_end()

