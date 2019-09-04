
from .scanner import Scanner
from .interal_representation import InternalRepresentation

class Parser(object):

    def __init__(self, scanner: Scanner, ir: InternalRepresentation):

        self._scanner = scanner

        self._ir = ir
