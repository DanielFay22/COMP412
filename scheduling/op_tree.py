
from resources import *
from .multi_op_ir import MultiInternalRepresentation





class OpTree(object):


    def __init__(self):
        self._heads = []
        self.memmap = {}

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
            s += " 0 -> {0} ;\n".format(i)

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

                    s += " {0} -> {1} ;\n".format(ind, i)

            for c in n.children:
                if c in visited:
                    ind = visited.index(c)

                    s += " {0} -> {1} ;\n".format(i, ind)
                else:
                    queue.append(c)

            i += 1

        s += "}"

        print(s)




class Node(object):

    def __init__(self, op, parents=None, children=None, val=None, addr=None):

        self._op = op

        self._parents = parents if parents is not None else []
        self._children = children if children is not None else []

        self.all_parents_executed = False

        self.visited = False
        self.executed = False
        self.scheduled = False

        self._cp = None

        self._val = val
        self._addr = addr

    @property
    def parents(self):
        return self._parents[:]

    @property
    def children(self):
        return self._children[:]

    @property
    def num_children(self):
        return len(self._children)

    @property
    def val(self):
        return self._val

    @property
    def addr(self):
        return self._addr

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

    def calculate_val(self):
        op = self._op[IR_OP]

        parent_vals = [p.val for p in self.parents]

        if op == LOADI_VAL:
            self._val = self._op[IR_R1]
            return

        elif op in [ADD_VAL, SUB_VAL, MULT_VAL, RSHIFT_VAL, LSHIFT_VAL]:
            if None in parent_vals or len(parent_vals) != 2:
                return

            if op == ADD_VAL:
                self._val = sum(parent_vals)
            elif op == SUB_VAL:
                pass    # Need to figure out how to order these
            elif op == MULT_VAL:
                self._val = parent_vals[0] * parent_vals[1]
            elif op == RSHIFT_VAL:
                pass
            elif op == LSHIFT_VAL:
                pass

            return

        elif op == LOAD_VAL:
            if len(self._parents) != 1:
                return

            self._addr = self._parents[0].val

        elif op == STORE_VAL:
            pass



class SerializedNode(Node):

    def __init__(self, op, parents=None, serialized_parents=None, children=None, val=None, addr=None):

        super(SerializedNode, self).__init__(op, parents, children, val, addr)

        self._serial_depends = serialized_parents[:]


    def can_execute(self):

        if self.all_parents_executed: return True

        for p in self.parents:
            if not p.executed:
                return False

        for s in self._serial_depends:
            if not s.scheduled:
                return False

        self.all_parents_executed = True

        return True
