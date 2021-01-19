from cement import Controller
from cement import ex as expose

from scipy import stats
import numpy as np
from matplotlib import pyplot as plt
import math

from cement_app.extracts.brisbane.births import BrisbaneBirthsExtract
from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract
from cement_app.extracts.cdc.brfss import BehavioralRiskFactorExtract
from cement_app.decorators.cdf import CumulativeDistributionFunction as CDF
from cement_app.distributions.normal_distribution import NormalDistribution


class Chapter5Controller(Controller):
    class Meta:
        label = 'ch-5'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py ch-5 e2
    @expose(aliases=['e2'])
    def exercise_5_2(self):
        x_min = 1.0  # meter
        alpha = 1.7

        # Use scipy pareto
        pareto_dist = stats.pareto(b=alpha, scale=x_min)

        # ppf = percent point function or inverse CDF
        seven_billion = 7e9
        top_percentile = 1 - (1 / seven_billion)
        tallest_of_7_billion = pareto_dist.ppf(top_percentile)

        vars = {
            'mean_height': pareto_dist.mean(),
            'shorter_than_mean': pareto_dist.cdf(pareto_dist.mean()) * 100,
            'taller_than_1_km': (1 - pareto_dist.cdf(1000)) * seven_billion,
            'tallest_height': tallest_of_7_billion
        }

        self.app.render(vars, 'exercises/ch5_2.jinja2')

    # python app.py ch-5 e1
    @expose(aliases=['e1'])
    def exercise_5_1(self):
        # US Male heights
        loc = 178
        scale = 7.7
        cm_in_inch = 2.54

        blue_man_min = 70 * cm_in_inch
        blue_man_max = 73 * cm_in_inch

        extract = BehavioralRiskFactorExtract()
        male_heights_with_nans = extract.males.htm3.to_list()
        male_heights = [n for n in male_heights_with_nans if not math.isnan(n)]
        num_males = len(male_heights)

        cdf_min = stats.norm.cdf(blue_man_min, loc=loc, scale=scale)
        cdf_max = stats.norm.cdf(blue_man_max, loc=loc, scale=scale)
        actual_males = [ht for ht in male_heights if ht >= blue_man_min and ht <= blue_man_max]

        vars = {
            'num_males': num_males,
            'blue_man_min_max': (blue_man_min, blue_man_max),
            'cdf_min_cdf_max': (cdf_min, cdf_max),
            'cdf_pct': cdf_max - cdf_min,
            'cdf_count': (cdf_max - cdf_min) * num_males,
            'actual_count': len(actual_males),
            'actual_pct': len(actual_males) / num_males
        }
        self.app.render(vars, 'exercises/ch5_1.jinja2')

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
