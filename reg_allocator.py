

import sys

from resources import *
from frontend import *
from core import *
from allocator import *

import cProfile



def rename_regs(ir: InternalRepresentation):
    """
    Renames registers in the ir such that each register is defined only once.
    """
    rename_registers(ir)

    ir.to_code_v(header = "// Filler comment\n// --- start of renamed code\n")


def allocate_regs(ir: InternalRepresentation, k: int):
    """
    Perform a register allocation with k physical registers.
    """
    rename_registers(ir)

    a = Allocator(ir, k)
    a.allocate_registers()

    new_ir = a.new_ir

    new_ir.to_code(header = "// Filler comment\n// --- start of renamed code\n")


def help_handler():

    print("COMP 412, Fall 2019 Register Allocator (lab 2)\n"
          "Command Syntax:\n"
          "\t./412alloc [flags] filename\n"
          "\n"
          "Required arguments:\n"
          "\tfilename  is the pathname (absolute or relative) to the input file\n"
          "\n"
          "Optional flags:\n"
          "\t-h       prints this message\n"
          "\t-x       Outputs ILOC with registers renamed so each is defined only once\n"
          "\tk        Performs regsiter allocation with k regsiters, where k is an integer in the range [3,64]\n"
          "\t-P       Enables profiling.")


def command_line_error(msg: str):
    """
    Prints error message to stderr, followed by printing correct command line usage to stdout.
    """
    error(msg, "Command Line Error")
    print("Correct Usage:")
    help_handler()


if __name__ == "__main__":
    argv = sys.argv[1:]

    x = False
    a = False
    k = None

    profile = False
    pr = None

    filename = None

    # Invalid
    if not len(argv):
        command_line_error("No command line arguments specified.")
        exit(1)
    else:
        while argv:
            arg = argv.pop(0)

            if arg == "-h":
                help_handler()
                exit(0)

            elif arg == "-x":

                if a:
                    error("Input should contain only one command line flag. "
                          "Defaulting to highest priority flag.")
                else:
                    x = True

            elif arg.isdigit():
                if x:
                    error("Input should contain only one command line flag. "
                          "Defaulting to highest priority flag.")
                    x = False

                a = True
                k = int(arg)

                if not 3 <= k <= 64:
                    error("Number of registers must be an integer in the range [3,64]. "
                          "Setting k to the nearest allowable value.")
                    k = 3 if k < 3 else 64

            # profile
            elif arg == "-P":
                profile = True

            else:
                if filename is None:
                    filename = arg
                else:
                    command_line_error("Multiple file names/unrecognized flags provided.")
                    exit(1)

        # default behavior
        if not (x or a):
            error("No valid command line option specified.")
            exit(1)

        assert not argv, "Did not process all arguments"

        if filename is None: # no file name provided
            command_line_error("Must provide a valid file name.")
            exit(1)

    reader = None
    try:
        reader = FileReader(filename)
    except OSError as o:
        error("Unable to open file with name {0}, no operations performed.".format(filename))
        exit(1)

    assert reader is not None, "Invalid reader object"


    # Initialize the profiler
    if profile:
        pr = cProfile.Profile()
        pr.enable()

    scanner = Scanner(fr=reader)

    ir = InternalRepresentation()
    parser = Parser(scanner = scanner, ir = ir)

    parser.parse()

    if parser.errors:
        error("Parser found {0} syntax errors in {1} lines of input. "
              "Unable to process code.".format(parser.errors, parser.ln))
        exit(1)

    if x:
        rename_regs(parser.ir)

    elif a:
        assert isinstance(k, int), "k is not valid type."

        allocate_regs(ir, k)

    # Creates profiler output
    if profile:
        pr.create_stats()
        pr.dump_stats("prof.prof")
        pr.print_stats(sort = 'tottime')
