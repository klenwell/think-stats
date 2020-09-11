from cement_app.services.caching_service import cached_property
from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract


class NsfgRespondentsCollection:
    @staticmethod
    def kids_per_household():
        # Returns pandas.core.series.Series object.
        collection = females_with_multiple_births()
        return collection.data_frame.numkdhh

    @staticmethod
    def females_with_multiple_births():
        # Returns pandas.core.series.Series object.
        collection = NsfgRespondentsCollection()
        return collection.data_frame[collection.data_frame.pregnum > 1]

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
