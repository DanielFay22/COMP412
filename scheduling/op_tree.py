
from resources import *
from .multi_op_ir import MultiInternalRepresentation





class OpTree(object):


    def __init__(self):
        self._heads = []

    def add_head(self, node):
        self._heads.append(node)

    @property
    def heads(self):
        return self._heads[:]


    def gen_dot_file(self):
        s = "digraph report\n{"

        s += "\n 0 [label = \"s\"];\n"

        visited = [None]
        queue = []

        i = 1
        for n in self._heads:
            s += " {0} [label = \"{1}\" ];\n".format(
                i, MultiInternalRepresentation.to_code_op(n.op)
            )
            s += f" 0 -> {0} ;\n".format(i)

            visited.append(n)

            i += 1

            queue.extend(n.children)

        while queue:
            n = queue.pop()
            visited.append(n)

            s += " {0} [label = \"{1}\" ];\n".format(
                i, MultiInternalRepresentation.to_code_op(n.op)
            )

            for p in n.parents:
                if p in visited:
                    ind = visited.index(p)

                    s += f" {0} -> {1} ;\n".format(ind, i)

            for c in n.children:
                if c in visited:
                    ind = visited.index(c)

                    s += f" {0} -> {1} ;\n".format(i, ind)
                else:
                    queue.append(c)

            i += 1

        s += "}"

        print(s)




class Node(object):

    def __init__(self, op, parents=None, children=None):

        self._op = op

        self._parents = parents if parents is not None else []
        self._children = children if children is not None else []

        self.executed = False

        self.all_parents_executed = False

        self.visited = False

        self._cp = None

    @property
    def parents(self):
        return self._parents[:]

    @property
    def children(self):
        return self._children[:]

    @property
    def num_children(self):
        return len(self._children)

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

    @property
    def critical_path(self):
        if self._cp is None:
            self._cp = self.latency()
            if self._children:
                self._cp += max([c.critical_path for c in self._children])

        return self._cp


class SerializedNode(Node):

    def __init__(self, op, parents=None, serialized_parents=None, children=None):

        super(SerializedNode, self).__init__(op, parents, children)

        self._serial_depends = serialized_parents[:]


    def can_execute(self):

        if self.all_parents_executed: return True

        for p in self.parents:
            if not p.executed:
                return False

        for s in self._serial_depends:
            if not s.visited:
                return False

        self.all_parents_executed = True

        return True
