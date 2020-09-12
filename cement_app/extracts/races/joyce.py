"""
Data Source:
https://github.com/AllenDowney/ThinkStats2/blob/9ee747/code/relay.py
https://github.com/AllenDowney/ThinkStats2/blob/9ee747/code/Apr25_27thAn_set1.shtml

Used with Think Stats 2e:
http://greenteapress.com/thinkstats2/html/thinkstats2004.html
"""
from os.path import join as path_join
import numpy as np

from cement_app.services.caching_service import cached_property
from cement_app.config.app import DATA_ROOT


#
# Constants
#
CDC_DATA_DIR = path_join(DATA_ROOT, 'races')
RESULTS_2010_FILE = '20100425-joyce-10k-results.shtml'


class JamesJoyceRelayExtract:
    #
    # Static Methods
    #

    def for_2010():
        file_path = path_join(CDC_DATA_DIR, RESULTS_2010_FILE)
        extract = JamesJoyceRelayExtract(file_path)
        return extract

    #
    # Properties
    #
    @cached_property
    def rows(self):
        rows = self.process()
        return rows

    @property
    def speeds(self):
        speeds = []
        col_index = 5

        for row in self.rows:
            pace = row[col_index]
            speed = self.pace_to_speed(pace)
            speeds.append(speed)

        return speeds

    @property
    def speed_bins(self):
        """Return numpy array of speeds rounds off to fit 100 bins.
        """
        low = 3
        high = 12
        bins = 100
        return self.bin_data(self.speeds, low, high, bins)

    @property
    def columns(self):
        return [
            'Place',
            'Div/Tot',
            'Division',
            'Guntime',
            'Nettime',
            'Pace'
        ]

    #
    # Instance Methods
    #
    def __init__(self, file_path):
        self.file_path = file_path

    def process(self):
        rows = []
        for line in open(self.file_path):
            row = self.process_row(line)
            if row:
                rows.append(row)
        return rows

    #
    # Private
    #
    def bin_data(self, data, low, high, n):
        """Rounds data off into bins.

        data: sequence of numbers
        low: low value
        high: high value
        n: number of bins

        returns: sequence of numbers
        """
        data = (np.array(data) - low) / (high - low) * n
        data = (np.round(data) * (high - low) / n) + low
        return data

    def pace_to_speed(self, pace):
        min, sec = pace.split(':')
        secs = (int(min) * 60) + int(sec)
        mph = 1.0 / secs * 60 * 60
        return mph

    def process_row(self, line):
        """Data row will look like this:
        1   1/362  M2039   30:43   30:42   4:57 Brian Harvey           22 M  1422 Allston MA

        Columns:
        Place Div/Tot  Div   Guntime Nettime  Pace  Name                   Ag S Race# City/state
        """
        cols = line.split()

        if len(cols) < 6:
            return None

        place, divtot, div, gun, net, pace = cols[0:6]

        if '/' not in divtot:
            return None

        for time in [gun, net, pace]:
            if ':' not in time:
                return None

        return place, divtot, div, gun, net, pace
