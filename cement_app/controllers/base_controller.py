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

        extract = FamilyGrowthExtract()
        cdf = CumulativeDistributionFunction.from_series(extract.live_births.prglngth, 'births')
        print(cdf)

        sample = {
            'cdf.prob(38)': cdf.prob(38),
            'cdf.value(cdf.prob(38))': cdf.value(cdf.prob(38)),
            'cdf.percentile_rank(38)': cdf.percentile_rank(38),
            'cdf.percentile(cdf.percentile_rank(38))': cdf.percentile(cdf.percentile_rank(38)),
            'cdf.median': cdf.median
        }
        print(sample)

        chart = cdf.plot()
        chart.show()
        breakpoint()

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
