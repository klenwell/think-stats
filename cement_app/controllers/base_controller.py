from cement import Controller
from cement import ex as expose


class BaseController(Controller):
    class Meta:
        label = 'base'

    # python app.py interactive
    # This command can be used for testing and development.
    @expose(help="Run the Application interactively. Useful for testing and development.")
    def interactive(self):
        from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract
        from cement_app.decorators.cdf import CumulativeDistributionFunction

        # Plot birthweights
        extract = FamilyGrowthExtract()
        cdf = CumulativeDistributionFunction.from_series(extract.live_births.totalwgt_lb, 'weight')
        print(cdf.median)

        # Plot Model
        from scipy import stats
        import numpy as np

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

        model_cdf = CumulativeDistributionFunction([])
        for weight, cum_dist in zip(vals, probs):
            model_cdf.store[weight] = cum_dist

        model_chart = model_cdf.plot()

        # Plot birth chart over model chart
        births_chart = cdf.plot()
        births_chart.show()


    # python app.py test -f foo arg1 extra1 extra2
    @expose(
        help="Test Cement framework and CLI.",
        arguments=[
            (['-f', '--foo'], dict(action='store', help='the notorious foo')),

            # https://github.com/datafolklabs/cement/issues/256
            (['arg1'], dict(action='store', nargs=1)),
            (['extras'], dict(action='store', nargs='*'))
        ]
    )
    def test(self):
        vars = {'args': self.app.pargs}
        self.app.render(vars, 'test.jinja2')
