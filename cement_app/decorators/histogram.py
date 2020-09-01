from collections.abc import MutableMapping
from collections import Counter
from matplotlib import pyplot
from math import isnan
from statistics import stdev


class Histogram(MutableMapping):
    """Dictionary override based on this SO answer:
    https://stackoverflow.com/a/3387975/1093087
    """
    #
    # Static Methods
    #
    @staticmethod
    def from_series(series, label=None):
        """series = pandas.series
        """
        data_list = series.to_list()
        cleaned_data = [n for n in data_list if not isnan(n)]
        histogram = Histogram(cleaned_data, label=label)
        return histogram

    #
    # Constructor
    #
    def __init__(self, data_list, label=None):
        self.data = data_list
        self.store = dict()
        self.update(Counter(data_list))

        # Keyword args
        self.label = label

    #
    # Properties
    #
    @property
    def mean(self):
        total = sum([v*n for (v,n) in self.items()])
        count = sum(self.counts())
        return total / count

    @property
    def stdev(self):
        return stdev(self.data)

    #
    # Instance Methods
    #
    def values(self):
        return list(self.keys())

    def counts(self):
        return [count for (_, count) in self.items()]

    def freq(self, key):
        return self.store.get(key, 0)

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
        pyplot.bar(xs, ys, **bar_options)
        pyplot.show()

    #
    # Private Methods
    #
    def __repr__(self):
        if not self.label:
            return 'Histogram({})'.format(self.store)
        else:
            return 'Histogram[{}]({})'.format(self.label, self.store)

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
