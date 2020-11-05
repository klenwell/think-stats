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
        from cement_app.distributions.normal_distribution import NormalDistribution

        # Extract
        extract = FamilyGrowthExtract()
        birth_weights_series = extract.live_births.totalwgt_lb

        # As normal distribution
        normal_distribution = NormalDistribution.model_series(birth_weights_series, -4, 4)
        normal_chart = normal_distribution.plot_line()
        normal_chart.show()
        breakpoint()

        # Model birthweight CDF
        model_cdf = CumulativeDistributionFunction.model_series(birth_weights_series)
        model_chart = model_cdf.plot()

        # Plot birthweights chart over model chart
        cdf = CumulativeDistributionFunction.from_series(birth_weights_series, 'weight')
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
