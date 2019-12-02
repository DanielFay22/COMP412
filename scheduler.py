

import sys

from resources import *
from frontend import *
from core import *
from allocator import *
from scheduling import *

import cProfile


def schedule(filereader):
    """

    """

    scanner = Scanner(fr=filereader)

    ir = InternalRepresentation()

    parser = Parser(scanner=scanner, ir=ir)
    parser.parse()

    if parser.errors:
        error("Parser found {0} syntax errors in {1} lines of input. "
              "Unable to process code.".format(parser.errors, parser.ln))
        exit(1)

    rename_registers(parser.ir)

    scheduler = Scheduler(ir=parser.ir)

    scheduler.schedule()

    scheduler.new_ir.to_code(header = "// Filler comment\n// --- start of renamed code\n")


def help_handler():

    print("COMP 412, Fall 2019 Scheduler (lab 3)\n"
          "Command Syntax:\n"
          "\t./schedule [flags] filename\n"
          "\n"
          "Required arguments:\n"
          "\tfilename  is the pathname (absolute or relative) to the input file\n"
          "\n"
          "Optional flags:\n"
          "\t-h       prints this message\n"
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

            # profile
            elif arg == "-P":
                profile = True

            else:
                if filename is None:
                    filename = arg
                else:
                    command_line_error("Multiple file names/unrecognized flags provided.")
                    exit(1)

        assert not argv, "Did not process all arguments"

        if filename is None: # no file name provided
            command_line_error("Must provide a valid file name.")
            exit(1)

    try:
        reader = FileReader(filename)
    except OSError as o:
        error("Unable to open file with name {0}, no operations performed.".format(filename))
        exit(1)


    # Initialize the profiler
    if profile:
        pr = cProfile.Profile()
        pr.enable()

    schedule(reader)

    # Creates profiler output
    if profile:
        pr.create_stats()
        pr.dump_stats("prof.prof")
        pr.print_stats(sort = 'tottime')
