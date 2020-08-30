from collections.abc import MutableMapping
from collections import Counter
from matplotlib import pyplot


class Histogram(MutableMapping):
    """Source: https://stackoverflow.com/a/3387975/1093087
    """
    #
    # Static Methods
    #
    @staticmethod
    def from_series(series, label=None):
        """series = pandas.series
        """
        histogram = Histogram(series.values(), label=label)
        return histogram

    #
    # Constructor
    #
    def __init__(self, data_list, label=None):
        self.store = dict()
        self.update(Counter(data_list))

        # Keyword args
        self.label = label

    #
    # Instance Methods
    #
    def values(self):
        return list(self.keys())

    def freq(self, key):
        return self.store.get(key, 0)

    def plot(self):
        options = {
            'linewidth': 0,
            'alpha': 0.6
        }

        xs, ys = zip(*sorted(self.items()))
        pyplot.bar(xs, ys, **options)
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
