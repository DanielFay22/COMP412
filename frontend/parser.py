
from .scanner import Scanner
from .interal_representation import InternalRepresentation

from resources import *

class Parser(object):

    def __init__(self, scanner: Scanner, ir: InternalRepresentation):

        self._scanner = scanner

        self._ir = ir

        self.errors = 0

        self.token_queue = []

    @property
    def ln(self):
        return self._scanner.ln

    @property
    def count(self):
        return self._ir.count


    def parse(self):

        while True:
            if self.token_queue:
                tok = self.token_queue.pop(0)
            else:
                tok = self._scanner.get_token()

            if not tok:
                continue

            if tok.id == MEMOP_CAT:
                self._parse_memop(tok)
            elif tok.id == LOADI_CAT:
                self._parse_loadi(tok)
            elif tok.id == ARITHOP_CAT:
                self._parse_arithop(tok)
            elif tok.id == OUTPUT_CAT:
                self._parse_output(tok)
            elif tok.id == NOP_CAT:
                self._parse_nop(tok)
            elif tok.id == ENDFILE_CAT:
                break
            else:   # register, comma, and constant are all invalid tokens
                error(f"Line {self._scanner.ln}: Operation starts with invalid opcode: '{tok.name()}'.")
                self.errors += 1

    def _parse_memop(self, tok):
        """

        """
        tokens, t = self._load_tokens([REGISTER_CAT, INTO_CAT, REGISTER_CAT])

        if t:
            self._ir.add_token(tok.val, tokens[0].val, None, tokens[2].val)

        else:
            self.errors += 1
            self._report_error(f"Encountered error parsing {tok.name()} on line {tok.ln}.")

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
            self._ir.add_token(tok.val, tokens[0].val, tokens[2].val, tokens[4].val)
        else:
            self.errors += 1
            self._report_error(f"Encountered error parsing {tok.name()} on line {tok.ln}.")
            # if len(tokens)

    def _parse_output(self, tok):
        tokens, t = self._load_tokens([CONSTANT_CAT])

        if t:
            self._ir.add_token(tok.val, tokens[0].val, None, None)

        else:
            self.errors += 1
            self._report_error(f"Encountered error parsing {tok.name()} on line {tok.ln}.")

    def _parse_nop(self, tok):
        """
        nop's have no required parameters.
        """
        self._ir.add_token(tok.val, None, None, None)

    def _load_tokens(self, expected: list):

        tokens = []

        for i in expected:
            tokens.append(self._scanner.get_token())

            if not tokens[-1] or tokens[-1].id != i:
                self.token_queue.append(tokens[-1])
                return tokens, False

        return tokens, True

    def _report_error(self, msg: str):
        """

        """
        error(msg)


    def print_ir(self):
        self._ir.print_ir()