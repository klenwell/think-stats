"""
For Exercise #4 here:
http://greenteapress.com/thinkstats2/html/thinkstats2004.html
"""
from cement_app.decorators.pmf import ProbabilityMassFunction


class ObservedPmf(ProbabilityMassFunction):
    #
    # Constructor
    #
    def __init__(self, pmf, observer_value):
        super().__init__(pmf.data, pmf.label)
        self.observer = observer_value
        self.adjust_by_observer(observer_value)

    #
    # Instance Methods
    #
    def adjust_by_observer(self, observer_value):
        for value in self.values():
            diff = abs(value - observer_value)

            # The chance of observing a runner is proportional to the difference in speed.
            self.multiply(value, diff)

        self.normalize()
        return self
