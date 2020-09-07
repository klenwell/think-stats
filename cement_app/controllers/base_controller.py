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
        from cement_app.decorators.pmf import ProbabilityMassFunction

        extract = FamilyGrowthExtract()
        first_births = extract.live_first_births
        other_births = extract.live_non_first_births

        first_pmf = ProbabilityMassFunction(first_births.prglngth, 'first')
        plot = first_pmf.plot()
        plot.show()

        other_pmf = ProbabilityMassFunction(other_births.prglngth, 'non-first')
        plot = other_pmf.plot()
        plot.show()

        plot = first_pmf.plot_against(other_pmf)
        plot.xlabel('Weeks')
        plot.axis([27, 46, 0, 1.0])
        plot.show()
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
