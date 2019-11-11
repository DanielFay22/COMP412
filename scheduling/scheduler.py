
from core import *


class Scheduler(object):

    def __init__(self, ir: InternalRepresentation):
        """

        """
        self._ir = ir
        self._new_ir = InternalRepresentation()

    @property
    def ir(self):
        return self._ir

    @property
    def new_ir(self):
        return self._new_ir

    def schedule(self):
        pass
