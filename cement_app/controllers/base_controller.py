from cement import Controller
from cement import ex as expose


class BaseController(Controller):
    class Meta:
        label = 'base'

    # python app.py interactive
    # This command can be used for testing and development.
    @expose(help="Run the Application interactively. Useful for testing and development.")
    def interactive(self):
        from cement_app.extracts.brisbane.births import BrisbaneBirthsExtract
        from cement_app.decorators.cdf import CumulativeDistributionFunction as CDF

        extract = BrisbaneBirthsExtract()
        diffs = extract.dataframe.minutes.diff()
        cdf = CDF.from_series(diffs, 'actual')
        chart = cdf.plot()
        chart.show()

        print(extract.dataframe)
        breakpoint()

        from cement_app.distributions.analytic_distribution import AnalyticDistribution

        dist = AnalyticDistribution.exponential()
        print(dist.sequence)
        breakpoint()

        chart = dist.plot()
        chart.show()

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
