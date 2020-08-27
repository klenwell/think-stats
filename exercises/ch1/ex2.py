"""
Think Stats 2e

See Constants below.

Data Source: https://www.cdc.gov/nchs/nsfg/nsfg_cycle6.htm

USAGE:
    python exercises/ch1/ex2.py
"""
# Insert root directory in PATH
import sys
from os.path import dirname
ROOT_DIR = dirname(dirname(dirname(__file__)))
sys.path.insert(0, ROOT_DIR)

# Imports
from extracts.cdc.nsfg import CdcNsfgExtract


#
# Constants
#
URL = "http://greenteapress.com/thinkstats2/html/thinkstats2002.html"
CHAPTER = 1
EXERCISE = 2


#
# Actions
#
# python exercises/ch1/ex2.py
def interactive(args):
    print("Chapter {} Exercise #{}".format(CHAPTER, EXERCISE))
    print("You are interactive mode for {}".format(sys.argv[0]))
    breakpoint()


# python exercises/ch1/ex2.py exercise
def exercise(args):
    extract = CdcNsfgExtract()
    print(extract)


#
# Controller
#
def controller():
    args = sys.argv[1:]
    command = args[0] if args else None

    print('Command: %s / Arguments: %s' % (command, args))

    if command == 'exercise':
        exercise(args)
    else:
        interactive(args)


#
# Main
#
if __name__ == '__main__':
    controller()
