"""
Source:
https://github.com/AllenDowney/ThinkStats2/blob/57d151/code/analytic.py#L40
https://github.com/AllenDowney/ThinkStats2/blob/57d151/code/babyboom.dat

Used with Think Stats 2e:
http://greenteapress.com/thinkstats2/html/thinkstats2006.html
"""
from os.path import join as path_join
import numpy as np

from cement_app.services.caching_service import cached_property
from cement_app.config.app import DATA_ROOT


#
# Constants
#
DATA_DIR = path_join(DATA_ROOT, 'brisbane')
BIRTHS_FILE = 'TBA'


class BrisbaneBirthsExtract:
    pass
