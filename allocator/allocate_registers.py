
from core import InternalRepresentation
from resources import *



class Allocator(object):



    def __init__(self, ir: InternalRepresentation, k: int):

        self.ir = ir
        self.k = k

        self.spill_reg = self.k - 1

        self.pr_to_vr   = [None] * (self.k - 1)
        self.vr_to_pr   = [None] * (self.ir.max_reg + 1)
        self.vr_spill   = self.vr_to_pr[:]
        self.vr_nu      = self.vr_spill[:]
        self.pr_nu = self.pr_to_vr[:]

        self.new_ir = InternalRepresentation()

        # Location for spilling memory
        self.mem_loc = 32772
        self.open_addr = []


    def allocate_registers(self):
        """

        """

        vr_to_pr    = self.vr_to_pr
        vr_nu       = self.vr_nu

        for op in self.ir.ir:
            vr1 = op[IR_VR1]
            vr2 = op[IR_VR2]
            vr3 = op[IR_VR3]

            if vr1 is not None:
                if vr_to_pr[vr1] is not None:
                    op[IR_PR1] = vr_to_pr[vr1]
                else:
                    # Retrieve spilled value
                    p = self.unspill(vr1)
                    op[IR_PR1] = p

            if vr2 is not None:
                if vr_to_pr[vr2] is not None:
                    op[IR_PR2] = vr_to_pr[vr2]
                else:
                    # Retrieve spilled value
                    p = self.unspill(vr2)

                    op[IR_PR2] = p

            if vr3 is not None:

                p = self.get_pr()
                self.assign_pr(vr3, p)

                op[IR_PR3] = p


            if vr1 is not None:
                if op[IR_NU1]:
                    vr_nu[vr1] = op[IR_NU1]
                else:
                    self.clear_vr(vr1)
            if vr2 is not None:
                if op[IR_NU2]:
                    vr_nu[vr2] = op[IR_VR2]
                else:
                    self.clear_vr(vr2)
            if vr3 is not None:
                if op[IR_NU3]:
                    vr_nu[vr3] = op[IR_NU3]
                else:
                    self.clear_vr(vr3)


            self.new_ir.add_token_copy(op)

    def clear_vr(self, vr):

        p = self.vr_to_pr[vr]

        if p:
            self.pr_to_vr[p] = None
            self.vr_to_pr[vr] = None
            if self.vr_spill[vr]:
                self.open_addr.append(self.vr_spill[vr])
                self.vr_spill[vr] = None


    def get_pr(self):
        """

        """

        if None in self.pr_to_vr:
            return self.pr_to_vr.index(None)

        else:
            return self.spill()

    def spill(self):
        """

        """
        # If some value
        clean_vrs = [vr for vr in self.pr_to_vr if vr is not None and self.vr_spill[vr] is not None]
        if clean_vrs:
            vr = max(clean_vrs, key=lambda v: self.vr_nu[v])
            pr = self.vr_to_pr[vr]
            self.vr_to_pr[vr] = None
            self.pr_to_vr[pr] = None
            return pr

        mu, nu = 0, -1
        for i, n in enumerate(self.pr_nu):
            if n is not None and  n > nu:
                mu, nu = i, n
        pr = mu#self.pr_nu.index(max(self.pr_nu))

        if not self.open_addr:
            m = self.mem_loc
            self.mem_loc += 1

        else:
            m = self.open_addr.pop()


        vr = self.pr_to_vr[pr]

        self.new_ir.add_full_token(
            op=LOADI_VAL,
            r1=m, vr1=m, pr1=m,
            r3=self.ir.max_reg + 1, vr3=self.ir.max_reg + 1, pr3=self.spill_reg
        )

        self.new_ir.add_full_token(
            op=STORE_VAL,
            r1=self.ir.max_reg + 1, vr1=vr, pr1=pr,
            r2=self.ir.max_reg + 1, vr2=self.ir.max_reg + 1, pr2=self.spill_reg
        )

        self.vr_to_pr[vr] = None
        self.pr_to_vr[pr] = None
        self.vr_spill[vr] = m

        return pr

    def unspill(self, vr):
        """

        """
        pr = self.get_pr()

        # Get address of spilled value
        self.new_ir.add_full_token(
            op=LOADI_VAL,
            r1=self.vr_spill[vr], vr1=self.vr_spill[vr], pr1=self.vr_spill[vr],
            r3=self.spill_reg, vr3=self.ir.max_reg + 1, pr3=self.spill_reg
        )

        self.new_ir.add_full_token(
            op=LOAD_VAL,
            r1=self.ir.max_reg + 1, vr1=self.ir.max_reg + 1, pr1=self.spill_reg,
            r3=self.ir.max_reg + 1, vr3=self.ir.max_reg + 1, pr3=pr
        )

        self.assign_pr(vr, pr)

        return pr


    def assign_pr(self, vr, pr):

        self.vr_to_pr[vr] = pr
        self.pr_to_vr[pr] = vr




