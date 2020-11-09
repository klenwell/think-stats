from cement import Controller
from cement import ex as expose

from scipy import stats
import numpy as np

from cement_app.extracts.brisbane.births import BrisbaneBirthsExtract
from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract
from cement_app.decorators.cdf import CumulativeDistributionFunction as CDF


class Chapter5Controller(Controller):
    class Meta:
        label = 'ch-5'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py ch-5 s2
    @expose(aliases=['s2'])
    def section_5_2(self):
        # Plot birthweights
        extract = FamilyGrowthExtract()
        cdf = CDF.from_series(extract.live_births.totalwgt_lb, 'weight')
        print(cdf.median)

        # Birth weights sans null values
        weights = extract.live_births.totalwgt_lb.dropna()

        # Estimate parameters: trimming outliers yields a better fit
        # Lop off high and low 1% of values
        trimmed_margin = 0.01
        trimmed_count = int(trimmed_margin * len(weights))
        trimmed_weights = sorted(weights)[trimmed_count:-trimmed_count]

        # Compute mean
        weights_as_array = np.asarray(trimmed_weights)
        mean = weights_as_array.mean()

        # Compute variance
        devs = weights_as_array - mean
        var = np.dot(devs, devs) / len(weights_as_array)
        sigma = np.sqrt(var)
        print(var, sigma)

        # xs, ps = thinkstats2.RenderNormalCdf(mu, sigma, low=0, high=12.5)
        low, high, steps = 0, 12.5, 101
        vals = np.linspace(low, high, steps)
        probs = stats.norm.cdf(vals, mean, sigma)

        model_cdf = CDF([])
        for weight, cum_dist in zip(vals, probs):
            model_cdf.store[weight] = cum_dist

        # Plot birth chart over model chart
        model_cdf.plot()
        births_chart = cdf.plot()
        births_chart.show()

    # python app.py ch-5 s1
    @expose(aliases=['s1'])
    def section_5_1(self):
        extract = BrisbaneBirthsExtract()
        diffs = extract.dataframe.minutes.diff()
        cdf = CDF.from_series(diffs, 'actual')
        chart = cdf.plot()
        chart.show()
