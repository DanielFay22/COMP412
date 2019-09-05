
import sys

def error(msg: str, err_type: str = "Error"):
    """
    Prints error message to stderr.
    """
    sys.stderr.write(f"{err_type}: {msg}\n")