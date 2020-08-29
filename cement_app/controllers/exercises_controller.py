from cement import Controller
from cement import ex as expose

from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract


class ExercisesController(Controller):
    class Meta:
        label = 'exercise'
        stacked_on = 'base'
        stacked_type = 'nested'

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
        preg_count_buckets = extract.respondents.pregnum.value_counts()

        for count in range(7):
            assert preg_count_buckets[count] == nsfg_codebook_preg_counts[count]

        print(extract.respondents)
