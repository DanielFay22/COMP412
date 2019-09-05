
from .utils import *


def tok_name(tok):
    name = ""
    if tok[TOK_ID] in [MEMOP_CAT, LOADI_CAT, ARITHOP_CAT, OUTPUT_CAT, NOP_CAT]:
        name = instructions[tok[TOK_VAL]]
    elif tok[TOK_ID] == CONSTANT_CAT:
        name = str(tok[TOK_VAL])
    elif tok[TOK_ID] == REGISTER_CAT:
        name = "r" + str(tok[TOK_VAL])
    elif tok[TOK_ID] == COMMA_CAT:
        name = ","
    elif tok[TOK_ID] == INTO_CAT:
        name = "=>"

    return name


def print_token(tok: tuple):
    print(str(tok[TOK_LN]) +
          ": < " + categories[tok[TOK_ID]] + "\t, " +
          "\"" + tok_name(tok) + "\" >"
          )

# class Token(object):
#
#     def __init__(self, id: int, ln: int, value: Union[int, None]):
#
#         self.id = id
#
#         self.val = value
#
#         self.ln = ln
#
#     def name(self):
#         return instructions[self.val]
#
#     def __repr__(self):
#         return str(self.ln) + \
#                ": < " + \
#                self.__class__.__name__ + \
#                "\t, " + \
#                "\"" + \
#                self.name() + \
#                "\" >"
#
#
#
# # def MEMOP(ln: int, value: int):
# #     return MEMOP_CAT, value, ln
#
# # Category 0
# class MEMOP(Token):
#
#     def __init__(self, ln: int, value: int):
#         super(MEMOP, self).__init__(
#             id = MEMOP_CAT, value = value, ln = ln
#         )
#
# # Category 1
# class LOADI(Token):
#
#     # Only token value is "loadI", which has value 2
#     def __init__(self, ln: int, value: int = None):
#         super(LOADI, self).__init__(
#             id = LOADI_CAT, value = LOADI_VAL, ln = ln
#         )
#
# # Category 2
# class ARITHOP(Token):
#
#     def __init__(self, ln: int, value: int):
#         super(ARITHOP, self).__init__(
#             id = ARITHOP_CAT, value = value, ln = ln
#         )
#
# # Category 3
# class OUTPUT(Token):
#
#     # Only token value is "output", which has value 8
#     def __init__(self, ln: int, value: int = None):
#         super(OUTPUT, self).__init__(
#             id = OUTPUT_CAT, value = OUTPUT_VAL, ln = ln
#         )
#
# # Category 4
# class NOP(Token):
#
#     # Only token value is "nop", which has value 9
#     def __init__(self, ln: int, value: int = None):
#         super(NOP, self).__init__(
#             id = NOP_CAT, value = NOP_VAL, ln = ln
#         )
#
# # Category 5
# class CONSTANT(Token):
#
#     def __init__(self, ln: int, value: int, ):
#         super(CONSTANT, self).__init__(
#             id = CONSTANT_CAT, value = value, ln = ln
#         )
#
#     def name(self):
#         return str(self.val)
#
# # Category 6
# class REGISTER(Token):
#
#     def __init__(self, ln: int, value: int):
#         super(REGISTER, self).__init__(
#             id = REGISTER_CAT, value = value, ln = ln
#         )
#
#     def name(self):
#         return "r" + str(self.val)
#
# # Category 7
# class COMMA(Token):
#
#     def __init__(self, ln: int, value: int = None):
#         super(COMMA, self).__init__(
#             id = COMMA_CAT, value = None, ln = ln)
#
#     def name(self):
#         return ","
#
# # Category 8
# class INTO(Token):
#
#     def __init__(self, ln: int, value: int = None):
#         super(INTO, self).__init__(
#             id = INTO_CAT, value = None, ln = ln
#         )
#
#     def name(self):
#         return "=>"
#
# # Category 9
# class ENDFILE(Token):
#
#     def __init__(self, ln: int):
#         super(ENDFILE, self).__init__(
#             id = ENDFILE_CAT, value = None, ln = ln
#         )
#
#
#     def name(self):
#         return ""