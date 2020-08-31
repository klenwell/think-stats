from cement import Controller
from cement import ex as expose

from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract
from cement_app.decorators.histogram import Histogram


class ExercisesController(Controller):
    class Meta:
        label = 'exercise'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py exercise 2.1
    @expose(aliases=['2.1'])
    def ch2_1(self):
        LIVE_BIRTH = 1
        FIRST_BIRTH = 1

        extract = FamilyGrowthExtract()
        live = extract.pregnancies[extract.pregnancies.outcome == LIVE_BIRTH]

        first_births = live[live.birthord == FIRST_BIRTH]
        other_births = live[live.birthord != FIRST_BIRTH]

        first_hist = Histogram.from_series(first_births.prglngth, label="first")
        other_hist = Histogram.from_series(other_births.prglngth, label="other")

        vars = {
            'first': first_hist,
            'other': other_hist
        }
        self.app.render(vars, 'exercises/ch2_1.jinja2')


    # python app.py exercise 1.2
    @expose(aliases=['1.2'])
    def ch1_2(self):
        # Source: https://www.icpsr.umich.edu/nsfg6/Controller \
        # ?displayPage=labelDetails&fileCode=FEM&section=R&subSec=7869&srtLabel=606835
        nsfg_codebook_preg_counts = {
            0: 2610,
            1: 1267,
            2: 1432,
            3: 1110,
            4: 611,
            5: 305,
            6: 150,
            '7+': 158
        }
        extract = FamilyGrowthExtract()
        preg_count_buckets = extract.females.pregnum.value_counts()

        # Compare value counts to the published results in the NSFG codebook.
        for count in range(7):
            assert preg_count_buckets[count] == nsfg_codebook_preg_counts[count]

        vars = {'extract': extract}
        self.app.render(vars, 'exercises/ch1_2.jinja2')
