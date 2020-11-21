"""
Behavioral Risk Factor Surveillance System Survey

Used with Think Stats 2e:
http://greenteapress.com/thinkstats2/html/thinkstats2002.html
"""
from os.path import join as path_join
import pandas
import numpy as np

from cement_app.services.caching_service import cached_property
from cement_app.config.app import DATA_ROOT


#
# Constants
#
CDC_DATA_DIR = path_join(DATA_ROOT, 'cdc')
SURVEY_DATA_FILE = 'CDBRFS08.ASC.gz'
MALE = 1
FEMALE = 2


class BehavioralRiskFactorExtract:
    #
    # Static Methods
    #

    #
    # Properties
    #
    @cached_property
    def males(self):
        return self.dataframe[self.dataframe.sex == MALE]

    @cached_property
    def dataframe(self):
        df = self.unclean_dataframe

        # clean age
        df.age.replace([7, 9], float('NaN'), inplace=True)

        # clean height
        df.htm3.replace([999], float('NaN'), inplace=True)

        # clean weight
        df.wtkg2.replace([99999], float('NaN'), inplace=True)
        df.wtkg2 /= 100.0

        # clean weight a year ago
        df.wtyrago.replace([7777, 9999], float('NaN'), inplace=True)
        df['wtyrago'] = df.wtyrago.apply(lambda x: x/2.2 if x < 9000 else x-9000)

        return df

    @cached_property
    def unclean_dataframe(self):
        data_path = path_join(CDC_DATA_DIR, SURVEY_DATA_FILE)

        compression = 'gzip'
        colspecs = self.column_specs
        names = self.variables_dataframe['name']

        dataframe = pandas.read_fwf(data_path,
                                    colspecs=colspecs,
                                    names=names,
                                    compression=compression,
                                    nrows=None)
        return dataframe

    @property
    def variables(self):
        return [
            ('age', 101, 102, int),
            ('sex', 143, 143, int),
            ('wtyrago', 127, 130, int),
            ('finalwt', 799, 808, int),
            ('wtkg2', 1254, 1258, int),
            ('htm3', 1251, 1253, int),
        ]

    @property
    def columns(self):
        return ['name', 'start', 'end', 'type']

    @property
    def variables_dataframe(self):
        df = pandas.DataFrame(self.variables, columns=self.columns)
        df.end += 1
        return df

    @property
    def column_specs(self):
        index_base = 1
        specs = self.variables_dataframe[['start', 'end']] - index_base
        return specs.astype(np.int).values.tolist()

    #
    # Private Methods
    #
