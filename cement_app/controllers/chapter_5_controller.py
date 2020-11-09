from cement import Controller
from cement import ex as expose

from scipy import stats
import numpy as np
from matplotlib import pyplot as plt

from cement_app.extracts.brisbane.births import BrisbaneBirthsExtract
from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract
from cement_app.decorators.cdf import CumulativeDistributionFunction as CDF
from cement_app.distributions.normal_distribution import NormalDistribution


class Chapter5Controller(Controller):
    class Meta:
        label = 'ch-5'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py ch-5 s3
    @expose(aliases=['s3'])
    def section_5_3(self):
        # Extract
        extract = FamilyGrowthExtract()
        birth_weights_series = extract.live_births.totalwgt_lb

        # Weights as normal distribution
        n = len(birth_weights_series)
        xs = np.random.normal(0, 1, n)
        xs.sort()
        ys = np.array(birth_weights_series)
        ys.sort()

        options = dict(linewidth=3, alpha=0.7, label='Normal')
        plt.plot(xs, ys, '', **options)

        # As normal distribution
        normal_distribution = NormalDistribution.model_series(birth_weights_series, -4, 4)
        normal_chart = normal_distribution.plot_line()
        normal_chart.show()

    # python app.py ch-5 s2
    @expose(aliases=['s2'])
    def section_5_2(self):
        # Extract
        extract = FamilyGrowthExtract()
        birth_weights_series = extract.live_births.totalwgt_lb

        # Model birthweight CDF
        model_cdf = CDF.model_series(birth_weights_series)
        model_cdf.plot()

        # Plot birthweights chart over model chart
        cdf = CDF.from_series(birth_weights_series, 'weight')
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
