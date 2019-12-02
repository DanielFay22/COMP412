
from resources import *






class OpTree(object):


    def __init__(self):
        self._heads = []

    def add_head(self, node):
        self._heads.append(node)

    @property
    def heads(self):
        return self._heads[:]




class Node(object):

    def __init__(self, op, parents=None, children=None):

        self._op = op

        self._parents = parents if parents is not None else []
        self._children = children if children is not None else []

        self.executed = False

        self.all_parents_executed = False

        self.visited = False

    @property
    def parents(self):
        return self._parents[:]

    @property
    def children(self):
        return self._children[:]

    def add_child(self, node):
        self._children.append(node)

    def can_execute(self):

        if self.all_parents_executed: return True

        for p in self.parents:
            if not p.executed:
                return False

        self.all_parents_executed = True

        return True

    def latency(self):
        return LATENCIES[self._op[IR_OP]]

    @property
    def op(self):
        return self._op

    @property
    def op_val(self):
        return self._op[IR_OP]

    def execute(self):
        self.executed = True
