"""
CDC National Survey of Family Growth
https://www.cdc.gov/nchs/nsfg/nsfg_cycle6.htm

Used with Think Stats 2e:
http://greenteapress.com/thinkstats2/html/thinkstats2002.html
"""
from cement_app.services.caching import cached_property
import pandas


#
# Constants
#
DATA_FILE = None


class FamilyGrowthExtract:
    #
    # Properties
    #
    @cached_property
    def dataframe(self):
        df = pandas.read_fwf(DATA_FILE, compression='gzip')
        return df
