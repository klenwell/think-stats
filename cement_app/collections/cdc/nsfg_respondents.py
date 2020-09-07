from cement_app.services.caching_service import cached_property
from cement_app.extracts.cdc.nsfg import FamilyGrowthExtract


class NsfgRespondentsCollection:
    @staticmethod
    def kids_per_household():
        # Returns pandas.core.series.Series object.
        collection = NsfgRespondentsCollection()
        return collection.data_frame.numkdhh

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
