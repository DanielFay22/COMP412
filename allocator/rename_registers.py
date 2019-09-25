

from core import InternalRepresentation
from resources import *




def rename_registers(ir: InternalRepresentation):
    """
    Pass through the internal representation, renaming registers
    such that each register is defined only once.
    """

    cur_reg = 0
    reg_map = [None] * ir.max_reg

    # Stores the location of the first and last uses of each VR.
    active = []

    op = ir.head

    while op:

        # Check register def
        if op[IR_R3] is not None:
            try:
                op[IR_VR3] = reg_map[op[IR_R3]]
                active[op[IR_VR3]][0] = op[IR_LN]

                reg_map.pop(op[IR_R3])

            except KeyError:
                reg_map[op[IR_R3]] = cur_reg
                op[IR_VR3] = cur_reg

                cur_reg += 1
                active.append([op[IR_LN], op[IR_LN]])

        # Check register uses
        if op[IR_R1] is not None:
            if not (op[IR_OP] == LOADI_VAL or op[IR_OP] == OUTPUT_VAL):
                try:
                    op[IR_VR1] = reg_map[op[IR_R1]]
                except KeyError:
                    reg_map[op[IR_R1]] = cur_reg
                    op[IR_VR1] = cur_reg

                    cur_reg += 1
                    active.append([0, op[IR_LN]])


        if op[IR_R2] is not None:
            try:
                op[IR_VR2] = reg_map[op[IR_R2]]
            except KeyError:
                reg_map[op[IR_R2]] = cur_reg
                op[IR_VR2] = cur_reg

                cur_reg += 1
                active.append([0, op[IR_LN]])

        # Get next operation
        op = op[IR_PREV]

    ir.max_reg = cur_reg - 1
    ir.active = active
