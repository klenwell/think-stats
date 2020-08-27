"""
Think Stats 2e

See Constants below.

USAGE:
    python exercises/ch1/ex2.py
"""
import sys


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
    print("You are interactive mode for {}".format(sys.argv[0]))
    breakpoint()


# python exercises/ch1/ex2.py exercise
def exercise(args):
    pass


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
