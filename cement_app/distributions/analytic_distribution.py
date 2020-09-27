import math
from matplotlib import pyplot
import numpy as np


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
    def __init__(self, lambda_=1, low=0, high=3.0, count=50):
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
        xs = np.linspace(self.low, self.high, self.count)
        probs = 1 - np.exp(-self.λ * xs)
        return list(zip(xs, probs))

    #
    # Instance Methods
    #
    def plot(self, **options):
        pass

    #
    # Private Methods
    #
