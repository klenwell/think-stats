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
        extract = FamilyGrowthExtract()
        breakpoint()
