from cement import Controller
from cement import ex as expose
from statistics import mean, stdev

from cement_app.extracts.brisbane.births import BrisbaneBirthsExtract
from cement_app.decorators.cdf import CumulativeDistributionFunction as CDF


class Chapter5Controller(Controller):
    class Meta:
        label = 'ch-5'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py ch-5 s1
    @expose(aliases=['s1'])
    def section_5_1(self):
        extract = BrisbaneBirthsExtract()
        diffs = extract.dataframe.minutes.diff()
        cdf = CDF.from_series(diffs, 'actual')
        chart = cdf.plot()
        chart.show()
