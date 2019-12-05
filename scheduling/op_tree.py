
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

    def get_leaves(self):
        """
        Finds the leaves by traversing the tree.
        """

        nodes = self._heads[:]
        leaves = []

        visited = set(nodes)

        while nodes:
            n = nodes.pop()

            if n.all_children:
                unvisited = [c for c in n.all_children if c not in visited]
                nodes.extend(unvisited)
                visited.update(unvisited)

            else:
                leaves.append(n)

        return leaves

    def calc_critical_paths(self):
        """
        One time calculation to find the critical path for every node.
        """
        visited = set([])
        nodes = set(self.get_leaves())

        while nodes:
            n = nodes.pop()
            n.update_critical_path(n.latency())
            visited.add(n)
            cp = n.critical_path

            for p in n.parents:
                p.update_critical_path(cp + p.latency())
                # if p not in visited:
                nodes.add(p)
                    # visited.add(p)

            for d in n.serial_parents:
                d.update_critical_path(cp + 1)
                # if d not in visited:
                nodes.add(d)
                    # visited.add(d)




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

        self._serial_children = []

    def __str__(self):
        return MultiInternalRepresentation.to_code_op(self._op)

    @property
    def parents(self):
        return self._parents[:]

    @property
    def children(self):
        return self._children[:]

    @property
    def all_children(self):
        return self._children + self._serial_children

    @property
    def serial_children(self):
        return self._serial_children[:]

    @property
    def serial_parents(self):
        return []

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

    def add_serial_child(self, n):
        self._serial_children.append(n)

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
        # if self._cp is None:
        #     self._cp = self.latency()
        #     if self._children:
        #         self._cp += max([c.critical_path for c in self._children])
        #
        #     self._cp = max(self._cp, 1 + max([0] + [n.critical_path for n in self._serial_children]))

        return self._cp

    def update_critical_path(self, c):
        if self._cp is None:
            self._cp = c
        else:
            self._cp = max(self._cp, c)




class SerializedNode(Node):

    def __init__(self, op, parents=None, serialized_parents=None, children=None, val=None, addr=None):

        super(SerializedNode, self).__init__(op, parents, children, val, addr)

        self._serial_depends = [p for p in serialized_parents if p not in parents]

        for n in self._serial_depends:
            n.add_serial_child(self)


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

    @property
    def serial_parents(self):
        return self._serial_depends[:]
