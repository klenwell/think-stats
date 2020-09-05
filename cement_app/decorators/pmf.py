from collections.abc import MutableMapping
from math import isnan

from cement_app.decorators.histogram import Histogram


class ProbabilityMassFunction(MutableMapping):
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
        cleaned_data = [n for n in data_list if not isnan(n)]
        pmf = ProbabilityMassFunction(cleaned_data, label=label)
        return pmf

    #
    # Constructor
    #
    def __init__(self, data_list, label=None):
        self.data = data_list
        self.label = label
        self.store = dict()
        self.histogram = Histogram(data_list, label)

        for val, freq in self.histogram.items():
            self.store[val] = freq / self.histogram.total

    #
    # Properties
    #
    @property
    def total(self):
        return sum(self.store.values())

    @property
    def mean(self):
        pass

    @property
    def stdev(self):
        pass

    #
    # Instance Methods
    #
    def values(self):
        return list(self.keys())

    def probabilities(self):
        return self.store.values()

    def prob(self, value):
        return self.store.get(value, 0)

    def increase(self, value, amount):
        self.store[value] = self.store.get(value, 0) + amount
        return self

    def normalize(self):
        factor = 1 / self.total

        for val in self.values():
            self.store[val] *= factor

        return self

    def plot(self, **options):
        pass

    #
    # Private Methods
    #
    def __repr__(self):
        if not self.label:
            return 'ProbabilityMassFunction({})'.format(self.store)
        else:
            return 'ProbabilityMassFunction[{}]({})'.format(self.label, self.store)

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
