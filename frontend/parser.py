
from .scanner import Scanner
from .interal_representation import InternalRepresentation

from resources import *

class Parser(object):

    def __init__(self, scanner: Scanner, ir: InternalRepresentation):

        self._scanner = scanner

        self._ir = ir

        self.errors = 0

        self._next_token = None

    @property
    def ln(self):
        return self._scanner.ln

    @property
    def count(self):
        return self._ir.count


    def parse(self):

        while True:
            if self._next_token:
                tok = self._next_token
                self._next_token = None
            else:
                tok = self._scanner.get_token()

            if not tok:
                continue

            if tok[TOK_ID] == MEMOP_CAT:
                self._parse_memop(tok)
            elif tok[TOK_ID] == LOADI_CAT:
                self._parse_loadi(tok)
            elif tok[TOK_ID] == ARITHOP_CAT:
                self._parse_arithop(tok)
            elif tok[TOK_ID] == OUTPUT_CAT:
                self._parse_output(tok)
            elif tok[TOK_ID] == NOP_CAT:
                self._parse_nop(tok)
            elif tok[TOK_ID] == ENDFILE_CAT:
                break
            else:   # register, comma, and constant are all invalid tokens
                error("Line {0}: Operation starts with invalid opcode: '{1}'."
                      .format(tok[TOK_LN], tok_name(tok)))
                # self._next_line()
                self.errors += 1

    def _parse_memop(self, tok):
        """

        """
        tokens, t = self._load_tokens([REGISTER_CAT, INTO_CAT, REGISTER_CAT])

        if t:
            self._ir.add_token(tok[TOK_VAL], tokens[0][TOK_VAL], None, tokens[2][TOK_VAL])

        else:
            self.errors += 1
            self._report_error("Encountered error parsing {0} on line {1}."
                               .format(tok_name(tok),tok[TOK_LN]))

    def _parse_loadi(self, tok):
        """
        A loadI command must be followed by a constant, into, and then register.
        """
        tokens, t = self._load_tokens([CONSTANT_CAT, INTO_CAT, REGISTER_CAT])

        # correct grammar, build IR
        if t:
            self._ir.add_token(tok[TOK_VAL], tokens[0][TOK_VAL], None, tokens[2][TOK_VAL])
        # error, report error and continue
        else:
            self.errors += 1

            if len(tokens) == 1:
                self._report_error("Missing constant in loadI in line {}.".format(tok[TOK_LN]))
            elif len(tokens) == 2:
                self._report_error("Missing \"=>\" in loadI in line {}.".format(tok[TOK_LN]))
            elif len(tokens) == 3:
                self._report_error("Missing target register in loadI in line {}.".format(tok[TOK_LN]))
            else:
                # this should never happen
                assert False

    def _parse_arithop(self, tok):
        """
        ARITHOP's (add, sub, mult, rshift, lshift) must have
        two source registers and one target register.

        ARITHOP REG1, REG2 => REG3
        """

        tokens, t = self._load_tokens([REGISTER_CAT, COMMA_CAT, REGISTER_CAT, INTO_CAT, REGISTER_CAT])

        if t:
            self._ir.add_token(tok[TOK_VAL], tokens[0][TOK_VAL], tokens[2][TOK_VAL], tokens[4][TOK_VAL])
        else:
            self.errors += 1
            self._report_error("Encountered error parsing {0} on line {1}."
                               .format(tok_name(tok), tok[TOK_LN]))
            # if len(tokens)

    def _parse_output(self, tok):
        tokens, t = self._load_tokens([CONSTANT_CAT])

        if t:
            self._ir.add_token(tok[TOK_VAL], tokens[0][TOK_VAL], None, None)

        else:
            self.errors += 1
            self._report_error("Encountered error parsing {0} on line {1}.".format(tok_name(tok), tok[TOK_LN]))

    def _parse_nop(self, tok):
        """
        nop's have no required parameters.
        """
        self._ir.add_token(tok[TOK_VAL], None, None, None)

    def _load_tokens(self, expected: list):

        tokens = [None] * len(expected)

        gt = self._scanner.get_token

        for i, e in enumerate(expected):
            tokens[i] = gt()

            if not tokens[i] or tokens[i][TOK_ID] != e:
                self._next_token = tokens[i]
                return tokens[:i + 1], False

        return tokens, True

    @staticmethod
    def _report_error(msg: str):
        """

        """
        error(msg)


    def print_ir(self):
        self._ir.print_ir()

    def _next_line(self):

        if self._next_token:
            tok = self._next_token
        else:
            return

        t2 = self._scanner.get_token()

        while t2[TOK_LN] == tok[TOK_LN]:
            tok = t2
            t2 = self._scanner.get_token()

        self._next_token = t2