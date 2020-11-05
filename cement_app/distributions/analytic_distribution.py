from matplotlib import pyplot
import numpy as np

from cement_app.services.caching_service import cached_property


class AnalyticDistribution:
    #
    # Static Methods
    #
    @staticmethod
    def exponential(λ=1):
        return AnalyticDistribution(λ)

    #
    # Constructor
    #
    def __init__(self, lambda_=1, low=0, high=10.0, count=50):
        self.λ = lambda_
        self.low = low
        self.high = high
        self.count = count

    #
    # Properties
    #
    @property
    def sequence(self):
        """Generates sequence as list of tuples.

        Source:
        https://github.com/AllenDowney/ThinkStats2/blob/ed2aaa08/code/thinkstats2.py#L2112
        """
        return list(zip(self.values, self.probabilities))

    @cached_property
    def values(self):
        return np.linspace(self.low, self.high, self.count)

    @cached_property
    def probabilities(self):
        return 1 - np.exp(-self.λ * self.values)

    @property
    def plot_points(self):
        """Convert bars to continues series of lines for line chart

        Source:
        https://github.com/AllenDowney/ThinkStats2/blob/b3db0d/thinkplot/thinkplot.py#L468
        """
        line_pts = []

        ln_width = np.diff(self.values).min()
        last_x = np.nan
        last_y = 0

        for x, y in self.sequence:
            line_pts.append((x, last_y))
            line_pts.append((x, y))
            line_pts.append((x + ln_width, y))

            last_x = x + ln_width
            last_y = y

        line_pts.append((last_x, last_y))
        return line_pts

    #
    # Instance Methods
    #
    def plot(self, **options):
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
        xs, ys = zip(*self.plot_points)

        # Plot it!
        pyplot.plot(xs, ys, **line_options)

        # Still need to call pyplot.show() to display
        return pyplot

    #
    # Private Methods
    #
