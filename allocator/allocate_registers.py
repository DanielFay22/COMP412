
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
        self.pr_nu      = self.pr_to_vr[:]

        self.new_ir = InternalRepresentation()

        # Location for spilling memory
        self.mem_loc = 32772
        self.open_addr = []

        self.reserved_vr = None


    def allocate_registers(self):
        """

        """

        vr_to_pr    = self.vr_to_pr
        vr_nu       = self.vr_nu

        for op in self.ir.ir:
            vr1 = op[IR_VR1]
            vr2 = op[IR_VR2]
            vr3 = op[IR_VR3]

            # Store LOADI values for rematerialization later.
            if op[IR_OP] == LOADI_VAL:
                self.vr_spill[vr3] = (CONSTANT, op[IR_R1])

            # Unused declaration.
            if vr3 is not None and op[IR_NU3] is None:
                if vr1 is not None:
                    if op[IR_NU1] is not None:
                        vr_nu[vr1] = op[IR_NU1]
                    else:
                        self.clear_vr(vr1)
                if vr2 is not None:
                    if op[IR_NU2] is not None:
                        vr_nu[vr2] = op[IR_NU2]
                    else:
                        self.clear_vr(vr2)
                continue

            if vr1 is not None:
                if vr_to_pr[vr1] is not None:
                    op[IR_PR1] = vr_to_pr[vr1]
                else:
                    # Retrieve spilled value
                    self.reserved_vr = vr2
                    p = self.unspill(vr1)
                    op[IR_PR1] = p

            if vr2 is not None:
                if vr_to_pr[vr2] is not None:
                    op[IR_PR2] = vr_to_pr[vr2]
                else:
                    # Retrieve spilled value
                    self.reserved_vr = vr1
                    p = self.unspill(vr2)
                    op[IR_PR2] = p

            self.reserved_vr = None

            # Update next use and clear regs if necessary. Clearing before
            # handling r3 allows for reuse of the same registers within an expression.
            if vr1 is not None:
                if op[IR_NU1] is not None:
                    vr_nu[vr1] = op[IR_NU1]
                else:
                    self.clear_vr(vr1)
            if vr2 is not None:
                if op[IR_NU2] is not None:
                    vr_nu[vr2] = op[IR_NU2]
                else:
                    self.clear_vr(vr2)


            # vr3 corresponds to new declaration, so always needs new pr
            if vr3 is not None:
                p = self.get_pr()
                self.assign_pr(vr3, p)

                op[IR_PR3] = p

            # Update next use of vr3
            if vr3 is not None:
                if op[IR_NU3] is not None:
                    vr_nu[vr3] = op[IR_NU3]
                else:
                    self.clear_vr(vr3)


            self.new_ir.add_token_copy(op)

    def clear_vr(self, vr):

        p = self.vr_to_pr[vr]

        if p is not None:
            self.pr_to_vr[p] = None
            self.vr_to_pr[vr] = None
            if self.vr_spill[vr]:
                if self.vr_spill[vr][0] == ADDRESS:
                    self.open_addr.append(self.vr_spill[vr][1])
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
        for p, vr in enumerate(self.pr_to_vr):
            if self.vr_nu[vr] is None:
                self.clear_vr(vr)
                return p

        # If some value is already stored somewhere, you don't need to store it again.
        clean_vrs = [
            vr for vr in self.pr_to_vr
            if self.vr_spill[vr] is not None and vr != self.reserved_vr
        ]
        if clean_vrs:
            vr = max(clean_vrs, key=lambda v: self.vr_nu[v])
            pr = self.vr_to_pr[vr]
            self.vr_to_pr[vr] = None
            self.pr_to_vr[pr] = None
            return pr

        pr = self.pr_to_vr.index(
            max(self.pr_to_vr, key=lambda v: self.vr_nu[v] * int(v != self.reserved_vr))
        )

        if not self.open_addr:
            m = self.mem_loc
            self.mem_loc += 4

        else:
            m = self.open_addr.pop()


        vr = self.pr_to_vr[pr]

        self.new_ir.add_full_token(
            op=LOADI_VAL,
            r1=-2, vr1=vr, pr1=m,
            r3=self.ir.max_reg + 1, vr3=self.ir.max_reg + 1, pr3=self.spill_reg
        )

        self.new_ir.add_full_token(
            op=STORE_VAL,
            r1=self.ir.max_reg + 1, vr1=vr, pr1=pr,
            r2=self.ir.max_reg + 1, vr2=self.ir.max_reg + 1, pr2=self.spill_reg
        )

        self.vr_to_pr[vr] = None
        self.pr_to_vr[pr] = None
        self.vr_spill[vr] = (ADDRESS, m)

        return pr

    def unspill(self, vr):
        """

        """
        pr = self.get_pr()

        spill_val = self.vr_spill[vr]

        # Get address of spilled value
        if spill_val is not None:

            if spill_val[0] == ADDRESS:
                self.new_ir.add_full_token(
                    op=LOADI_VAL,
                    r1=-1, vr1=vr, pr1=spill_val[1],
                    r3=self.spill_reg, vr3=self.ir.max_reg + 1, pr3=self.spill_reg
                )

                self.new_ir.add_full_token(
                    op=LOAD_VAL,
                    r1=self.ir.max_reg + 1, vr1=vr, pr1=self.spill_reg,
                    r3=self.ir.max_reg + 1, vr3=self.ir.max_reg + 1, pr3=pr
                )

            elif spill_val[0] == CONSTANT:
                self.new_ir.add_full_token(
                    op=LOADI_VAL,
                    r1=-3, vr1=vr, pr1=spill_val[1],
                    r3=self.ir.max_reg + 1, vr3=self.ir.max_reg + 1, pr3=pr
                )

        else:

            self.new_ir.add_full_token(
                op=LOADI_VAL,
                r1=-3, vr1=vr, pr1=0,
                r3=self.ir.max_reg + 1, vr3=self.ir.max_reg + 1, pr3=pr
            )

        self.assign_pr(vr, pr)

        return pr


    def assign_pr(self, vr, pr):

        self.vr_to_pr[vr] = pr
        self.pr_to_vr[pr] = vr




