from cement import Controller
from cement import ex as expose

from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract
from cement_app.decorators.histogram import Histogram
from cement_app.decorators.pmf import ProbabilityMassFunction
from cement_app.collections.cdc.nsfg_respondents import NsfgRespondents


class ExercisesController(Controller):
    class Meta:
        label = 'exercise'
        stacked_on = 'base'
        stacked_type = 'nested'

    # python app.py exercise 3.3
    @expose(aliases=['3.3'])
    def ch3_3(self):
        moms = NsfgRespondents.females_with_multiple_babies()
        preg_len_diffs = [mom.diff_first_baby_weeks() for mom in moms]
        print(sum(preg_len_diffs) / len(preg_len_diffs))

    # python app.py exercise 3.2
    @expose(aliases=['3.2'])
    def ch3_2(self):
        simple_list = [1, 2, 2, 3, 5]
        pmf = ProbabilityMassFunction(simple_list)
        vars = {
            'pmf': pmf
        }
        self.app.render(vars, 'exercises/ch3_2.jinja2')

    # python app.py exercise 3.1
    @expose(aliases=['3.1'])
    def ch3_1(self):
        kids_per_household = NsfgRespondents.kids_per_household()
        pmf = ProbabilityMassFunction(kids_per_household, 'Kids per Household')
        biased_pmf = pmf.bias()

        # Chart will pop up and halt.
        chart = pmf.plot_against(biased_pmf)
        chart.show()

        vars = {
            'pmf': pmf,
            'biased_pmf': biased_pmf
        }
        self.app.render(vars, 'exercises/ch3_1.jinja2')

    # python app.py exercise 2.4
    @expose(aliases=['2.4'])
    def ch2_4(self):
        extract = FamilyGrowthExtract()
        first_birth_weights = extract.live_first_births.totalwgt_lb
        other_birth_weights = extract.live_non_first_births.totalwgt_lb
        cohen_d = FamilyGrowthExtract.cohen_effect_size(first_birth_weights, other_birth_weights)

        vars = {
            'first': first_birth_weights,
            'other': other_birth_weights,
            'cohen_d': cohen_d
        }
        self.app.render(vars, 'exercises/ch2_4.jinja2')

    # python app.py exercise 2.3
    @expose(aliases=['2.3'])
    def ch2_3(self):
        extract = FamilyGrowthExtract()
        histogram = Histogram.from_series(extract.pregnancies.prglngth, label="prglngth")

        vars = {
            'mode': histogram.mode,
            'mode_freq': histogram.freq(histogram.mode),
            'modes': histogram.modes
        }
        self.app.render(vars, 'exercises/ch2_3.jinja2')

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
