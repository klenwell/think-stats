from collections.abc import MutableMapping
from collections import Counter
from matplotlib import pyplot
from statistics import stdev
import math


class StatisticalMapping(MutableMapping):
    """Dictionary override based on this SO answer:
    https://stackoverflow.com/a/3387975/1093087

    A variation on this class:
    https://github.com/AllenDowney/ThinkStats2/blob/master/code/thinkstats2.py#L437
    """
    #
    # Static Methods
    #
    @staticmethod
    def from_series(series, label=None):
        """series = pandas.series
        """
        data_list = series.to_list()
        cleaned_data = [n for n in data_list if not math.isnan(n)]
        stats_mapping = StatisticalMapping(cleaned_data, label=label)
        return stats_mapping

    #
    # Constructor
    #
    def __init__(self, data_list, label=None):
        self.data = data_list
        self.label = label
        self.store = dict()
        self.update(Counter(data_list))

    #
    # Properties
    #
    @property
    def total(self):
        return sum(self.counts())

    @property
    def mean(self):
        total = sum([v*n for (v, n) in self.items()])
        count = sum(self.counts())
        return total / count

    @property
    def stdev(self):
        return stdev(self.data)

    @property
    def frequencies(self):
        return self.counts()

    @property
    def mode(self):
        # The mode of a distribution is the most frequent value.
        return self.modes[0][0]

    @property
    def modes(self):
        # https://stackoverflow.com/a/2258273/1093087
        return sorted(self.items(), key=lambda item: item[1], reverse=True)

    #
    # Instance Methods
    #
    def values(self):
        return list(self.keys())

    def counts(self):
        return [freq for freq in self.store.values()]

    def freq(self, value):
        return self.store.get(value, 0)

    def plot(self, **options):
        bar_options = {
            'linewidth': 0,
            'alpha': 0.6
        }

        xlabel = options.get('xlabel')
        ylabel = options.get('ylabel')

        if xlabel:
            pyplot.xlabel(xlabel)

        if ylabel:
            pyplot.ylabel(ylabel)

        xs, ys = zip(*sorted(self.items()))

        # Note: bar vs plot
        pyplot.bar(xs, ys, **bar_options)

        # Caller must call show method.
        return pyplot

    #
    # Private Methods
    #
    def __repr__(self):
        name = self.__class__.__name__
        if not self.label:
            return '{}({})'.format(name, self.store)
        else:
            return '{}[{}]({})'.format(name, self.label, self.store)

    #
    # Required MutableMapping Interface Methods
    #
    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
