import pandas as pd


class GrabbleFrame(pd.DataFrame):

    # temporary properties
    _internal_names = pd.DataFrame._internal_names + ["internal_cache"]
    _internal_names_set = set(_internal_names)

    # normal properties
    _metadata = ["added_property"]

    @property
    def _constructor(self):
        return SubclassedDataFrame2

    @property
    def _constructor_sliced(self):
        return SubclassedSeries
