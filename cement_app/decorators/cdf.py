import math
from matplotlib import pyplot
import numpy as np

from cement_app.decorators.statistical_mapping import StatisticalMapping


class CumulativeDistributionFunction(StatisticalMapping):
    #
    # Static Methods
    #
    @staticmethod
    def from_series(series, label=None):
        """series = pandas.series
        """
        data_list = series.to_list()
        cleaned_data = [n for n in data_list if not math.isnan(n)]
        cdf = CumulativeDistributionFunction(cleaned_data, label=label)
        return cdf

    #
    # Constructor
    #
    def __init__(self, data_list, label=None):
        super().__init__(data_list, label)

    def init_store(self):
        cdf_dict = {}
        super().init_store()
        total_sum = sum(val*freq for val, freq in self.store.items())
        cumulative_sum = 0

        for value in sorted(self.values()):
            freq = self.freq(value)
            cumulative_sum += (value * freq)
            cdf_dict[value] = cumulative_sum / total_sum

        self.update(cdf_dict)

    #
    # Properties
    #

    #
    # Instance Methods
    #
    def plot(self, **options):
        line_options = {
            'linewidth': 1,
            'alpha': 0.7
        }

        xlabel = options.get('xlabel', 'Values')
        ylabel = options.get('ylabel', 'CDF')

        if xlabel:
            pyplot.xlabel(xlabel)

        if ylabel:
            pyplot.ylabel(ylabel)

        # xs = values, ys = probabilities
        xs, ys = zip(*sorted(self.items()))

        # Convert bars to continues series of lines for line chart
        # Source: https://github.com/AllenDowney/ThinkStats2/blob/b3db0d/thinkplot/thinkplot.py#L468
        ln_width = options.pop('width', np.diff(xs).min())
        line_pts = []
        last_x = np.nan
        last_y = 0

        for x, y in zip(xs, ys):
            line_pts.append((x, last_y))
            line_pts.append((x, y))
            line_pts.append((x + ln_width, y))

            last_x = x + ln_width
            last_y = y

        line_pts.append((last_x, last_y))
        ln_xs, ln_ys = zip(*line_pts)

        # Note: plot vs bar
        pyplot.plot(ln_xs, ln_ys, **line_options)

        # Still need to call pyplot.show() to display
        return pyplot

    #
    # Private Methods
    #
