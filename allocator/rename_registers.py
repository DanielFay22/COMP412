

from core import InternalRepresentation
from resources import *




def rename_registers(ir: InternalRepresentation):
    """
    Pass through the internal representation, renaming registers
    such that each register is defined only once.
    """

    cur_reg = 0
    sr_to_vr = [None] * (ir.max_reg + 1)
    lu = sr_to_vr[:]

    for i in range(len(ir.ir) - 1, -1, -1):
        op = ir.ir[i]

        # Check register def
        if op[IR_R3] is not None:
            if sr_to_vr[op[IR_R3]] is None:
                sr_to_vr[op[IR_R3]] = cur_reg
                cur_reg += 1

            op[IR_VR3] = sr_to_vr[op[IR_R3]]
            op[IR_NU3] = lu[op[IR_R3]]

            sr_to_vr[op[IR_R3]] = None
            lu[op[IR_R3]] = None

        # Check register uses
        if op[IR_R1] is not None:
            if not (op[IR_OP] == LOADI_VAL or op[IR_OP] == OUTPUT_VAL):
                if sr_to_vr[op[IR_R1]] is None:
                    sr_to_vr[op[IR_R1]] = cur_reg
                    cur_reg += 1

                op[IR_VR1] = sr_to_vr[op[IR_R1]]
                op[IR_NU1] = lu[op[IR_R1]]
                lu[op[IR_R1]] = op[IR_LN]

        if op[IR_R2] is not None:

            if sr_to_vr[op[IR_R2]] is None:
                sr_to_vr[op[IR_R2]] = cur_reg
                cur_reg += 1

            op[IR_VR2] = sr_to_vr[op[IR_R2]]
            op[IR_NU2] = lu[op[IR_R2]]
            lu[op[IR_R2]] = op[IR_LN]


    ir.max_reg = cur_reg - 1

    undefined = [(i, j) for i, j in enumerate(lu) if j is not None]
    if undefined:
        for i, j in sorted(undefined, key=lambda x: x[1]):
            error(
                "Register \"r{}\" is used before it is defined on line {}.".format(
                    i, j
                ),
                "Undefined Register"
            )
