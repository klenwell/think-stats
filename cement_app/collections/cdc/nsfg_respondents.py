from cement_app.services.caching_service import cached_property
from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract
from cement_app.collections.cdc.nsfg_pregnancies import NsfgPregnancies
from cement_app.models.cdc.mother import Mother


class NsfgRespondents:
    @staticmethod
    def kids_per_household():
        # Returns pandas.core.series.Series object.
        collection = NsfgRespondents()
        return collection.data_frame.numkdhh

    @staticmethod
    def females_with_multiple_babies():
        """Returns list of Mother objects.
        """
        moms = []
        nsfg_respondents = NsfgRespondents()
        nsfg_pregnancies = NsfgPregnancies()
        data_frame = nsfg_respondents.data_frame[nsfg_respondents.data_frame.pregnum > 1]

        # https://stackoverflow.com/questions/16476924/#comment79152689_16476974
        for case_id in data_frame['caseid']:
            pregnancies = nsfg_pregnancies.by_case_id(case_id)
            mom = Mother(case_id, pregnancies)

            if mom.had_multiple_babies():
                moms.append(mom)

        return moms

    #
    # Properties
    #
    @cached_property
    def extract(self):
        return FamilyGrowthExtract()

    @cached_property
    def data_frame(self):
        # Returns pandas.core.frame.DataFrame object.
        return self.extract.females
