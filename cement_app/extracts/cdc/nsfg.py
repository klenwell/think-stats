"""
CDC National Survey of Family Growth
https://www.cdc.gov/nchs/nsfg/nsfg_cycle6.htm

Used with Think Stats 2e:
http://greenteapress.com/thinkstats2/html/thinkstats2002.html
"""
from os.path import join as path_join
import pandas
import numpy as np
from collections import defaultdict
import random
import math

from cement_app.services.caching_service import cached_property
from cement_app.config.app import DATA_ROOT


#
# Constants
#
CDC_DATA_DIR = path_join(DATA_ROOT, 'cdc')
RESPONDENTS_DAT_FILE = '2002FemResp.dat.gz'
RESPONDENTS_DCT_FILE = '2002FemResp.dct'
PREGANCIES_DAT_FILE = '2002FemPreg.dat.gz'
PREGANCIES_DCT_FILE = '2002FemPreg.dct'

LIVE_BIRTH = 1
FIRST_BIRTH = 1


class FamilyGrowthExtract:
    #
    # Static Methods
    #
    @staticmethod
    def cohen_effect_size(this_series, that_series):
        diff = this_series.mean() - that_series.mean()

        this_var = this_series.var()
        that_var = that_series.var()
        this_series_size = len(this_series)
        that_series_size = len(that_series)

        num = this_series_size * this_var + that_series_size * that_var
        den = this_series_size + that_series_size
        pooled_var = num / den

        cohen_d = diff / math.sqrt(pooled_var)
        return cohen_d

    #
    # Properties
    #
    @cached_property
    def females(self):
        data_path = path_join(CDC_DATA_DIR, RESPONDENTS_DAT_FILE)
        dct_path = path_join(CDC_DATA_DIR, RESPONDENTS_DCT_FILE)

        column_df = self.dct_file_to_dataframe(dct_path)
        names = column_df.name.values
        col_widths = column_df.width.astype(np.int).values

        dataframe = pandas.read_fwf(data_path, names=names, widths=col_widths, compression='gzip')
        return dataframe

    @cached_property
    def pregnancies(self):
        data_path = path_join(CDC_DATA_DIR, PREGANCIES_DAT_FILE)
        dct_path = path_join(CDC_DATA_DIR, PREGANCIES_DCT_FILE)

        column_df = self.dct_file_to_dataframe(dct_path)
        names = column_df.name.values
        col_widths = column_df.width.astype(np.int).values

        dataframe = pandas.read_fwf(data_path, names=names, widths=col_widths, compression='gzip')

        # Data normalizations
        # mother's age is encoded in centiyears; convert to years
        dataframe.agepreg /= 100.0

        # birthwgt_lb contains at least one bogus value (51 lbs)
        # replace with NaN
        dataframe.loc[dataframe.birthwgt_lb > 20, 'birthwgt_lb'] = np.nan

        # replace 'not ascertained', 'refused', 'don't know' with NaN
        na_vals = [97, 98, 99]
        dataframe.birthwgt_lb.replace(na_vals, np.nan, inplace=True)
        dataframe.birthwgt_oz.replace(na_vals, np.nan, inplace=True)
        dataframe.hpagelb.replace(na_vals, np.nan, inplace=True)

        dataframe.babysex.replace([7, 9], np.nan, inplace=True)
        dataframe.nbrnaliv.replace([9], np.nan, inplace=True)

        # birthweight is stored in two columns, lbs and oz. convert to a single column in lb
        dataframe['totalwgt_lb'] = dataframe.birthwgt_lb + (dataframe.birthwgt_oz / 16.0)

        return dataframe

    @cached_property
    def response_cases(self):
        cases = defaultdict(list)
        for index, case_id in self.pregnancies.caseid.iteritems():
            cases[case_id].append(index)
        return cases

    @property
    def random_female(self):
        case_ids = list(self.response_cases.keys())
        random_case_id = random.choice(case_ids)
        return self.females[self.females.caseid == random_case_id]

    @property
    def live_births(self):
        return self.pregnancies[self.pregnancies.outcome == LIVE_BIRTH]

    @property
    def live_first_births(self):
        return self.live_births[self.live_births.birthord == FIRST_BIRTH]

    @property
    def live_non_first_births(self):
        return self.live_births[self.live_births.birthord != FIRST_BIRTH]

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
