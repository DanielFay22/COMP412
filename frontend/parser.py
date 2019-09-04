
from .scanner import Scanner
from .interal_representation import InternalRepresentation

from resources import *

class Parser(object):

    def __init__(self, scanner: Scanner, ir: InternalRepresentation):

        self._scanner = scanner

        self._ir = ir

        self.errors = 0


    def parse(self):

        while True:

            tok = self._scanner.get_token()

            if tok.id == MEMOP_CAT:
                pass
            elif tok.id == LOADI_CAT:
                self._parse_loadi(tok)
            elif tok.id == ARITHOP_CAT:
                self._parse_arithop(tok)
            elif tok.id == OUTPUT_CAT:
                self._parse_output(tok)
            elif tok.id == NOP_CAT:
                pass
            elif tok.id == ENDFILE_CAT:
                break
            else:   # register, comma, and constant are all invalid tokens
                pass

    def _parse_memop(self, tok):
        pass

    def _parse_loadi(self, tok: Token):
        """
        A loadI command must be followed by a constant, into, and then register.
        """
        tokens, t = self._load_tokens([CONSTANT_CAT, INTO_CAT, REGISTER_CAT])

        # correct grammar, build IR
        if t:
            self._ir.add_token(tok.val, tokens[0].val, None, tokens[2].val)
        # error, report error and continue
        else:
            self.errors += 1

            if len(tokens) == 1:
                self._report_error(f"Missing constant in loadI in line {tok.ln}.")
            elif len(tokens) == 2:
                self._report_error(f"Missing \"=>\" in loadI in line {tok.ln}.")
            elif len(tokens) == 3:
                self._report_error(f"Missing target register in loadI in line {tok.ln}.")
            else:
                # this should never happen
                assert False

    def _parse_arithop(self, tok: Token):
        """
        ARITHOP's (add, sub, mult, rshift, lshift) must have
        two source registers and one target register.

        ARITHOP REG1, REG2 => REG3
        """

        tokens, t = self._load_tokens([REGISTER_CAT, COMMA_CAT, REGISTER_CAT, INTO_CAT, REGISTER_CAT])

        if t:
            self._ir.add_token(tok.val, tokens[0].val, tokens[1].val, tokens[2].val)
        else:
            self.errors += 1
            self._report_error(f"Encountered error parsing {tok.name()} on line {tok.ln}.")
            # if len(tokens)

    def _parse_output(self, tok):
        pass

    def _parse_nop(self, tok):
        """
        nop's have no required parameters.
        """
        self._ir.add_token(NOP_VAL, None, None, None)

    def _load_tokens(self, expected: list):

        tokens = []

        for i in expected:
            tokens.append(self._scanner.get_token())

            if tokens[-1].id != i:
                # error
                pass

        return tokens, True

    def _report_error(self, msg: str):