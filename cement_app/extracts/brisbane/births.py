"""
Source:
https://github.com/AllenDowney/ThinkStats2/blob/57d151/code/analytic.py#L40
https://github.com/AllenDowney/ThinkStats2/blob/57d151/code/babyboom.dat

Used with Think Stats 2e:
http://greenteapress.com/thinkstats2/html/thinkstats2006.html
"""
from os.path import join as path_join
import pandas
import numpy as np

from cement_app.services.caching_service import cached_property
from cement_app.config.app import DATA_ROOT


#
# Constants
#
DATA_DIR = path_join(DATA_ROOT, 'brisbane')
BIRTHS_FILE = 'births.dat'


class BrisbaneBirthsExtract:
    #
    # Properties
    #
    @cached_property
    def dataframe(self):
        file_path = path_join(DATA_DIR, BIRTHS_FILE)
        names = self.variables['name']
        skip_rows = 59
        return pandas.read_fwf(file_path, colspecs=self.colspecs, names=names, skiprows=skip_rows)

    @property
    def var_info(self):
        return [
            ('time', 1, 8, int),
            ('sex', 9, 16, int),
            ('weight_g', 17, 24, int),
            ('minutes', 25, 32, int)
        ]

    @property
    def columns(self):
        return ['name', 'start', 'end', 'type']

    @cached_property
    def variables(self):
        variables = pandas.DataFrame(self.var_info, columns=self.columns)
        variables.end += 1
        return variables

    @cached_property
    def colspecs(self):
        index_base = 1
        colspecs = self.variables[['start', 'end']] - index_base
        return colspecs.astype(np.int).values.tolist()

    #
    # Instance Methods
    #
    def __init__(self):
        pass
