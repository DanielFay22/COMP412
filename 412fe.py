

import sys

from resources import *
from core import *



reader = None
scanner = None
ir = None

def help_handler():

    print("COMP 412, Fall 2019 Front End (lab 1)\n"
          "Command Syntax:\n"
          "\t./lab1_ref [flags] filename\n"
          "\n"
          "Required arguments:\n"
          "\tfilename  is the pathname (absolute or relative) to the input file\n"
          "\n"
          "Optional flags:\n"
          "\t-h       prints this message\n"
          "\t-l       Opens log file \"./Log\" and starts logging.\n"
          "\t-s       prints tokens in token stream\n"
          "\t-p       invokes parser and reports on success or failure\n"
          "\t-r       prints human readable version of parser's IR")




if __name__ == "__main__":
    argv = sys.argv[1:]

    p = False
    s = False
    r = False

    filename = None

    # Invalid
    if not len(argv):
        error("No command line arguments specified.")
        exit(1)
    else:
        while argv:
            arg = argv.pop(0)

            if arg == "-h":
                help_handler()
                exit(0)

            elif arg == "-p":
                if p or s or r:
                    error("Input should contain only one command line flag. "
                          "Defaulting to highest priority flag.")

                    if not r:
                        p, s = True, False

                else:
                    p = True

            elif arg == "-s":
                if p or s or r:
                    error("Input should contain only one command line flag. "
                          "Defaulting to highest priority flag.")

                else:
                    s = True

            elif arg == "-r":
                if p or r or s:
                    error("Input should contain only one command line flag. "
                          "Defaulting to highest priority flag.")

                    p, s = False, False

                r = True

            else:
                if filename is None:
                    filename = arg
                else:
                    error("Multiple file names provided.")
                    exit(1)

        # default behavior
        if not (p or r or s):
            p = True

        assert not argv, "Did not process all arguments"

        if filename is None: # no file name provided
            error("Must provide a valid file name.")
            exit(1)


    try:
        reader = FileReader(filename)
    except OSError as o:
        error(f"Unable to open file with name {filename}")
        exit(1)

    scanner = Scanner(fr = reader)

    c = scanner.get_token()

    while True:
        if c:
            print(repr(c))

        if isinstance(c, ENDFILE):
            break
        else:
            c = scanner.get_token()







