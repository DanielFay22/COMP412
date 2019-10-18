
from core import InternalRepresentation
from resources import *



class Allocator(object):



    def __init__(self, ir: InternalRepresentation, k: int):

        self.ir = ir
        self.k = k



def allocate_registers(ir: InternalRepresentation, k: int):
    """

    """

    pr_to_vr = [None] * k
    vr_to_pr = [None] * ir.max_reg
    vr_spill = vr_to_pr[:]

    for op in ir.ir:
        vr1 = op[IR_VR1]
        vr2 = op[IR_VR2]
        vr3 = op[IR_VR3]

        if vr1 is not None:
            if vr_to_pr[vr1] is not None:
                op[IR_PR1] = vr_to_pr[vr1]
            else:
                # Retrieve spilled value
                pass

        if vr2 is not None:
            if vr_to_pr[vr2] is not None:
                op[IR_PR2] = vr_to_pr[vr2]
            else:
                # Retrieve spilled value
                pass

        if vr3 is not None:
            try:
                i = pr_to_vr.index(None)

                vr_to_pr[vr3] = i
                pr_to_vr[i] = vr3
                op[IR_PR3] = i

            except ValueError:
                # Spill value
                pass

        





    pass