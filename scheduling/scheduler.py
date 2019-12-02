
from collections import deque

from core import *
from .op_tree import OpTree, Node
from .multi_op_ir import MultiInternalRepresentation
from resources import *


class Scheduler(object):

    def __init__(self, ir: InternalRepresentation):
        """

        """
        self._ir = ir
        self._new_ir = MultiInternalRepresentation()

        self._dependence_tree = None

    @property
    def ir(self):
        return self._ir

    @property
    def new_ir(self):
        return self._new_ir

    def schedule(self):

        if self._dependence_tree is None:
            self.build_dependence_tree()

        tree = self._dependence_tree

        i = 0

        ready = tree.heads
        active = []


        while ready or active:


            j = 0
            while j < len(active):
                if i >= active[j][0]:
                    node = active.pop(j)[1]

                    ready.extend([
                        c for c in node.children if c.can_execute()
                    ])

                else:
                    j += 1

            next_op1, next_op2 = None, None

            if not ready:
                self.new_ir.add_nop()

            elif len(ready) == 1:
                next_op1 = ready.pop()
                next_op1.execute()
                self.new_ir.add_op((next_op1.op,))

            else:
                ready.sort(key=lambda o: (o.latency(), len(o.children)), reverse=True)

                op1 = ready.pop(0)
                op1_val = op1.op_val


                for j in range(len(ready)):
                    op2_val = ready[j].op_val

                    if op1_val == LOAD_VAL or op1_val == STORE_VAL:
                        if op2_val == LOAD_VAL or op2_val == STORE_VAL:
                            continue

                    elif op1_val == MULT_VAL:
                        if op2_val == MULT_VAL:
                            continue

                    elif op1_val == OUTPUT_VAL:
                        if op2_val == OUTPUT_VAL:
                            continue

                    break

                if j < len(ready):
                    op2 = ready.pop(j)
                else:
                    op2 = None

                next_op1, next_op2 = op1, op2


                op1.execute()
                if op2 is not None:
                    op2.execute()
                    self.new_ir.add_op((op1.op, op2.op))
                else:
                    self.new_ir.add_op((op1.op,))


            for next_op in [next_op1, next_op2]:

                if next_op is not None:

                    active.append((next_op.latency() + i, next_op))

                    # for c in next_op.children:
                    #     if not c.visited:
                    #         if c.can_execute(i):
                    #             ready.append(c)
                    #             c.visited = True
                    #         elif c.all_parents_executed:
                    #             available.append(c)
                    #             c.visited = True
            i += 1

        return self.new_ir


    def build_dependence_tree(self):

        tree = OpTree()

        all_nodes = [None] * (self._ir.max_reg + 1)


        last_store = None
        last_output = None

        all_load_out = []


        for op in self._ir.ir:
            op_val = op[IR_OP]
            if op_val == NOP_VAL:
                continue
            elif op_val == LOADI_VAL:
                node = Node(op)

                all_nodes[op[IR_VR3]] = node
                tree.add_head(node)

            elif op_val == LOAD_VAL:
                vr1 = op[IR_VR1]
                vr3 = op[IR_VR3]

                assert vr1 is not None
                assert vr3 is not None

                parents = [all_nodes[vr1]]

                if last_store is not None:
                    parents += [last_store]

                node = Node(op, parents=parents)

                for p in parents:
                    p.add_child(node)

                all_nodes[vr3] = node

                all_load_out.append(node)

            elif op_val == STORE_VAL:
                vr1 = op[IR_VR1]
                vr2 = op[IR_VR2]

                assert vr1 is not None
                assert vr2 is not None

                parents = [all_nodes[vr1], all_nodes[vr2]]

                if last_store is not None:
                    parents += [last_store]
                parents += all_load_out

                node = Node(op, parents=parents)

                for p in parents:
                    p.add_child(node)

                last_store = node

            elif op_val == OUTPUT_VAL:

                parents = []

                if last_store is not None:
                    parents += [last_store]
                if last_output is not None:
                    parents += [last_output]

                node = Node(op, parents=parents)

                for p in parents:
                    p.add_child(node)

                # If this output occured before any other output or write to memory,
                # it has no dependencies.
                if not parents:
                    tree.add_head(node)

                last_output = node

            # All arithops have the same dependency structure.
            else:

                vr1 = op[IR_VR1]
                vr2 = op[IR_VR2]

                assert vr1 is not None
                assert vr2 is not None

                parents = [all_nodes[vr1], all_nodes[vr2]]
                node = Node(op, parents=parents)

                for p in parents:
                    p.add_child(node)

                vr3 = op[IR_VR3]

                assert vr3 is not None

                all_nodes[vr3] = node


        self._dependence_tree = tree