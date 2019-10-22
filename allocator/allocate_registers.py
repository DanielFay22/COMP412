
from core import InternalRepresentation
from resources import *



class Allocator(object):



    def __init__(self, ir: InternalRepresentation, k: int):

        self.ir = ir
        self.k = k

        self.spill_reg = self.k - 1

        self.pr_to_vr   = [None] * (self.k - 1)
        self.vr_to_pr   = [None] * self.ir.max_reg
        self.vr_spill   = self.vr_to_pr[:]
        self.vr_nu      = self.vr_spill[:]


    def allocate_registers(self):
        """

        """

        pr_to_vr    = self.pr_to_vr
        vr_to_pr    = self.vr_to_pr
        vr_spill    = self.vr_spill
        vr_nu       = self.vr_nu

        new_ir = InternalRepresentation()

        for op in self.ir.ir:
            vr1 = op[IR_VR1]
            vr2 = op[IR_VR2]
            vr3 = op[IR_VR3]

            if vr1 is not None:
                if vr_to_pr[vr1] is not None:
                    op[IR_PR1] = vr_to_pr[vr1]
                else:
                    # Retrieve spilled value
                    new_ir.add_full_token(
                        op=LOADI_VAL,
                        r1=0, vr1=vr1, pr1=
                    )

                    # if vr_spill[vr1][0] == CONSTANT:
                    #     new_ir.append(
                    #         [LOADI_VAL, ]
                    #     )
                    # else:


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
                    i = vr_nu.index(max(vr_nu))

                    new_ir.append([
                        STORE_VAL,

                    ])








        pass


    def get_pr(self):
        """

        """


