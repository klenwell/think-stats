from cement import Controller
from cement import ex as expose


class BaseController(Controller):
    class Meta:
        label = 'base'

    # python app.py interactive
    # This command can be used for testing and development.
    @expose(help="Run the Application interactively. Useful for testing and development.")
    def interactive(self):
        from cement_app.decorators.pmf import ProbabilityMassFunction

        pmf = ProbabilityMassFunction([1, 2, 2, 3, 5])
        assert pmf.prob(1) == 0.2
        assert pmf.total == sum(pmf.probabilities())
        print(pmf.prob(2))
        print(pmf.total)

        pmf.increase(2, 0.2)
        print(pmf.prob(2))
        print(pmf.total)

        pmf.normalize()
        print(pmf.prob(2))
        print(pmf.total)

        pmf.multiply(2, 0.5)
        print(pmf.prob(2))
        print(pmf.total)

        pmf.normalize()
        print(pmf.prob(2))
        print(pmf.total)

        print(pmf)
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
