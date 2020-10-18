from cement import Controller
from cement import ex as expose


class ChartsController(Controller):
    class Meta:
        label = 'charts'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py charts os-vs-states
    # This command can be used for testing and development.
    @expose(help="Generates a map showing states smaller than the OC (CA).")
    def os_vs_states(self):
        print("TODO")


    # python app.py charts interactive
    # This command can be used for testing and development.
    @expose(help="Run the Application interactively. Useful for testing and development.")
    def interactive(self):
        import plotly.figure_factory as ff
        import plotly.graph_objects as go
        import requests
        import csv
        from pprint import pprint

        OC_POP = 3175692
        OC_FIPS = '06059'

        # Get State Abbreviations
        url = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'
        response = requests.get(url)

        # https://stackoverflow.com/a/38677619/1093087
        f = (line.decode('utf-8') for line in response.iter_lines())
        reader = csv.DictReader(f)
        state_codes = dict([(row['State'], row['Postal']) for row in reader])
        pprint(state_codes)

        # Get Latest State Pop Data
        pop_pct = lambda st_pop: st_pop / OC_POP * 100
        url = 'https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:*'
        rows = requests.get(url).json()
        states = [(row[2], int(row[1]), row[0]) for row in rows[1:]]
        smaller_states = [(state_codes[st[2]], pop_pct(st[1]), st[1]) for st in states if st[1] <= OC_POP]
        pprint(sorted(smaller_states, key=lambda r: r[1], reverse=True))

        # Map Attrs
        map_title = [
            'States with Populations Smaller than Orange County, CA',
            'OC Population: 3,175,692'
        ]
        color_scale = [
            "#fff5e6", "#ffe0b3", "#ffcc80", "#ffb84d",
            "#ffa31a", "#ff9900", "#e68a00", "#cc7a00"
        ]
        locations = [st[0] for st in smaller_states]
        zs = [st[1] for st in smaller_states]

        # https://plotly.com/python/choropleth-maps/#united-states-choropleth-map
        fig = go.Figure(data=go.Choropleth(
            locations=locations, # Spatial coordinates
            z = zs, # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = color_scale,
            colorbar_title = '% of OC Population'
        ))
        fig.update_layout(
            title_text = '<br>'.join(map_title),
            geo_scope='usa', # limite map scope to USA
        )
        fig.show()
