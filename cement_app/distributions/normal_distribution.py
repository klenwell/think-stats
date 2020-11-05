"""
Based on Think Stats 2, Chapter 5.3
http://greenteapress.com/thinkstats2/html/thinkstats2006.html
"""
import math
from matplotlib import pyplot
import numpy as np

from cement_app.services.caching_service import cached_property
from cement_app.distributions.analytic_distribution import AnalyticDistribution


class NormalDistribution(AnalyticDistribution):
    #
    # Static Methods
    #
    @staticmethod
    def model_series(series, low, high):
        return NormalDistribution(series.mean(), series.std(), low, high)

    #
    # Constructor
    #
    def __init__(self, mean, stdev, low=None, high=None):
        self.mean = mean
        self.stdev = stdev
        self.low = low
        self.high = high

    #
    # Properties
    #
    @cached_property
    def values(self):
        return np.sort([self.low, self.high])

    @cached_property
    def probabilities(self):
        return self.mean + self.stdev * self.values

    #
    # Instance Methods
    #
    def plot_line(self, **options):
        line_options = {
            'linewidth': 1,
            'alpha': 0.7
        }

        xlabel = options.get('xlabel', 'Values')
        ylabel = options.get('ylabel', 'Probabilities')

        if xlabel:
            pyplot.xlabel(xlabel)

        if ylabel:
            pyplot.ylabel(ylabel)

        # Prepare xs and ys
        xs = self.values
        ys = self.probabilities

        # Plot it!
        pyplot.plot(xs, ys, **line_options)

        # Still need to call pyplot.show() to display
        return pyplot

    #
    # Private Methods
    #
