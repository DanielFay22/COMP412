
import heapq

from core import *
from .op_tree import OpTree, Node, SerializedNode
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

        ready = [(-t.latency(), -t.critical_path, -t.num_children, hc, t) for hc, t in enumerate(tree.heads)]
        heapq.heapify(ready)    # Use a heap to automatically track the highest priority ops available.

        active = []

        hc = len(tree.heads)

        while ready or active:

            next_op1, next_op2 = None, None

            if not ready:
                self.new_ir.add_nop()

            elif len(ready) == 1:
                next_op1 = ready.pop()[-1]
                self.new_ir.add_op((next_op1.op,))

            # If multiple ops are ready, decide which ones to schedule.
            else:
                op1 = heapq.heappop(ready)[-1]
                op1_val = op1.op_val

                op2 = None
                for j in range(len(ready)):
                    op2_val = ready[j][-1].op_val

                    if op1_val == LOAD_VAL or op1_val == STORE_VAL:
                        if op2_val == LOAD_VAL or op2_val == STORE_VAL:
                            continue

                    elif op1_val == MULT_VAL:
                        if op2_val == MULT_VAL:
                            continue

                    elif op1_val == OUTPUT_VAL:
                        if op2_val == OUTPUT_VAL:
                            continue

                    op2 = ready.pop(j)[-1]
                    break

                next_op1, next_op2 = op1, op2

                if op2 is not None:
                    self.new_ir.add_op((op1.op, op2.op))
                else:
                    self.new_ir.add_op((op1.op,))


            # Add ops to the active queue.
            for next_op in [next_op1, next_op2]:
                if next_op is not None:
                    next_op.scheduled = True
                    active.append((next_op.latency() + i, next_op))


            i += 1

            # Add in children of active ops that have completed.
            # Performing this at the end prevents a single trailing nop from being added.
            j = 0
            while j < len(active):
                if i >= active[j][0]:
                    node = active.pop(j)[1]

                    node.execute()

                    for c in node.children:
                        if c.can_execute() and not c.visited:
                            heapq.heappush(ready, (-c.latency(), -c.critical_path, -c.num_children, hc, c))
                            hc += 1
                            c.visited = True

                else:
                    j += 1

        return self.new_ir


    def build_dependence_tree(self):

        tree = OpTree()

        all_nodes = [None] * (self._ir.max_reg + 1)


        last_store = None
        last_output = None

        stores = []

        all_load_out = []


        for op in self._ir.ir:
            op_val = op[IR_OP]
            if op_val == NOP_VAL:
                continue
            elif op_val == LOADI_VAL:
                node = Node(op, val=op[IR_R1])

                all_nodes[op[IR_VR3]] = node
                tree.add_head(node)

            elif op_val == LOAD_VAL:
                vr1 = op[IR_VR1]
                vr3 = op[IR_VR3]

                assert vr1 is not None
                assert vr3 is not None

                parents = [all_nodes[vr1]]

                # If memory is a known location and value store for later optimization
                val = None
                addr = None
                p1 = all_nodes[vr1]
                if p1.val is not None:
                    addr = p1.val
                    if p1.val in tree.memmap:
                        val = tree.memmap[p1.val]

                for s in range(len(stores) - 1, -1, -1):
                    if addr is not None and stores[s].addr is not None and addr != stores[s].addr:
                        continue

                    parents += [stores[s]]
                    break

                node = Node(op, parents=parents, val=val, addr=addr)

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

                if None in parents:
                    error("Undeclared register in store op at line {}".format(op[IR_LN]))
                    exit()

                val = parents[0].val
                addr = parents[1].val

                sparents = []
                if last_store is not None:
                    sparents += [last_store]
                if last_output is not None:
                    sparents += [last_output]
                sparents += all_load_out

                node = SerializedNode(op, parents=parents, serialized_parents=sparents, val=val, addr=addr)

                # If a store has no parents then it's behavior is undefined,
                # but it is technically a head node.
                if not parents and not sparents:
                    tree.add_head(node)

                for p in parents + sparents:
                    p.add_child(node)

                last_store = node
                stores.append(node)

            elif op_val == OUTPUT_VAL:

                parents = []
                sparents = []


                # Add dependency to last store which could write to address
                addr = op[IR_R1]
                for s in range(len(stores) - 1, -1, -1):
                    if stores[s].addr is not None and addr != stores[s].addr:
                        continue

                    parents += [stores[s]]
                    break

                if last_output is not None:
                    sparents = [last_output]

                node = SerializedNode(op, parents=parents, serialized_parents=sparents, addr=addr)

                for p in parents + sparents:
                    p.add_child(node)

                # If this output occured before any other output or write to memory,
                # it has no dependencies.
                if not (parents or sparents):
                    tree.add_head(node)

                last_output = node

            # All arithops have the same dependency structure.
            else:

                vr1 = op[IR_VR1]
                vr2 = op[IR_VR2]

                assert vr1 is not None
                assert vr2 is not None

                parents = [all_nodes[vr1], all_nodes[vr2]]

                opcode = op[IR_OP]
                parent_vals = [p.val for p in parents]
                val = None

                if None not in parent_vals:
                    if opcode == ADD_VAL:
                        val = sum(parent_vals)
                    elif opcode == SUB_VAL:
                        val = parent_vals[0] - parent_vals[1]
                    elif opcode == MULT_VAL:
                        val = parent_vals[0] * parent_vals[1]
                    elif opcode == RSHIFT_VAL:
                        val = parent_vals[0] >> parent_vals[1]
                    elif op == LSHIFT_VAL:
                        val = parent_vals[0] << parent_vals[1]

                node = Node(op, parents=parents, val=val)

                for p in parents:
                    p.add_child(node)

                vr3 = op[IR_VR3]

                assert vr3 is not None

                all_nodes[vr3] = node


        self._dependence_tree = tree