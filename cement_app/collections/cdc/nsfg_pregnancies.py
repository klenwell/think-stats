from cement_app.services.caching_service import cached_property
from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract, LIVE_BIRTH
from cement_app.models.cdc.pregnancy import Pregnancy


class NsfgPregnancies:
    #
    #
    #

    #
    # Properties
    #
    @cached_property
    def extract(self):
        return FamilyGrowthExtract()

    @cached_property
    def data_frame(self):
        # Returns pandas.core.frame.DataFrame object.
        return self.extract.pregnancies

    #
    # Instance Methods
    #
    def __init__(self):
        pass

    def by_case_id(self, case_id):
        # case_id is a NSFG respondent case_id
        pregnancies = []
        data_frame = self.data_frame[self.data_frame.caseid == case_id]

        for row in data_frame.itertuples():
            attrs = {
                'mother_age': row.agepreg,
                'live': row.outcome == LIVE_BIRTH,
                'weeks': row.prglngth,
                'weight': row.totalwgt_lb,
                'sex': row.babysex,
                'first': row.birthord == 1
            }
            pregnancy = Pregnancy(**attrs)
            pregnancies.append(pregnancy)

        return pregnancies
