from cement import Controller
from cement import ex as expose

from cement_app.charts.us_maps.oc_states import OcVsStatePopulationChart


class ChartsController(Controller):
    class Meta:
        label = 'charts'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py charts os-vs-states
    # This command can be used for testing and development.
    @expose(help="Generates a map showing states smaller than the OC (CA).")
    def os_vs_states(self):
        chart = OcVsStatePopulationChart()
        map = chart.generate_map()
        map.show()

        small_states = []
        for state in chart.states_smaller_than_oc_sorted:
            pop = '{:,}'.format(state['population'])
            small_states.append((state['name'], pop))

        vars = {
            'chart': chart,
            'small_states': small_states
        }
        self.app.render(vars, 'charts/oc_vs_states.jinja2')

    # python app.py charts interactive
    # This command can be used for testing and development.
    @expose(help="Run the Application interactively. Useful for testing and development.")
    def interactive(self):
        from pprint import pprint
        chart = OcVsStatePopulationChart()
        pprint(chart.state_populations)
