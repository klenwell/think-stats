"""
Source:
https://github.com/AllenDowney/ThinkStats2/blob/9ee747/code/relay.py
https://github.com/AllenDowney/ThinkStats2/blob/9ee747/code/Apr25_27thAn_set1.shtml

Used with Think Stats 2e:
http://greenteapress.com/thinkstats2/html/thinkstats2004.html
"""
import requests
import csv
import plotly.graph_objects as go

from cement_app.services.caching_service import cached_property
from cement_app.config.maps import US_STATES_NAME_TO_ABBR


#
# Constants
#
OC_POPULATION = 3175692
OC_FIPS = '06059'


class OcVsStatePopulationChart:
    #
    # Properties
    #
    @cached_property
    def state_populations(self):
        state_data = {}
        API_URL = 'https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:*'
        rows = requests.get(API_URL).json()

        # First row is headers: NAME, POP, state
        for row in rows[1:]:
            name, population, code = row
            state_data[name] = {
                'population': int(population),
                'name': name,
                'code': code,
                'abbr': US_STATES_NAME_TO_ABBR[name]
            }

        return state_data

    @cached_property
    def state_abbreviations_2014(self):
        CSV_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'
        response = requests.get(CSV_URL)

        # https://stackoverflow.com/a/38677619/1093087
        f = (line.decode('utf-8') for line in response.iter_lines())
        reader = csv.DictReader(f)
        state_codes = dict([(row['State'], row['Postal']) for row in reader])
        return state_codes

    @property
    def states_smaller_than_oc(self):
        small_states = []
        for state in self.state_populations.values():
            if state['population'] <= OC_POPULATION:
                small_states.append(state)
        return small_states

    @property
    def states_smaller_than_oc_sorted(self):
        return sorted(self.states_smaller_than_oc,
                      key=lambda st: st['population'],
                      reverse=True)

    @property
    def locations(self):
        return [state['abbr'] for state in self.states_smaller_than_oc_sorted]

    @property
    def choropleth_data(self):
        values = []

        for state in self.states_smaller_than_oc_sorted:
            value = self.compute_oc_pop_pct(state['population'])
            values.append(value)

        return values

    @property
    def color_scale(self):
        # Based on https://www.w3schools.com/colors/colors_picker.asp
        return [
            "#fff5e6",
            "#ffe0b3",
            "#ffcc80",
            "#ffb84d",
            "#ffa31a",
            "#ff9900",
            "#e68a00",
            "#cc7a00"
        ]

    @property
    def colorbar_title(self):
        return '% of OC Population'

    @property
    def chart_title(self):
        title = 'States with Populations Smaller than Orange County, CA'
        subtitle = 'OC Population: {:,}'.format(OC_POPULATION)
        return '<br>'.join([title, subtitle])

    #
    # Instance Methods
    #
    def __init__(self):
        pass

    def generate_map(self):
        # https://plotly.com/python/choropleth-maps/#united-states-choropleth-map
        location_mode = 'USA-states'
        geo_scope = 'usa'

        figure_data = go.Choropleth(
            locations=self.locations,
            z=self.choropleth_data,
            locationmode=location_mode,
            colorscale=self.color_scale,
            colorbar_title=self.colorbar_title
        )

        fig = go.Figure(data=figure_data)
        fig.update_layout(title_text=self.chart_title, geo_scope=geo_scope)
        return fig

    #
    # Private
    #
    def compute_oc_pop_pct(self, state_pop):
        return state_pop / OC_POPULATION * 100
