"""
This file contain a doctest of next_lorenz_step() from solver.py


"""
import doctest
import sys
sys.path.append('../')
import fractal

def fractal_doctest():
    doctest.testmod(fractal.naive, verbose=True)
    doctest.testmod(fractal.parallel, verbose=True)

if __name__ == "__main__":
    """Main function for running the doctest script.

    Doctest looks though the specified file and locate doctest embedded in the docstrings of functions.
    """
    fractal_doctest()