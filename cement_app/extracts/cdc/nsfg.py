"""
CDC National Survey of Family Growth
https://www.cdc.gov/nchs/nsfg/nsfg_cycle6.htm

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
RESPONDENTS_DAT_FILE = '2002FemResp.dat.gz'
RESPONDENTS_DCT_FILE = '2002FemResp.dct'


class FamilyGrowthExtract:
    #
    # Properties
    #
    @cached_property
    def respondents(self):
        data_path = path_join(CDC_DATA_DIR, RESPONDENTS_DAT_FILE)
        dct_path = path_join(CDC_DATA_DIR, RESPONDENTS_DCT_FILE)

        column_df = self.dct_file_to_dataframe(dct_path)
        names = column_df.name.values
        col_widths = column_df.width.astype(np.int).values

        dataframe = pandas.read_fwf(data_path, names=names, widths=col_widths, compression='gzip')
        return dataframe

    #
    # Private Methods
    #
    def dct_file_to_dataframe(self, dct_file):
        df_columns = ['start', 'width', 'type', 'name', 'format', 'desc']
        dct_columns = []

        with open(dct_file) as f:
            for line in f:
                if '_column' not in line:
                    continue

                attrs = self.dct_line_to_attrs(line)
                dct_columns.append(attrs)

        dataframe = pandas.DataFrame(dct_columns, columns=df_columns)
        return dataframe

    def dct_line_to_attrs(self, line):
        type_map = dict(byte=int, int=int, long=int, float=float, double=float, numeric=float)

        head, tail = line.split('"', 1)

        col_num, col_type, name, format_str = head.split()

        start = self.extract_digits_from_str(col_num)
        width = self.extract_digits_from_str(format_str)
        col_type = str if col_type.startswith('str') else type_map[col_type]
        name = name.lower()
        desc, _ = tail.split('"')

        return (start, width, col_type, name, format_str, desc)

    def extract_digits_from_str(self, str_):
        return int(''.join(filter(lambda i: i.isdigit(), str_)))
