from cement import Controller
from cement import ex as expose


class BaseController(Controller):
    class Meta:
        label = 'base'

    # python app.py interactive
    # This command can be used for testing and development.
    @expose(help="Run the Application interactively. Useful for testing and development.")
    def interactive(self):
        from cement_app.decorators.histogram import Histogram
        from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract

        LIVE_BIRTH = 1
        extract = FamilyGrowthExtract()

        live = extract.pregnancies[extract.pregnancies.outcome == LIVE_BIRTH]
        histogram = Histogram.from_series(live.birthwgt_lb, label='birthweight lb')
        breakpoint()

        histogram.plot(xlabel='value', ylabel='frequency')

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
