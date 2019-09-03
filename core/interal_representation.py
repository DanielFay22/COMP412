


class InternalRepresentation(object):

    def __init__(self, init_size: int = 1000):
        self._ir = self._gen_empty_ir(init_size)

        self._head = self._ir

    @staticmethod
    def _gen_empty_ir(n: int = 1000) -> list:
        """
        Generates an empty internal representation
        """
        l = [[None] * 15 for _ in range(n)]

        for x in range(n - 1):
            l[x][-2] = l[x + 1]
            l[x + 1][-1] = l[x]

        return l[0]

    def _expand_ir(self) -> None:
        ir = self._gen_empty_ir()

        self._head[-2] = ir
        ir[-1] = self._head

    def add_token(self, op: int, r1: int, r2: int, r3: int) -> None:
        """
        Enters a new operation to the current IR and increments the head.
        """
        self._head[0] = op
        self._head[1] = r1
        self._head[5] = r2
        self._head[9] = r3

        if self._head[-2] is None:
            self._expand_ir()

        self._head = self._head[-2]
