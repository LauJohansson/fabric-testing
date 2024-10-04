import os
import sys
from contextlib import contextmanager


@contextmanager
def clear_output_from_powershell():
    """
    A context manager that allows printing to the terminal and then clears the output
    so that PowerShell does not capture it in $out.
    """
    original_stdout = sys.stdout
    try:
        # Print to the terminal as usual
        yield
        # After printing, redirect stdout temporarily to os.devnull (clear it)
        sys.stdout = open(os.devnull, 'w')
    finally:
        # Restore stdout to its original state
        sys.stdout.close()
        sys.stdout = original_stdout

@contextmanager
def no_output_to_powershell():
    """
    A context manager that temporarily redirects sys.stdout to os.devnull,
    preventing PowerShell from capturing printed output.
    """
    original_stdout = sys.stdout
    try:
        sys.stdout = open(os.devnull, "w")
        yield
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout